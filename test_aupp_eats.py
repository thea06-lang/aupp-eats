"""
AUPPeats — Automated Tests
Run locally with: python test_aupp_eats.py
These same tests run automatically on GitHub every time you push.
"""

import sys
import os
import sqlite3

# Make sure imports work from the project root
sys.path.insert(0, os.path.dirname(__file__))

from database import initialize_db, get_connection
from data.seed import seed_data
from models.meal import (
    get_all_meals,
    get_meal_by_id,
    get_meals_within_budget,
    get_meals_by_category,
    search_meals,
)
from models.spot import get_all_spots, get_spot_by_id
from models.log import (
    log_meal,
    get_logs_by_date,
    get_total_spent_on_date,
    get_most_logged_meals,
    delete_log,
)


# ─────────────────────────────────────────────
#  Test Runner Helpers
# ─────────────────────────────────────────────

passed = 0
failed = 0

def check(description, condition):
    global passed, failed
    if condition:
        print(f"  ✔  {description}")
        passed += 1
    else:
        print(f"  ✘  FAILED: {description}")
        failed += 1


# ─────────────────────────────────────────────
#  Setup — use a separate test database
# ─────────────────────────────────────────────

# Point the app at a test DB so we never touch real data
os.environ["AUPP_EATS_TEST"] = "1"
import database
database.DB_PATH = os.path.join(os.path.dirname(__file__), "test_aupp_eats.db")

print("\n  Setting up test database...")
initialize_db()
seed_data()
print("  Done.\n")


# ─────────────────────────────────────────────
#  Database Tests
# ─────────────────────────────────────────────

print("── Database ──────────────────────────────────")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
conn.close()

check("food_spots table exists",  "food_spots" in tables)
check("meals table exists",       "meals"      in tables)
check("budget table exists",      "budget"     in tables)
check("meal_logs table exists",   "meal_logs"  in tables)


# ─────────────────────────────────────────────
#  Seed Data Tests
# ─────────────────────────────────────────────

print("\n── Seed Data ─────────────────────────────────")

spots = get_all_spots()
meals = get_all_meals()

check("At least 3 food spots seeded",  len(spots) >= 3)
check("At least 10 meals seeded",      len(meals) >= 10)
check("AUPP Canteen exists",           any(s["name"] == "AUPP Canteen" for s in spots))
check("Event Stalls exists",           any(s["name"] == "Event Stalls"  for s in spots))
check("All meals have a price > 0",    all(m["price"] > 0 for m in meals))
check("All meals have a name",         all(m["name"]  for m in meals))


# ─────────────────────────────────────────────
#  Meal Model Tests
# ─────────────────────────────────────────────

print("\n── Meal Model ────────────────────────────────")

budget_meals = get_meals_within_budget(2.00)
check("get_meals_within_budget(2.00) returns results",       len(budget_meals) > 0)
check("All returned meals are within budget",                all(m["price"] <= 2.00 for m in budget_meals))
check("Results are sorted cheapest first",                   budget_meals[0]["price"] <= budget_meals[-1]["price"])

zero_meals = get_meals_within_budget(0.00)
check("get_meals_within_budget(0.00) returns nothing",       len(zero_meals) == 0)

drink_meals = get_meals_by_category("Drink")
check("get_meals_by_category('Drink') returns results",      len(drink_meals) > 0)
check("All returned meals are in Drink category",            all(m["category"].lower() == "drink" for m in drink_meals))

search_results = search_meals("rice")
check("search_meals('rice') returns results",                len(search_results) > 0)
check("search_meals('rice') results contain 'rice'",         all("rice" in m["name"].lower() for m in search_results))

no_results = search_meals("zzznomatch")
check("search_meals with no match returns empty list",       len(no_results) == 0)

meal = get_meal_by_id(1)
check("get_meal_by_id(1) returns a meal",                    meal is not None)
check("get_meal_by_id(1) has expected fields",               "name" in meal.keys() and "price" in meal.keys())

missing = get_meal_by_id(99999)
check("get_meal_by_id with bad ID returns None",             missing is None)


# ─────────────────────────────────────────────
#  Spot Model Tests
# ─────────────────────────────────────────────

print("\n── Spot Model ────────────────────────────────")

spot = get_spot_by_id(1)
check("get_spot_by_id(1) returns a spot",        spot is not None)
check("Spot has name and location fields",        "name" in spot.keys() and "location" in spot.keys())


# ─────────────────────────────────────────────
#  Log Model Tests
# ─────────────────────────────────────────────

print("\n── Log Model ─────────────────────────────────")

from datetime import date
today = str(date.today())

# Start fresh for log tests
conn = get_connection()
conn.execute("DELETE FROM meal_logs WHERE log_date = ?", (today,))
conn.commit()
conn.close()

initial_total = get_total_spent_on_date()
check("Total spent starts at 0.0 before logging",   initial_total == 0.0)

log_id = log_meal(1, 1.50)
check("log_meal returns a valid ID",                log_id is not None and log_id > 0)

logs = get_logs_by_date()
check("get_logs_by_date() returns today's log",     len(logs) == 1)
check("Logged meal has correct price",              logs[0]["price_paid"] == 1.50)

log_meal(2, 2.00)
total = get_total_spent_on_date()
check("Total spent updates correctly after 2 logs", round(total, 2) == 3.50)

deleted = delete_log(log_id)
check("delete_log returns True for valid ID",       deleted is True)

logs_after = get_logs_by_date()
check("Log is removed after delete",                len(logs_after) == 1)

bad_delete = delete_log(99999)
check("delete_log returns False for bad ID",        bad_delete is False)

log_meal(1, 1.50)
log_meal(1, 1.50)
favorites = get_most_logged_meals(limit=3)
check("get_most_logged_meals returns results",      len(favorites) > 0)
check("Favorites sorted by most ordered",           favorites[0]["times_ordered"] >= 1)


# ─────────────────────────────────────────────
#  Cleanup
# ─────────────────────────────────────────────

if os.path.exists(database.DB_PATH):
    os.remove(database.DB_PATH)

# ─────────────────────────────────────────────
#  Summary
# ─────────────────────────────────────────────

total_tests = passed + failed
print(f"\n── Results ───────────────────────────────────")
print(f"  {passed}/{total_tests} tests passed")

if failed == 0:
    print("  ✔  All tests passed!\n")
else:
    print(f"  ✘  {failed} test(s) failed.\n")
    sys.exit(1)  # non-zero exit tells GitHub Actions the build failed

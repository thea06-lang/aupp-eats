import sys
import os

from database import initialize_db, get_connection
from data.seed import seed_data

from models.meal import (
    get_all_meals,
    get_meals_within_budget,
    get_meals_by_spot,
    get_meals_by_category,
    search_meals,
    get_meal_by_id,
)
from models.spot import get_all_spots
from models.log  import (
    log_meal,
    get_logs_by_date,
    get_total_spent_on_date,
    get_logs_by_week,
    get_most_logged_meals,
    delete_log,
)
from utils.display import (
    print_banner,
    print_header,
    print_separator,
    print_blank,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_budget_status,
    print_meal_list,
    print_meal_detail,
    print_spot_list,
    print_log_list,
    print_favorites,
    print_menu,
    print_weekly_summary,
)
from utils.helpers import (
    get_int_input,
    get_float_input,
    get_week_range,
    today_str,
    press_enter_to_continue,
)

from colorama import Fore, Style


# ─────────────────────────────────────────────
#  Budget Helpers
# ─────────────────────────────────────────────

def get_active_budget():
    """Fetch today's budget amount. Returns None if not set."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT daily_amount FROM budget
        WHERE set_date = ?
        ORDER BY id DESC LIMIT 1
    """, (today_str(),))
    row = cursor.fetchone()
    conn.close()
    return row["daily_amount"] if row else None


def set_budget(amount):
    """Save a new daily budget for today."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budget (daily_amount, set_date)
        VALUES (?, ?)
    """, (amount, today_str()))
    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
#  Screens
# ─────────────────────────────────────────────

def screen_setup_budget():
    """First-time budget setup screen."""
    print_header("Set Your Daily Budget")
    print_info("How much do you want to spend on food today?")
    print_blank()
    amount = get_float_input("Enter amount in USD (e.g. 5.00):", min_val=0.5)
    if amount:
        set_budget(amount)
        print_success(f"Budget set to ${amount:.2f} for today!")
    else:
        print_warning("No budget set. Using default of $5.00.")
        set_budget(5.00)
    press_enter_to_continue()


def screen_browse_meals(budget):
    """Browse meals with filtering options."""
    while True:
        print_menu("Browse Meals", [
            "All meals",
            "Meals within my remaining budget",
            "Browse by food spot",
            "Browse by category",
            "Search by name",
            "Back",
        ])
        choice = get_int_input("", min_val=1, max_val=6)

        if choice == 1:
            print_header("All Meals")
            print_meal_list(get_all_meals())
            press_enter_to_continue()

        elif choice == 2:
            spent     = get_total_spent_on_date()
            remaining = budget - spent
            if remaining <= 0:
                print_warning("You've hit your budget for today!")
            else:
                print_header(f"Meals Under ${remaining:.2f}")
                print_meal_list(get_meals_within_budget(remaining))
            press_enter_to_continue()

        elif choice == 3:
            spots = get_all_spots()
            print_header("Choose a Food Spot")
            print_spot_list(spots)
            idx = get_int_input("Enter spot number (0 to cancel):", min_val=1, max_val=len(spots))
            if idx:
                spot = spots[idx - 1]
                print_header(spot["name"])
                print_meal_list(get_meals_by_spot(spot["id"]))
                press_enter_to_continue()

        elif choice == 4:
            categories = ["Rice", "Noodles", "Snack", "Drink"]
            print_header("Choose a Category")
            for i, cat in enumerate(categories, start=1):
                print(f"  {Fore.CYAN}[{i}]{Style.RESET_ALL}  {cat}")
            print_blank()
            idx = get_int_input("Enter category number (0 to cancel):", min_val=1, max_val=4)
            if idx:
                cat = categories[idx - 1]
                print_header(cat)
                print_meal_list(get_meals_by_category(cat))
                press_enter_to_continue()

        elif choice == 5:
            print_header("Search Meals")
            keyword = input(Fore.WHITE + Style.BRIGHT + "  Enter keyword: ").strip()
            if keyword:
                results = search_meals(keyword)
                if results:
                    print_meal_list(results)
                else:
                    print_warning(f"No meals found for '{keyword}'.")
            press_enter_to_continue()

        else:
            break


def screen_log_meal(budget):
    """Log a meal the user just ate."""
    print_header("Log a Meal")

    spent     = get_total_spent_on_date()
    remaining = budget - spent
    print_info(f"Remaining budget today: ${remaining:.2f}")
    print_blank()

    # Show all meals for the user to pick from
    meals = get_all_meals()
    print_meal_list(meals)

    idx = get_int_input(f"Enter meal number to log (0 to cancel):", min_val=1, max_val=len(meals))
    if not idx:
        return

    meal = meals[idx - 1]
    print_blank()
    print_meal_detail(meal)

    # Warn if over budget
    if meal["price"] > remaining:
        print_warning(f"This meal costs ${meal['price']:.2f} but you only have ${remaining:.2f} left!")
        confirm = input(Fore.YELLOW + "  Log it anyway? (y/n): ").strip().lower()
        if confirm != "y":
            print_info("Cancelled.")
            press_enter_to_continue()
            return

    log_meal(meal["id"], meal["price"])
    print_success(f"Logged: {meal['name']} — ${meal['price']:.2f}")

    # Show updated budget
    new_spent = get_total_spent_on_date()
    print_budget_status(budget, new_spent)
    press_enter_to_continue()


def screen_view_budget(budget):
    """View and optionally update the daily budget."""
    spent = get_total_spent_on_date()
    print_budget_status(budget, spent)

    print_header("Today's Meals")
    print_log_list(get_logs_by_date())

    print_blank()
    print_menu("Budget Options", [
        "Update today's budget",
        "Remove a logged meal",
        "Back",
    ])
    choice = get_int_input("", min_val=1, max_val=3)

    if choice == 1:
        amount = get_float_input("Enter new budget amount:", min_val=0.5)
        if amount:
            set_budget(amount)
            print_success(f"Budget updated to ${amount:.2f}!")
        press_enter_to_continue()
        return amount  # return updated budget

    elif choice == 2:
        logs = get_logs_by_date()
        if not logs:
            print_info("Nothing to remove.")
        else:
            print_log_list(logs)
            idx = get_int_input("Enter log number to remove (0 to cancel):", min_val=1, max_val=len(logs))
            if idx:
                log_id = logs[idx - 1]["id"]
                if delete_log(log_id):
                    print_success("Log entry removed.")
                else:
                    print_error("Could not remove that entry.")
        press_enter_to_continue()

    return budget


def screen_weekly_summary():
    """Show spending across this week."""
    start, end = get_week_range()
    logs  = get_logs_by_week(start, end)
    print_weekly_summary(logs, start, end)
    press_enter_to_continue()


def screen_favorites():
    """Show the user's most ordered meals."""
    print_header("Your Favorites")
    print_favorites(get_most_logged_meals(limit=5))
    press_enter_to_continue()


# ─────────────────────────────────────────────
#  Main Loop
# ─────────────────────────────────────────────

def main():
    # Boot sequence
    initialize_db()
    seed_data()

    print_banner()

    # Budget check — set one if missing
    budget = get_active_budget()
    if not budget:
        screen_setup_budget()
        budget = get_active_budget()

    # Main app loop
    while True:
        spent = get_total_spent_on_date()
        print_budget_status(budget, spent)

        print_menu("Main Menu", [
            "Browse meals",
            "Log a meal",
            "View budget & today's log",
            "Weekly summary",
            "My favorites",
            "Exit",
        ])

        choice = get_int_input("", min_val=1, max_val=6)

        if choice == 1:
            screen_browse_meals(budget)

        elif choice == 2:
            screen_log_meal(budget)

        elif choice == 3:
            updated = screen_view_budget(budget)
            if updated:
                budget = updated

        elif choice == 4:
            screen_weekly_summary()

        elif choice == 5:
            screen_favorites()

        elif choice == 6 or choice is None:
            print_blank()
            print(Fore.CYAN + Style.BRIGHT + "  See you next meal, Kunthea! 👋")
            print_blank()
            sys.exit(0)


if __name__ == "__main__":
    main()

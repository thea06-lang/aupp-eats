import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_connection


def is_already_seeded(cursor):
    """Check if data has already been seeded to avoid duplicates."""
    cursor.execute("SELECT COUNT(*) FROM food_spots")
    count = cursor.fetchone()[0]
    return count > 0


def seed_data():
    """Insert default food spots and meals into the database."""
    conn = get_connection()
    cursor = conn.cursor()

    if is_already_seeded(cursor):
        print("Data already seeded. Skipping.")
        conn.close()
        return

    # -------------------------
    # Insert Food Spots
    # -------------------------
    spots = [
        ("AUPP Canteen",    "Inside AUPP campus",   "The main daily canteen on campus. Open on regular school days."),
        ("Event Stalls",    "AUPP campus grounds",  "Pop-up food stalls during AUPP events and special occasions."),
        ("Outside Vendors", "Near AUPP entrance",   "Food carts and stalls just outside the campus gates."),
    ]

    cursor.executemany("""
        INSERT INTO food_spots (name, location, description)
        VALUES (?, ?, ?)
    """, spots)

    # Grab the IDs that were just inserted
    cursor.execute("SELECT id, name FROM food_spots")
    spot_map = {row["name"]: row["id"] for row in cursor.fetchall()}

    canteen_id = spot_map["AUPP Canteen"]
    event_id   = spot_map["Event Stalls"]
    outside_id = spot_map["Outside Vendors"]

    # -------------------------
    # Insert Meals
    # -------------------------
    meals = [
        # AUPP Canteen
        (canteen_id, "Fried Rice",              1.50, "Rice"),
        (canteen_id, "Rice with Chicken Curry", 2.00, "Rice"),
        (canteen_id, "Rice with Stir-Fry Pork", 2.00, "Rice"),
        (canteen_id, "Beef Noodle Soup",         2.50, "Noodles"),
        (canteen_id, "Stir-Fry Noodles",         2.00, "Noodles"),
        (canteen_id, "Baguette Sandwich",        1.50, "Snack"),
        (canteen_id, "Sugarcane Juice",          0.75, "Drink"),
        (canteen_id, "Iced Coffee",              1.00, "Drink"),
        (canteen_id, "Water Bottle",             0.50, "Drink"),

        # Event Stalls
        (event_id,   "BBQ Skewers (x3)",        2.00, "Snack"),
        (event_id,   "Grilled Corn",             1.00, "Snack"),
        (event_id,   "Papaya Salad",             1.50, "Salad"),
        (event_id,   "Fresh Fruit Cup",          1.00, "Snack"),
        (event_id,   "Bubble Tea",               2.50, "Drink"),
        (event_id,   "Fried Chicken",            2.50, "Snack"),

        # Outside Vendors
        (outside_id, "Num Banh Chok (Khmer Noodles)", 1.50, "Noodles"),
        (outside_id, "Congee (Rice Porridge)",          1.00, "Rice"),
        (outside_id, "Banh Mi (Baguette)",              1.25, "Snack"),
        (outside_id, "Fresh Coconut",                   1.50, "Drink"),
        (outside_id, "Iced Sugar Cane Juice",           0.75, "Drink"),
    ]

    cursor.executemany("""
        INSERT INTO meals (spot_id, name, price, category)
        VALUES (?, ?, ?, ?)
    """, meals)

    conn.commit()
    conn.close()
    print(f"Seeded {len(spots)} food spots and {len(meals)} meals successfully.")


if __name__ == "__main__":
    seed_data()

import sqlite3

conn = sqlite3.connect("practice.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS food(
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT NOT NULL,
        price    REAL NOT NULL,
        category TEXT
    )
""")

# ── Rice ──────────────────────────────────────────────
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Fried Rice', 2.00, 'Rice')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('White Rice with Pork', 1.50, 'Rice')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Chicken Rice', 2.00, 'Rice')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Mixed Rice', 1.75, 'Rice')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Egg Fried Rice', 1.50, 'Rice')")

# ── Noodles ───────────────────────────────────────────
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Beef Noodle Soup', 2.50, 'Noodles')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Stir Fried Noodles', 2.00, 'Noodles')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Kuy Teav', 1.75, 'Noodles')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Glass Noodle Soup', 2.00, 'Noodles')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Pad Thai', 2.50, 'Noodles')")

# ── Snack ─────────────────────────────────────────────
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Spring Roll', 0.50, 'Snack')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Corn', 0.75, 'Snack')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Grilled Banana', 0.50, 'Snack')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Baguette with Egg', 1.00, 'Snack')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Steamed Bun', 0.75, 'Snack')")

# ── Drink ─────────────────────────────────────────────
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Iced Coffee', 1.00, 'Drink')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Sugar Cane Juice', 0.75, 'Drink')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Coconut Water', 1.00, 'Drink')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Thai Milk Tea', 1.25, 'Drink')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Water Bottle', 0.50, 'Drink')")

# ── Extra ─────────────────────────────────────────────
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Pork Skewer', 0.75, 'Snack')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Mango Sticky Rice', 1.50, 'Snack')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Iced Lemon Tea', 1.00, 'Drink')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Congee', 1.50, 'Rice')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Vermicelli Salad', 2.00, 'Noodles')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Grilled Pork Rice', 2.00, 'Rice')")
cursor.execute("INSERT INTO food (name, price, category) VALUES ('Soy Milk', 0.75, 'Drink')")

conn.commit()
print("Food added!")


# ─────────────────────────────────────────────────────
#  get_food() — filter by category and/or max price
# ─────────────────────────────────────────────────────

def get_food(category=None, max_price=None):
    query = "SELECT * FROM food WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if max_price:
        query += " AND price <= ?"
        params.append(max_price)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    for row in rows:
        print(row)


# ─────────────────────────────────────────────────────
#  Call the function — these are OUTSIDE the function
# ─────────────────────────────────────────────────────

print("\n── All food under $1.00 ──")
get_food(max_price=1.00)

print("\n── All Rice ──")
get_food(category="Rice")

print("\n── All Drinks ──")
get_food(category="Drink")

print("\n── Drinks under $1.00 ──")
get_food(category="Drink", max_price=1.00)

print("\n── Everything ──")
get_food()


conn.close()

import sqlite3
import os

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), "aupp_eats.db")


def get_connection():
    """Create and return a connection to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def initialize_db():
    """Create all tables if they don't exist yet."""
    conn = get_connection()
    cursor = conn.cursor()

    # --- Food Spots ---
    # Represents a place where food is sold near/at AUPP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_spots (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT
        )
    """)

    # --- Meals ---
    # Each meal belongs to a food spot
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_id  INTEGER NOT NULL,
            name     TEXT NOT NULL,
            price    REAL NOT NULL,
            category TEXT,
            FOREIGN KEY (spot_id) REFERENCES food_spots(id)
        )
    """)

    # --- Budget ---
    # Stores the user's daily budget (one active budget at a time)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            daily_amount REAL NOT NULL,
            set_date     TEXT NOT NULL
        )
    """)

    # --- Meal Logs ---
    # Records every meal the user logs throughout the day
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_logs (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id    INTEGER NOT NULL,
            log_date   TEXT NOT NULL,
            price_paid REAL NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_db()

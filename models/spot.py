import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_connection


def get_all_spots():
    """
    Return all food spots.
    Each row includes: id, name, location, description.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, location, description
        FROM food_spots
        ORDER BY name
    """)
    spots = cursor.fetchall()
    conn.close()
    return spots


def get_spot_by_id(spot_id):
    """
    Return a single food spot by its ID.
    Returns None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, location, description
        FROM food_spots
        WHERE id = ?
    """, (spot_id,))
    spot = cursor.fetchone()
    conn.close()
    return spot


def get_spot_by_name(name):
    """
    Search for a food spot by name (partial match, case-insensitive).
    Returns a list in case multiple spots match.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, location, description
        FROM food_spots
        WHERE LOWER(name) LIKE LOWER(?)
    """, (f"%{name}%",))
    spots = cursor.fetchall()
    conn.close()
    return spots

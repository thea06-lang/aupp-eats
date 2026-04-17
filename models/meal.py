import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_connection


def get_all_meals():
    """
    Return all meals joined with their food spot name.
    Each row includes: id, name, price, category, spot_name.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.name, m.price, m.category, s.name AS spot_name
        FROM meals m
        JOIN food_spots s ON m.spot_id = s.id
        ORDER BY s.name, m.price
    """)
    meals = cursor.fetchall()
    conn.close()
    return meals


def get_meal_by_id(meal_id):
    """
    Return a single meal by its ID.
    Returns None if no meal is found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.name, m.price, m.category, s.name AS spot_name
        FROM meals m
        JOIN food_spots s ON m.spot_id = s.id
        WHERE m.id = ?
    """, (meal_id,))
    meal = cursor.fetchone()
    conn.close()
    return meal


def get_meals_by_spot(spot_id):
    """
    Return all meals from a specific food spot.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.name, m.price, m.category, s.name AS spot_name
        FROM meals m
        JOIN food_spots s ON m.spot_id = s.id
        WHERE m.spot_id = ?
        ORDER BY m.price
    """, (spot_id,))
    meals = cursor.fetchall()
    conn.close()
    return meals


def get_meals_within_budget(max_price):
    """
    Return all meals that cost at or below max_price.
    This is the core filtering function for the budget suggester.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.name, m.price, m.category, s.name AS spot_name
        FROM meals m
        JOIN food_spots s ON m.spot_id = s.id
        WHERE m.price <= ?
        ORDER BY m.price ASC
    """, (max_price,))
    meals = cursor.fetchall()
    conn.close()
    return meals


def get_meals_by_category(category):
    """
    Return all meals that match a given category.
    Categories: Rice, Noodles, Snack, Drink
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.name, m.price, m.category, s.name AS spot_name
        FROM meals m
        JOIN food_spots s ON m.spot_id = s.id
        WHERE LOWER(m.category) = LOWER(?)
        ORDER BY m.price
    """, (category,))
    meals = cursor.fetchall()
    conn.close()
    return meals


def search_meals(keyword):
    """
    Search meals by name using a keyword (partial match).
    Useful for when the user knows what they want but not where it's from.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.name, m.price, m.category, s.name AS spot_name
        FROM meals m
        JOIN food_spots s ON m.spot_id = s.id
        WHERE LOWER(m.name) LIKE LOWER(?)
        ORDER BY m.price
    """, (f"%{keyword}%",))
    meals = cursor.fetchall()
    conn.close()
    return meals

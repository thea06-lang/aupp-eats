import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_connection
from datetime import date


def log_meal(meal_id, price_paid, log_date=None):
    """
    Record a meal the user ate today (or on a given date).
    If log_date is not provided, defaults to today.
    Returns the ID of the new log entry.
    """
    if log_date is None:
        log_date = str(date.today())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO meal_logs (meal_id, log_date, price_paid)
        VALUES (?, ?, ?)
    """, (meal_id, log_date, price_paid))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_logs_by_date(log_date=None):
    """
    Return all meal logs for a specific date.
    Defaults to today if no date is given.
    Each row includes: log id, meal name, spot name, price paid, date.
    """
    if log_date is None:
        log_date = str(date.today())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.id, m.name AS meal_name, s.name AS spot_name,
               l.price_paid, l.log_date
        FROM meal_logs l
        JOIN meals m ON l.meal_id = m.id
        JOIN food_spots s ON m.spot_id = s.id
        WHERE l.log_date = ?
        ORDER BY l.id ASC
    """, (log_date,))
    logs = cursor.fetchall()
    conn.close()
    return logs


def get_total_spent_on_date(log_date=None):
    """
    Return the total amount spent on a given date.
    Defaults to today. Returns 0.0 if nothing was logged.
    """
    if log_date is None:
        log_date = str(date.today())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(price_paid), 0.0)
        FROM meal_logs
        WHERE log_date = ?
    """, (log_date,))
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_logs_by_week(start_date, end_date):
    """
    Return all meal logs between two dates (inclusive).
    Useful for the weekly spending summary.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.id, m.name AS meal_name, s.name AS spot_name,
               l.price_paid, l.log_date
        FROM meal_logs l
        JOIN meals m ON l.meal_id = m.id
        JOIN food_spots s ON m.spot_id = s.id
        WHERE l.log_date BETWEEN ? AND ?
        ORDER BY l.log_date ASC
    """, (start_date, end_date))
    logs = cursor.fetchall()
    conn.close()
    return logs


def get_most_logged_meals(limit=5):
    """
    Return the user's most frequently logged meals.
    This powers the 'your favorites' smart suggest feature.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.name AS meal_name, s.name AS spot_name,
               m.price, COUNT(l.id) AS times_ordered
        FROM meal_logs l
        JOIN meals m ON l.meal_id = m.id
        JOIN food_spots s ON m.spot_id = s.id
        GROUP BY m.id
        ORDER BY times_ordered DESC
        LIMIT ?
    """, (limit,))
    meals = cursor.fetchall()
    conn.close()
    return meals


def delete_log(log_id):
    """
    Remove a log entry by ID.
    Useful when the user makes a mistake logging a meal.
    Returns True if a row was deleted, False if the ID didn't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meal_logs WHERE id = ?", (log_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

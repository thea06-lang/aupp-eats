from colorama import Fore, Style
from datetime import date, timedelta


def get_int_input(prompt, min_val=None, max_val=None):
    """
    Ask the user for an integer.
    Keeps asking until a valid number within range is entered.
    Returns the integer, or None if the user types '0' or 'q' to cancel.
    """
    while True:
        try:
            raw = input(Fore.WHITE + Style.BRIGHT + f"  {prompt} ").strip()
            if raw.lower() in ("0", "q", ""):
                return None
            value = int(raw)
            if min_val is not None and value < min_val:
                print(Fore.RED + f"  ✘  Please enter a number of {min_val} or more.")
                continue
            if max_val is not None and value > max_val:
                print(Fore.RED + f"  ✘  Please enter a number of {max_val} or less.")
                continue
            return value
        except ValueError:
            print(Fore.RED + "  ✘  That's not a valid number. Try again.")


def get_float_input(prompt, min_val=0.0):
    """
    Ask the user for a decimal number (e.g. a price or budget).
    Keeps asking until a valid number is entered.
    """
    while True:
        try:
            raw = input(Fore.WHITE + Style.BRIGHT + f"  {prompt} ").strip()
            if raw.lower() in ("q", ""):
                return None
            value = float(raw)
            if value < min_val:
                print(Fore.RED + f"  ✘  Please enter a value of {min_val:.2f} or more.")
                continue
            return value
        except ValueError:
            print(Fore.RED + "  ✘  That's not a valid amount. Try again (e.g. 5.00).")


def get_week_range():
    """
    Return (start_date, end_date) as strings for the current week (Mon–Sun).
    """
    today = date.today()
    start = today - timedelta(days=today.weekday())   # Monday
    end   = start + timedelta(days=6)                  # Sunday
    return str(start), str(end)


def today_str():
    """Return today's date as a string (YYYY-MM-DD)."""
    return str(date.today())


def press_enter_to_continue():
    """Pause and wait for user to press Enter."""
    input(Fore.WHITE + Style.DIM + "\n  Press Enter to continue...")

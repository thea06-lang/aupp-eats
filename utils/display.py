from colorama import init, Fore, Back, Style

# Initialize colorama (works on Windows and Mac/Linux)
init(autoreset=True)

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
WIDTH = 52  # total terminal width for the app


# ─────────────────────────────────────────────
#  Layout Helpers
# ─────────────────────────────────────────────

def print_separator(char="─"):
    """Print a full-width divider line."""
    print(Fore.WHITE + Style.DIM + char * WIDTH)


def print_blank():
    """Print an empty line."""
    print()


def print_banner():
    """Print the AUPPeats app banner."""
    print_blank()
    print(Fore.CYAN + Style.BRIGHT + "█" * WIDTH)
    print(Fore.CYAN + Style.BRIGHT + "█" + " " * (WIDTH - 2) + "█")
    title = "🍜  AUPPeats"
    padding = (WIDTH - 2 - len(title)) // 2
    print(Fore.CYAN + Style.BRIGHT + "█" + " " * padding + title + " " * (WIDTH - 2 - padding - len(title)) + "█")
    subtitle = "Your campus meal budget tracker"
    padding2 = (WIDTH - 2 - len(subtitle)) // 2
    print(Fore.WHITE + "█" + " " * padding2 + subtitle + " " * (WIDTH - 2 - padding2 - len(subtitle)) + "█")
    print(Fore.CYAN + Style.BRIGHT + "█" * WIDTH)
    print_blank()


def print_header(title):
    """Print a section header."""
    print_blank()
    print(Fore.CYAN + Style.BRIGHT + f"  ╔  {title.upper()}")
    print_separator()


# ─────────────────────────────────────────────
#  Status Messages
# ─────────────────────────────────────────────

def print_success(message):
    """Green checkmark message for successful actions."""
    print(Fore.GREEN + Style.BRIGHT + f"  ✔  {message}")


def print_error(message):
    """Red X message for errors or invalid input."""
    print(Fore.RED + Style.BRIGHT + f"  ✘  {message}")


def print_warning(message):
    """Yellow warning message."""
    print(Fore.YELLOW + Style.BRIGHT + f"  ⚠  {message}")


def print_info(message):
    """Dim blue info message."""
    print(Fore.BLUE + f"  ℹ  {message}")


# ─────────────────────────────────────────────
#  Budget Display
# ─────────────────────────────────────────────

def print_budget_status(daily_budget, spent):
    """
    Show a color-coded budget bar and remaining amount.
    Green = healthy, Yellow = getting low, Red = over or nearly gone.
    """
    remaining = daily_budget - spent
    percent_used = (spent / daily_budget * 100) if daily_budget > 0 else 100

    print_header("Budget Status")

    # Color logic based on how much is left
    if percent_used >= 90:
        color = Fore.RED
        status = "DANGER — Almost out!"
    elif percent_used >= 60:
        color = Fore.YELLOW
        status = "Getting low"
    else:
        color = Fore.GREEN
        status = "Looking good"

    # Progress bar (20 blocks wide)
    bar_width = 20
    filled = int((percent_used / 100) * bar_width)
    filled = min(filled, bar_width)  # cap at max
    bar = "█" * filled + "░" * (bar_width - filled)

    print(f"  Daily Budget : {Fore.WHITE + Style.BRIGHT}${daily_budget:.2f}")
    print(f"  Spent        : {Fore.WHITE + Style.BRIGHT}${spent:.2f}")

    if remaining < 0:
        print(f"  Remaining    : {Fore.RED + Style.BRIGHT}${remaining:.2f}  (OVER BUDGET)")
    else:
        print(f"  Remaining    : {color + Style.BRIGHT}${remaining:.2f}")

    print(f"  [{color}{bar}{Style.RESET_ALL}]  {color}{status}")
    print_separator()


# ─────────────────────────────────────────────
#  Meal Display
# ─────────────────────────────────────────────

def print_meal_list(meals, show_index=True):
    """
    Print a formatted list of meals.
    meals: list of sqlite3.Row with keys — id, name, price, category, spot_name
    """
    if not meals:
        print_warning("No meals found.")
        return

    print(f"  {'#':<4} {'Meal':<28} {'Spot':<14} {'Price':>5}")
    print_separator()

    for i, meal in enumerate(meals, start=1):
        index = str(i) if show_index else " "
        name  = meal["name"][:27]
        spot  = meal["spot_name"][:13]
        price = f"${meal['price']:.2f}"

        # Color cheap meals green, pricier ones white
        if meal["price"] <= 1.00:
            color = Fore.GREEN
        elif meal["price"] <= 2.00:
            color = Fore.WHITE
        else:
            color = Fore.YELLOW

        print(f"  {Fore.CYAN}{index:<4}{color}{name:<28}{Style.DIM}{spot:<14}{Style.RESET_ALL + color}{price:>5}")

    print_separator()


def print_meal_detail(meal):
    """Print a single meal's full details."""
    print_blank()
    print(f"  {Fore.CYAN + Style.BRIGHT}{meal['name']}")
    print(f"  {Style.DIM}From: {meal['spot_name']}  |  Category: {meal['category']}")
    print(f"  {Fore.GREEN + Style.BRIGHT}Price: ${meal['price']:.2f}")
    print_separator()


# ─────────────────────────────────────────────
#  Spot Display
# ─────────────────────────────────────────────

def print_spot_list(spots):
    """Print a formatted list of food spots."""
    if not spots:
        print_warning("No food spots found.")
        return

    print(f"  {'#':<4} {'Name':<20} {'Location'}")
    print_separator()

    for i, spot in enumerate(spots, start=1):
        print(f"  {Fore.CYAN}{i:<4}{Fore.WHITE}{spot['name']:<20}{Style.DIM}{spot['location']}")

    print_separator()


# ─────────────────────────────────────────────
#  Log Display
# ─────────────────────────────────────────────

def print_log_list(logs):
    """Print today's meal log entries."""
    if not logs:
        print_info("Nothing logged yet today.")
        return

    print(f"  {'#':<4} {'Meal':<28} {'Paid':>6}")
    print_separator()

    for i, log in enumerate(logs, start=1):
        name = log["meal_name"][:27]
        paid = f"${log['price_paid']:.2f}"
        print(f"  {Fore.CYAN}{i:<4}{Fore.WHITE}{name:<28}{Fore.GREEN}{paid:>6}")

    print_separator()


def print_favorites(meals):
    """Print the user's most frequently ordered meals."""
    if not meals:
        print_info("No favorites yet — start logging meals!")
        return

    print(f"  {'#':<4} {'Meal':<28} {'Times':>5}  {'Price':>6}")
    print_separator()

    for i, meal in enumerate(meals, start=1):
        name  = meal["meal_name"][:27]
        times = str(meal["times_ordered"])
        price = f"${meal['price']:.2f}"
        print(f"  {Fore.CYAN}{i:<4}{Fore.WHITE}{name:<28}{Fore.YELLOW}{times:>5}  {Fore.GREEN}{price:>6}")

    print_separator()


# ─────────────────────────────────────────────
#  Menu Display
# ─────────────────────────────────────────────

def print_menu(title, options):
    """
    Print a numbered menu.
    options: list of strings e.g. ["View meals", "Log a meal", "Exit"]
    """
    print_header(title)
    for i, option in enumerate(options, start=1):
        print(f"  {Fore.CYAN + Style.BRIGHT}[{i}]{Style.RESET_ALL}  {option}")
    print_blank()
    print(Fore.WHITE + Style.DIM + "  Enter a number to continue: ", end="")


def print_weekly_summary(logs, start_date, end_date):
    """Print a spending summary for the week."""
    print_header(f"Week: {start_date} to {end_date}")

    if not logs:
        print_info("No meals logged this week.")
        return

    total = sum(log["price_paid"] for log in logs)

    for log in logs:
        date  = log["log_date"]
        meal  = log["meal_name"][:24]
        price = f"${log['price_paid']:.2f}"
        print(f"  {Style.DIM}{date}  {Style.RESET_ALL}{Fore.WHITE}{meal:<25}{Fore.GREEN}{price:>6}")

    print_separator()
    print(f"  {Fore.CYAN + Style.BRIGHT}Total spent this week: {Fore.GREEN + Style.BRIGHT}${total:.2f}")
    print_separator()

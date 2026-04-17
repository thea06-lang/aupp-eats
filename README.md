# 🍜 AUPPeats

> A terminal-based meal budget tracker built for students at the American University of Phnom Penh (AUPP).

---

## The Problem

AUPP students eat on tight budgets. Between the canteen, event stalls, and outside vendors, it's easy to lose track of what you've spent on food throughout the day — and end up broke before dinner.

AUPPeats solves that. Set your daily food budget, browse real meals from real campus spots, log what you eat, and always know exactly how much you have left.

---

## Demo

```
████████████████████████████████████████████████████
█                                                  █
█               🍜  AUPPeats                       █
█         Your campus meal budget tracker          █
████████████████████████████████████████████████████

  ╔  BUDGET STATUS
────────────────────────────────────────────────────
  Daily Budget : $5.00
  Spent        : $2.50
  Remaining    : $2.50
  [██████████░░░░░░░░░░]  Looking good
────────────────────────────────────────────────────

  ╔  MAIN MENU
────────────────────────────────────────────────────
  [1]  Browse meals
  [2]  Log a meal
  [3]  View budget & today's log
  [4]  Weekly summary
  [5]  My favorites
  [6]  Exit
```

---

## Features

- **Daily budget tracker** — set how much you want to spend, see it update in real time
- **Color-coded budget bar** — green when you're fine, yellow when it's getting low, red when you're close to the edge
- **Meal browser** — filter by spot, category (Rice / Noodles / Snack / Drink), remaining budget, or keyword search
- **Meal logger** — log what you ate with a single keypress; warns you before you go over budget
- **Today's log** — see everything you've eaten today and remove mistakes
- **Weekly summary** — full spending history from Monday to Sunday
- **Favorites tracker** — tracks your most ordered meals over time

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Language   | Python 3                |
| Database   | SQLite 3 (via `sqlite3` built-in) |
| Styling    | `colorama` for terminal colors |
| Storage    | Local `.db` file        |

No frameworks. No external APIs. Just clean Python.

---

## Project Structure

```
aupp-eats/
├── main.py              ← entry point — run this
├── database.py          ← DB connection and table setup
├── models/
│   ├── meal.py          ← meal queries (filter, search, budget)
│   ├── spot.py          ← food spot queries
│   └── log.py           ← meal logging and spending history
├── utils/
│   ├── display.py       ← terminal colors and formatted output
│   └── helpers.py       ← input validation and date utilities
├── data/
│   └── seed.py          ← pre-loads AUPP food spots and meals
├── requirements.txt
└── README.md
```

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/your-username/aupp-eats.git
cd aupp-eats
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
python main.py
```

That's it. The database is created and seeded automatically on first run.

---

## Database Schema

```
food_spots   id | name | location | description
meals        id | spot_id | name | price | category
budget       id | daily_amount | set_date
meal_logs    id | meal_id | log_date | price_paid
```

`meals.spot_id` → `food_spots.id`  
`meal_logs.meal_id` → `meals.id`

---

## Design Decisions

**Why SQLite?** It's serverless, zero-config, and ships with Python. Perfect for a local-first app with no need for network access.

**Why a CLI instead of a GUI?** The terminal forces you to think clearly about data flow and user experience without relying on visual shortcuts. Every piece of information on screen has to earn its place.

**Why separate models from display logic?** So the database queries stay reusable and testable, completely independent from how the output looks. Changing the UI never touches the data layer.

---

## Author

**Nou Sokunthea**  
AI Major — American University of Phnom Penh  
COS 111: Computer Science Survey  
Lecturer: Dr. HAS Sothea

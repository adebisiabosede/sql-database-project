import random
import sqlite3
from datetime import date, datetime

from faker import Faker

# register adapters for datetime and date
# store Python datetime objects as ISO strings
sqlite3.register_adapter(datetime, lambda d: d.isoformat(" "))
sqlite3.register_adapter(date, lambda d: d.isoformat())
#
sqlite3.register_converter("DATETIME", lambda s: datetime.fromisoformat(s.decode()))
sqlite3.register_converter("DATE", lambda s: date.fromisoformat(s.decode()))

fake = Faker()

DB_FILE = "data.db"

conn = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()


# helper functions to insert data into each tables
# which also add 2 to 5 percent missing and duplicate values per table
def insert_customers(n):
    customers = []
    for _ in range(n):
        # miss customer emails can cause due to incomplete registration
        email = fake.unique.email() if random.random() > 0.03 else None

        # 2 percent chance of reused name
        name = fake.name()
        if random.random() < 0.02:
            name = random.choice(customers)[0] if customers else name

        membership_level = (
            random.choice(["Bronze", "Silver", "Gold"])
            if random.random() > 0.02
            else None
        )
        signup_year = fake.year() if random.random() > 0.02 else None
        customers.append(
            (
                name,
                email,
                membership_level,
                signup_year,
                random.randint(0, 100),
                datetime.now(),
                datetime.now(),
            )
        )
    cursor.executemany(
        """
        INSERT INTO
            Customers (
                name,
                email,
                membership_level,
                signup_year,
                total_orders,
                created_at,
                updated_at
            )
        VALUES
            (?, ?, ?, ?, ?, ?, ?)
        """,
        customers,
    )
    conn.commit()

    print(f"{n} customers as been inserted")


def insert_restaurants(n):
    restaurants = []
    cuisines = ["Italian", "Chinese", "Mexican", "Indian", "American", "Japanese"]
    for _ in range(n):
        name = fake.company()
        # duplicate restaurant names
        if random.random() < 0.03 and restaurants:
            name = random.choice(restaurants)[0]

        rating = random.randint(1, 5) if random.random() > 0.05 else None
        avg_price = round(random.uniform(5, 50), 2) if random.random() > 0.03 else None
        restaurants.append(
            (
                name,
                random.choice(cuisines),
                rating,
                fake.year(),
                avg_price,
                datetime.now(),
                datetime.now(),
            )
        )
    cursor.executemany(
        """
        INSERT INTO
            Restaurants (
                name,
                cuisine_type,
                rating,
                established_year,
                avg_price,
                created_at,
                updated_at
            )
        VALUES
            (?, ?, ?, ?, ?, ?, ?)
        """,
        restaurants,
    )
    conn.commit()

    print(f"{n} restaurants has been inserted")


def insert_menu_items(n):
    cursor.execute("SELECT restaurant_id FROM Restaurants")
    restaurant_ids = [row[0] for row in cursor.fetchall()]
    items = []
    categories = ["Main", "Side", "Drink", "Dessert"]
    for _ in range(n):
        calories = random.randint(100, 800) if random.random() > 0.10 else None
        items.append(
            (
                random.choice(restaurant_ids),
                fake.word().capitalize(),
                random.choice(categories),
                round(random.uniform(3, 40), 2),
                calories,
                datetime.now(),
                datetime.now(),
            )
        )
    cursor.executemany(
        """
        INSERT INTO
            MenuItems (
                restaurant_id,
                name,
                category,
                price,
                calories,
                created_at,
                updated_at
            )
        VALUES
            (?, ?, ?, ?, ?, ?, ?)
        """,
        items,
    )
    conn.commit()

    print(f"create {n} menu items")


def insert_orders(n):
    cursor.execute("SELECT customer_id FROM Customers")
    customer_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT item_id, price FROM MenuItems")
    items = cursor.fetchall()
    orders = []
    for _ in range(n):
        delivery_time = random.randint(10, 60) if random.random() > 0.05 else None
        item_id, price = random.choice(items)
        quantity = random.randint(1, 5)
        total_amount = round(price * quantity, 2)
        orders.append(
            (
                random.choice(customer_ids),
                item_id,
                quantity,
                fake.date_this_year(),
                delivery_time,
                total_amount,
                datetime.now(),
                datetime.now(),
            )
        )
    # duplicate last row, to repeat last order
    orders.append(orders[-1])

    cursor.executemany(
        """
        INSERT INTO
            Orders (
                customer_id,
                item_id,
                quantity,
                order_date,
                delivery_time,
                total_amount,
                created_at,
                updated_at
            )
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        orders,
    )
    conn.commit()

    print(f"{n} orders insert")


if __name__ == "__main__":
    # populate the tables with fake data
    insert_customers(1000)
    insert_restaurants(100)
    insert_menu_items(500)
    insert_orders(1000)

    print("all fake data has been generated successfully")

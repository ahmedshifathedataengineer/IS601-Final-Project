import sqlite3
import json

DB_FILE = "db.sqlite"
JSON_FILE = "example_orders.json"

def initialize_schema():
    """Initialize the database schema."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY,
            name CHAR(64) NOT NULL,
            phone CHAR(10) NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY,
            name CHAR(64) NOT NULL,
            price REAL NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cust_id INT NOT NULL,
            notes TEXT,
            FOREIGN KEY(cust_id) REFERENCES customers(id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS item_list(
            order_id INT NOT NULL,
            item_id INT NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        );
        """)
        print("Database schema initialized.")

def populate_database():
    """Populate the database with data from the JSON file."""
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        return

    customers = {}
    items = {}

    # Extract customers and items
    for order in data:
        customers[order['phone']] = order['name']
        for item in order['items']:
            items[item['name']] = item['price']

    # Insert data into tables
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        for phone, name in customers.items():
            cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (name, phone))
        
        for name, price in items.items():
            cursor.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, price))
        
        for order in data:
            cust_id = cursor.execute("SELECT id FROM customers WHERE phone=?;", (order['phone'],)).fetchone()[0]
            cursor.execute("INSERT INTO orders (timestamp, cust_id, notes) VALUES (?, ?, ?);",
                           (order['timestamp'], cust_id, order.get('notes')))
            order_id = cursor.lastrowid
            for item in order['items']:
                item_id = cursor.execute("SELECT id FROM items WHERE name=?;", (item['name'],)).fetchone()[0]
                cursor.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?);", (order_id, item_id))
        conn.commit()
        print("Database populated successfully.")

if __name__ == "__main__":
    initialize_schema()
    populate_database()

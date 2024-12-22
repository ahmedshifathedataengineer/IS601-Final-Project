from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

# Initialize the FastAPI app
app = FastAPI()

# ----------------
# Data Models
# ----------------
class Customer(BaseModel):
    """
    Data model representing a customer.

    Attributes:
    - name (str): The name of the customer.
    - phone (str): The phone number of the customer.
    """
    name: str
    phone: str

class Item(BaseModel):
    """
    Data model representing an item.

    Attributes:
    - name (str): The name of the item.
    - price (float): The price of the item.
    """
    name: str
    price: float

class Order(BaseModel):
    """
    Data model representing an order.

    Attributes:
    - customer_id (int): The ID of the customer placing the order.
    - item_id (int): The ID of the item being ordered.
    - quantity (int): The quantity of the item being ordered.
    """
    customer_id: int
    item_id: int
    quantity: int

class BulkOrder(BaseModel):
    """
    Data model for a bulk order containing multiple items.

    Attributes:
    - items (List[Order]): A list of orders, each containing customer ID, item ID, and quantity.
    """
    items: List[Order]

# ----------------
# Utility Function
# ----------------
def get_db_connection():
    """
    Establish and return a connection to the SQLite database.

    Returns:
    - sqlite3.Connection: A connection object to interact with the database.
    """
    return sqlite3.connect("db.sqlite")

# ----------------
# Customers Endpoints
# ----------------
@app.post("/customers")
def create_customer(customer: Customer):
    """
    Create a new customer in the database.

    Request Body:
    - name (str): Customer's name.
    - phone (str): Customer's phone number.

    Returns:
    - A JSON object containing the created customer's ID, name, and phone.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (customer.name, customer.phone))
    con.commit()
    customer_id = cur.lastrowid
    con.close()
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.get("/customers/{customer_id}")
def read_customer(customer_id: int):
    """
    Retrieve a customer's details by their ID.

    Path Parameter:
    - customer_id (int): The ID of the customer to retrieve.

    Returns:
    - A JSON object containing the customer's ID, name, and phone if found.
    - 404 error if the customer is not found.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM customers WHERE id=?;", (customer_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return {"id": row[0], "name": row[1], "phone": row[2]}
    raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    """
    Update an existing customer's details.

    Path Parameter:
    - customer_id (int): The ID of the customer to update.

    Request Body:
    - name (str): Updated customer name.
    - phone (str): Updated customer phone number.

    Returns:
    - A JSON object containing the updated customer's details.
    - 404 error if the customer is not found.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("UPDATE customers SET name = ?, phone = ? WHERE id=?;", (customer.name, customer.phone, customer_id))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    """
    Delete a customer by their ID.

    Path Parameter:
    - customer_id (int): The ID of the customer to delete.

    Returns:
    - A success message if the customer is deleted.
    - 404 error if the customer is not found.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM customers WHERE id=?;", (customer_id,))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

# ----------------
# Items Endpoints
# ----------------
@app.post("/items")
def create_item(item: Item):
    """
    Create a new item in the database.

    Request Body:
    - name (str): The name of the item.
    - price (float): The price of the item.

    Returns:
    - A JSON object containing the created item's ID, name, and price.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO items (name, price) VALUES (?, ?);", (item.name, item.price))
    con.commit()
    item_id = cur.lastrowid
    con.close()
    return {"id": item_id, "name": item.name, "price": item.price}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Retrieve an item's details by its ID.

    Path Parameter:
    - item_id (int): The ID of the item to retrieve.

    Returns:
    - A JSON object containing the item's ID, name, and price if found.
    - 404 error if the item is not found.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM items WHERE id=?;", (item_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return {"id": row[0], "name": row[1], "price": row[2]}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    Update an existing item's details.

    Path Parameter:
    - item_id (int): The ID of the item to update.

    Request Body:
    - name (str): Updated name of the item.
    - price (float): Updated price of the item.

    Returns:
    - A JSON object containing the updated item's details.
    - 404 error if the item is not found.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("UPDATE items SET name = ?, price = ? WHERE id=?;", (item.name, item.price, item_id))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "name": item.name, "price": item.price}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    Delete an item by its ID.

    Path Parameter:
    - item_id (int): The ID of the item to delete.

    Returns:
    - A success message if the item is deleted.
    - 404 error if the item is not found.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM items WHERE id=?;", (item_id,))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# ----------------
# Orders Endpoints
# ----------------
@app.post("/orders")
def create_order(order: Order):
    """
    Create a new order in the database.

    Request Body:
    - customer_id (int): ID of the customer placing the order.
    - item_id (int): ID of the item being ordered.
    - quantity (int): Quantity of the item being ordered.

    Returns:
    - A JSON object containing the created order's details.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?);", 
                (order.customer_id, order.item_id, order.quantity))
    con.commit()
    order_id = cur.lastrowid
    con.close()
    return {"id": order_id, "customer_id": order.customer_id, "item_id": order.item_id, "quantity": order.quantity}

@app.get("/orders/{order_id}")
def read_order(order_id: int):
    """
    Retrieve an order's details by its ID.

    Path Parameter:
    - order_id (int): The ID of the order to retrieve.

    Returns:
    - A JSON object containing the order's details, including customer name, item name, and quantity if found.
    - 404 error if the order is not found.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT o.id, c.name AS customer_name, i.name AS item_name, o.quantity
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        JOIN items i ON o.item_id = i.id
        WHERE o.id=?;
    """, (order_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return {"id": row[0], "customer_name": row[1], "item_name": row[2], "quantity": row[3]}
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    """
    Delete an order by its ID.

    Path Parameter:
    - order_id (int): The ID of the order to delete.

    Returns:
    - A success message if the order is deleted.
    - 404 error if the order is not found.
    """
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM orders WHERE id=?;", (order_id,))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

# ----------------
# Bulk Orders Endpoint
# ----------------
@app.post("/orders/bulk")
def create_bulk_order(bulk_order: BulkOrder):
    """
    Create multiple orders in a single request.

    Request Body:
    - items (List[Order]): A list of orders, each containing:
      - customer_id (int): ID of the customer placing the order.
      - item_id (int): ID of the item being ordered.
      - quantity (int): Quantity of the item being ordered.

    Returns:
    - A success message indicating the number of items in the bulk order.
    """
    con = get_db_connection()
    cur = con.cursor()
    for order in bulk_order.items:
        cur.execute("INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?);",
                    (order.customer_id, order.item_id, order.quantity))
    con.commit()
    con.close()
    return {"message": f"Bulk order created with {len(bulk_order.items)} items"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

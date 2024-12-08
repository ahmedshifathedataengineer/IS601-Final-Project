from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Models for request validation
class Customer(BaseModel):
    name: str
    phone: str

class Item(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    customer_id: int
    item_id: int
    quantity: int

# -------------------
# Customers Endpoints
# -------------------
@app.post("/customers")
def create_customer(customer: Customer):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (customer.name, customer.phone))
    con.commit()
    customer_id = cur.lastrowid
    con.close()
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.get("/customers/{customer_id}")
def read_customer(customer_id: int):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("SELECT * FROM customers WHERE id = ?;", (customer_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return {"id": row[0], "name": row[1], "phone": row[2]}
    raise HTTPException(status_code=404, detail="Customer not found")

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?;", (customer.name, customer.phone, customer_id))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("DELETE FROM customers WHERE id = ?;", (customer_id,))
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
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("INSERT INTO items (name, price) VALUES (?, ?);", (item.name, item.price))
    con.commit()
    item_id = cur.lastrowid
    con.close()
    return {"id": item_id, "name": item.name, "price": item.price}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("SELECT * FROM items WHERE id = ?;", (item_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return {"id": row[0], "name": row[1], "price": row[2]}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("UPDATE items SET name = ?, price = ? WHERE id = ?;", (item.name, item.price, item_id))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "name": item.name, "price": item.price}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("DELETE FROM items WHERE id = ?;", (item_id,))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# -----------------
# Orders Endpoints
# -----------------
@app.post("/orders")
def create_order(order: Order):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("INSERT INTO orders (customer_id, item_id, quantity) VALUES (?, ?, ?);", 
                (order.customer_id, order.item_id, order.quantity))
    con.commit()
    order_id = cur.lastrowid
    con.close()
    return {"id": order_id, "customer_id": order.customer_id, "item_id": order.item_id, "quantity": order.quantity}

@app.get("/orders/{order_id}")
def read_order(order_id: int):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?;", (order_id,))
    row = cur.fetchone()
    con.close()
    if row:
        return {"id": row[0], "customer_id": row[1], "item_id": row[2], "notes": row[3]}
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("UPDATE orders SET customer_id = ?, item_id = ?, quantity = ? WHERE id = ?;", 
                (order.customer_id, order.item_id, order.quantity, order_id))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"id": order_id, "customer_id": order.customer_id, "item_id": order.item_id, "quantity": order.quantity}

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()
    cur.execute("DELETE FROM orders WHERE id = ?;", (order_id,))
    con.commit()
    con.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

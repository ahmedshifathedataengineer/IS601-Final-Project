FastAPI SQLite CRUD Application
This is a FastAPI project that provides a RESTful API for managing customers, items, and orders using an SQLite database. The API supports basic CRUD (Create, Read, Update, Delete) operations and includes bulk order functionality.

Features
Customers API: Manage customer details (create, retrieve, update, delete).
Items API: Manage item details (create, retrieve, update, delete).
Orders API:
Create and retrieve individual orders.
Delete an order by its ID.
Create multiple orders in a single request (bulk order).
Auto-generated interactive documentation with Swagger UI and ReDoc.
Built-in SQLite database for easy setup and storage.
Requirements
Python 3.9+
FastAPI
Uvicorn (ASGI server)
SQLite (built into Python)
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/fastapi-sqlite-crud.git
cd fastapi-sqlite-crud
Set up a virtual environment (optional):

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
Install dependencies:

bash
Copy code
pip install fastapi uvicorn
Run the application:

bash
Copy code
python main.py
Alternatively, use Uvicorn directly:

bash
Copy code
uvicorn main:app --reload
Open your browser and navigate to:

http://127.0.0.1:8000/docs: Swagger UI.
http://127.0.0.1:8000/redoc: ReDoc.
Endpoints
Customers API
Create a customer: POST /customers

Request Body:
json
Copy code
{
  "name": "John Doe",
  "phone": "123-456-7890"
}
Response:
json
Copy code
{
  "id": 1,
  "name": "John Doe",
  "phone": "123-456-7890"
}
Get a customer by ID: GET /customers/{customer_id}

Update a customer: PUT /customers/{customer_id}

Delete a customer: DELETE /customers/{customer_id}

Items API
Create an item: POST /items

Request Body:
json
Copy code
{
  "name": "Laptop",
  "price": 1500.0
}
Response:
json
Copy code
{
  "id": 1,
  "name": "Laptop",
  "price": 1500.0
}
Get an item by ID: GET /items/{item_id}

Update an item: PUT /items/{item_id}

Delete an item: DELETE /items/{item_id}

Orders API
Create an order: POST /orders

Request Body:
json
Copy code
{
  "customer_id": 1,
  "item_id": 1,
  "quantity": 2
}
Response:
json
Copy code
{
  "id": 1,
  "customer_id": 1,
  "item_id": 1,
  "quantity": 2
}
Get an order by ID: GET /orders/{order_id}

Response:
json
Copy code
{
  "id": 1,
  "customer_name": "John Doe",
  "item_name": "Laptop",
  "quantity": 2
}
Delete an order: DELETE /orders/{order_id}

Bulk Orders API
Create multiple orders: POST /orders/bulk
Request Body:
json
Copy code
{
  "items": [
    {"customer_id": 1, "item_id": 1, "quantity": 2},
    {"customer_id": 2, "item_id": 3, "quantity": 1}
  ]
}
Response:
json
Copy code
{
  "message": "Bulk order created with 2 items"
}
Project Structure
graphql
Copy code
fastapi-sqlite-crud/
├── main.py           # Main FastAPI application
├── db.sqlite         # SQLite database file (auto-created on first run)
├── README.md         # Project documentation
Future Improvements
Add unit tests for endpoints using pytest.
Add authentication and authorization (e.g., OAuth2 or JWT).
Deploy to a cloud provider like AWS, GCP, or Azure.
Expand the database schema for more complex relationships (e.g., order statuses, user accounts).
Contributing
Fork the repository.
Create a new branch for your feature (git checkout -b feature-name).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-name).
Open a pull request.
License
This project is licensed under the MIT License. See LICENSE for more details.

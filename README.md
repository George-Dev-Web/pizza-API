# 🍕 Pizza Restaurant API

This is a RESTful API for a fictional pizza restaurant. It allows users to interact with data for:

* Pizzas
* Restaurants
* Restaurant-Pizza associations (which restaurants serve which pizzas and at what price)

Built with Flask, SQLAlchemy, Flask-Migrate, and PostgreSQL.

---

## 📁 Project Structure

```
pizza-API/
├── server/
│   ├── app.py                # App factory
│   ├── config.py             # Configuration
│   ├── models/
│   │   ├── __init__.py       # Imports all models
│   │   ├── pizza.py
│   │   ├── restaurant.py
│   │   └── restaurant_pizza.py
│   ├── controllers/
│   │   ├── pizza_controller.py
│   │   ├── restaurant_controller.py
│   │   └── restaurant_pizza_controller.py
├── migrations/               # Alembic migrations
├── instance/
│   └── config.py             # Local DB config
├── Pipfile & Pipfile.lock    # Dependencies
├── README.md                 # You're here :)
```

---

## ⚙️ Setup Instructions

### 1. **Clone the repository**

```bash
git clone <your-repo-url>
cd pizza-API
```

### 2. **Create a virtual environment**

```bash
pipenv shell
```

### 3. **Install dependencies**

```bash
pipenv install
```

### 4. **Set environment variables**

```bash
export FLASK_APP=server.app:create_app
export FLASK_ENV=development
```

### 5. **Database setup (PostgreSQL)**

Make sure PostgreSQL is running.

#### a. Create a PostgreSQL database

```bash
sudo -u postgres psql
CREATE DATABASE pizza_db;
\q
```

#### b. Set up the `Config` class in `server/config.py`

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:<your_password>@localhost/pizza_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 6. **Run database migrations**

```bash
flask db init   # Only once if not already run
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. **Run the server**

```bash
flask run
```

Server will start at: `http://127.0.0.1:5000`

---

## 🧪 API Endpoints

### 📦 Pizzas

* `GET /pizzas/` → List all pizzas
* `POST /pizzas/` → Create new pizza
* `DELETE /pizzas/<id>` → Delete pizza

### 🏬 Restaurants

* `GET /restaurants/` → List all restaurants
* `GET /restaurants/<id>` → Get restaurant by ID
* `POST /restaurants/` → Create new restaurant
* `DELETE /restaurants/<id>` → Delete restaurant

### 🍽️ Restaurant Pizzas

* `POST /restaurant_pizzas/` → Associate a pizza with a restaurant

Request JSON:

```json
{
  "restaurant_id": 1,
  "pizza_id": 2,
  "price": 13.99
}
```

---

## 📬 Postman Setup

If you're new to Postman:

1. Open Postman
2. Import the provided `pizza_api.postman_collection.json` file
3. Click `Collections` → select `Pizza API` → click `Run`

We'll generate these JSON files in the next steps.

---

## 🔧 Common Issues

* **404 Not Found**: Check if you're using the correct endpoint (trailing slashes matter).
* **500 Internal Server Error**: Likely a missing table → run migrations.
* **psycopg2.errors.UndefinedTable**: Run `flask db upgrade` to create tables.
* **Cannot connect to DB**: Ensure PostgreSQL is running and credentials in `config.py` are correct.

---

## 👷‍♂️ Contributing

If you want to extend this API:

* Add new models to `server/models/`
* Add new routes to `server/controllers/`
* Run `flask db migrate` and `flask db upgrade`

---

## 📘 License

MIT License

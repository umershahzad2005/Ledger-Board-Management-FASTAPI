# 📊 Ledger Board - Management & Accounting API

A robust, production-ready REST API built with **FastAPI**, **SQLAlchemy**, and **Pydantic v2**. This application provides an all-in-one ledger and business management solution featuring **Role-Based JWT Authentication**, **Vendor Ledger**, **Customer Ledger**, **Inventory Tracking**, and **Real-Time Financial Reports**.

---

## 🚀 Key Features

* **🔐 User Authentication & RBAC (Admin & User Roles)**
  * Secure password hashing with `bcrypt`.
  * Stateless token authentication with `PyJWT`.
  * Role-based access control (`admin` vs. `user`) with dependency-based protection (`require_admin`).
  * Direct integration with Swagger UI's built-in **Authorize** button (OAuth2 Password Flow).

* **🏢 Vendor Management & Ledger**
  * Record vendors with contact information and trade roles.
  * Track purchases and payments with running balance calculations.
  * Automatic total calculation from `no_of_units * per_unit_price`.

* **👥 Customer Management & Ledger**
  * Maintain customer profiles and records.
  * Record customer purchases and payments.
  * Real-time outstanding customer receivable balance calculation.

* **📦 Inventory Management**
  * Track product quantities, purchase costs, and selling prices.
  * Automatically import stock directly from vendor purchase transactions.
  * Automatic selling price margin calculation (10% default markup).

* **📈 Financial Reports & Analytics**
  * **Vendor Report (`/reports/vendors`)**: Total purchases, total payments, and outstanding payables.
  * **Customer Report (`/reports/customers`)**: Total sales, total collections, and outstanding receivables.
  * **Inventory Report (`/reports/inventory`)**: Total stock valuation (purchase cost vs. potential sales value) and projected profits.
  * **Executive Summary (`/reports/summary`)**: High-level financial overview and net receivable/payable position.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
* **Server:** [Uvicorn](https://www.uvicorn.org/) (ASGI Web Server)
* **ORM & Database:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) with SQLite (configurable to PostgreSQL/MySQL)
* **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/)
* **Security:** `bcrypt` (password hashing) & `PyJWT` (JWT tokens)
* **Form Parsing:** `python-multipart` (OAuth2 support)

---

## 📋 Prerequisites

Before setting up, ensure you have the following installed on your machine:

* **Git**: [Download Git](https://git-scm.com/downloads)
* **Python 3.10 or higher**: [Download Python](https://www.python.org/downloads/)
* **pip** (Python package installer, usually bundled with Python)

Verify your installations in terminal/PowerShell:
```bash
git --version
python --version
```

---

## ⚙️ A to Z Installation & Setup Guide

Follow these exact steps to clone, configure, and run the project from scratch.

### Step 1: Clone the Repository
Open your terminal (PowerShell, Command Prompt, or Bash) and run:
```bash
git clone https://github.com/umershahzad2005/Ledger-Board-Management-FASTAPI.git
cd Ledger-Board-Management-FASTAPI
```

### Step 2: Switch to the Working Branch
If you are working on the `login` branch, check it out:
```bash
git checkout login
```

### Step 3: Create a Virtual Environment
Isolating dependencies in a virtual environment prevents conflicts with system packages.

* **On Windows (PowerShell / Command Prompt):**
  ```bash
  python -m venv venv
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  ```

### Step 4: Activate the Virtual Environment
* **On Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If you get a script execution policy error, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

* **On Windows (Command Prompt `cmd`):**
  ```cmd
  venv\Scripts\activate.bat
  ```

* **On macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

*(When active, your terminal prompt will show `(venv)` at the beginning).*

### Step 5: Install Project Dependencies
Upgrade `pip` and install all required libraries from `requirements.txt`:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: (Optional) Configure Environment Variables
By default, the application runs out-of-the-box using a local SQLite database (`ledger.db`) and a built-in secret key.

If you wish to configure custom settings, you can set environment variables:
```bash
# Optional custom database URL (e.g., PostgreSQL):
export DATABASE_URL="sqlite:///./ledger.db"

# Optional custom secret key for JWT tokens:
export SECRET_KEY="your-custom-production-secret-key"
```

### Step 7: Run the FastAPI Server
Start the development server with live-reloading enabled:
```bash
uvicorn main:app --reload
```

You should see output similar to:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process using StatReload
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 📖 Interactive API Documentation

Once the server is running, open your web browser to test and explore the API:

* **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Alternative ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 How to Authenticate in Swagger UI

1. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2. First, register an admin or user under `POST /register`:
   ```json
   {
     "name": "Admin User",
     "email": "admin@example.com",
     "password": "adminsecret123",
     "role": "admin"
   }
   ```
3. Click the green **Authorize** 🔒 button at the top right of the Swagger page.
4. Fill in:
   * **`username`**: Enter your registered email (e.g., `admin@example.com`)
   * **`password`**: Enter your password (e.g., `adminsecret123`)
   * *(Leave `client_id` and `client_secret` blank)*
5. Click **Authorize** and then **Close**.
6. The lock icon is now closed! All protected requests (such as `GET /admin/users`) will automatically include your Bearer token.

---

## 🗂️ Complete API Reference

### 1. Authentication
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Public | Create a new user account with `admin` or `user` role |
| `POST` | `/login` | Public | Authenticate via email & password and receive JWT token |
| `GET` | `/admin/users` | **Admin Only** | List all registered system users |

### 2. Customers & Customer Ledger
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/customers` | Public | Create a new customer profile |
| `GET` | `/customers` | Public | List all customers |
| `GET` | `/customers/{id}` | Public | Get customer details with real-time balance calculation |
| `PUT` | `/customers/{id}` | Public | Update customer information |
| `DELETE` | `/customers/{id}` | Public | Delete a customer and their transaction history |
| `POST` | `/customers/{id}/transactions` | Public | Record customer purchase or payment |
| `GET` | `/customers/{id}/transactions` | Public | List all transactions for a specific customer |

### 3. Vendors & Vendor Ledger
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/vendors` | Public | Create a new vendor with role and contact number |
| `GET` | `/vendors` | Public | List all vendors |
| `GET` | `/vendor/{id}` | Public | Get vendor details with real-time balance calculation |
| `PUT` | `/vendor/{id}` | Public | Update vendor details |
| `DELETE` | `/vendor/{id}` | Public | Delete a vendor and their transaction history |
| `POST` | `/vendor/{id}/transactions` | Public | Record vendor purchase or payment |
| `GET` | `/vendor/{id}/transactions` | Public | List all transactions for a specific vendor |

### 4. Inventory
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/inventory` | Public | List all stock items |
| `GET` | `/inventory/{id}` | Public | Get single inventory item details |
| `POST` | `/inventory` | Public | Add new product to inventory manually |
| `PUT` | `/inventory/{id}` | Public | Update inventory item pricing or stock count |
| `DELETE` | `/inventory/{id}` | Public | Remove item from inventory |
| `GET` | `/inventory/transaction/{transaction_id}` | Public | Auto-add/update inventory stock directly from a vendor purchase |

### 5. Financial Reports
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/reports/summary` | Public | Executive dashboard: Vendor, Customer & Inventory summary |
| `GET` | `/reports/vendors` | Public | Total purchases, payments, and payable balances for all vendors |
| `GET` | `/reports/customers` | Public | Total sales, collections, and receivable balances for all customers |
| `GET` | `/reports/inventory` | Public | Stock quantities, inventory cost value, sales value, and projected profit |

---

## 🧪 Quick Walkthrough: Step-by-Step Testing Flow

Once your application is running, follow this quick business flow to test the system:

1. **Create a Vendor:**
   * `POST /vendors`
   * Body:
     ```json
     {
       "name": "ABC Cement Mills",
       "vendor_role": "Manufacturer",
       "contact_number": "+1234567890"
     }
     ```

2. **Add a Vendor Purchase Transaction:**
   * `POST /vendor/1/transactions`
   * Body:
     ```json
     {
       "transaction_type": "purchase",
       "product_name": "Cement Bag 50kg",
       "no_of_units": 100,
       "per_unit_price": 20.0,
       "description": "Batch #101 purchase"
     }
     ```
   *(Amount automatically calculates to 2,000.00).*

3. **Import Purchase Into Inventory:**
   * `GET /inventory/transaction/1`
   * Automatically adds 100 units of "Cement Bag 50kg" with purchase price 20.0 and default selling price 22.0 (10% markup).

4. **Record a Vendor Payment:**
   * `POST /vendor/1/transactions`
   * Body:
     ```json
     {
       "transaction_type": "payment",
       "amount": 1200.0,
       "description": "Partial payment via bank transfer"
     }
     ```
   * Calling `GET /vendor/1` now displays `remaining_amount: 800.0`.

5. **Create a Customer:**
   * `POST /customers`
   * Body:
     ```json
     {
       "name": "Modern Builders Inc",
       "phone": "+9876543210",
       "address": "456 Market St"
     }
     ```

6. **Record a Customer Purchase & Payment:**
   * `POST /customers/1/transactions` (Purchase):
     ```json
     {
       "transaction_type": "purchase",
       "product_name": "Cement Bag 50kg",
       "no_of_units": 40,
       "per_unit_price": 22.0,
       "description": "Site supply order"
     }
     ```
     *(Amount = 880.00)*
   * `POST /customers/1/transactions` (Payment):
     ```json
     {
       "transaction_type": "payment",
       "amount": 500.0,
       "description": "Cash deposit"
     }
     ```
   * Calling `GET /customers/1` now displays `remaining_amount: 380.0`.

7. **Generate Financial Reports:**
   * `GET /reports/summary`: Displays current accounts payable ($800.00), accounts receivable ($380.00), inventory valuation, and net balance.

---

## 📁 Project Directory Structure

```text
FastAPI-Ledger/
│
├── auth.py             # Password hashing (bcrypt), JWT generation, & RBAC dependencies
├── database.py         # SQLAlchemy engine, session maker, and Base setup
├── models.py           # Database models (User, Customer, CustomerTransaction, Vendor, VendorTransaction, Inventory)
├── schemas.py          # Pydantic validation schemas and report response models
├── main.py             # FastAPI entrypoint, route handlers, and startup hooks
├── requirements.txt    # Production dependency requirements
└── README.md           # Project documentation and setup instructions
```

---

## 💡 Troubleshooting & FAQ

* **Q: How do I reset the database to a clean state?**
  * Stop the server (`Ctrl + C`).
  * Delete `ledger.db` in the project root folder.
  * Start the server again (`uvicorn main:app --reload`). SQLAlchemy will automatically recreate fresh, clean tables.

* **Q: Why do I get a `422 Unprocessable Content` error in Swagger Authorize?**
  * Ensure you enter your email into the **`username`** field in the Swagger Authorize modal and leave `client_id` and `client_secret` blank.

* **Q: Script execution is disabled on Windows PowerShell?**
  * Open PowerShell as Administrator and run:
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

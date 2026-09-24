# 📊 Ledger Board - Management & Accounting API

A robust, production-ready REST API built with **FastAPI**, **SQLAlchemy**, and **Pydantic v2**. This application provides an all-in-one ledger and business management solution featuring **Role-Based JWT Authentication**, **Dedicated Vendor & Customer Purchase/Payment Endpoints**, **Inventory Tracking & Auto-Stock Deduction**, and **Real-Time Financial Reports**.

---

## 🚀 Key Features

* **🔐 User Authentication & RBAC (Admin & User Roles)**
  * Secure password hashing with `bcrypt`.
  * Stateless token authentication with `PyJWT` (HS256).
  * Role-based access control (`admin` vs. `user`) with dependency protection (`require_admin`).
  * Dedicated `POST /login` accepting clean JSON (`email` & `password`).
  * Direct integration with Swagger UI's green **Authorize** 🔒 button via **`HTTPBearer`** (paste token directly into the `Value` box).
  * Auto-seeded default administrator account (`admin@ledger.com` / `admin123`).

* **🏢 Vendor Management & Dedicated Ledger**
  * Create, view, update, and delete vendor profiles.
  * **Dedicated Purchase (`POST /vendor/{id}/purchase`)**: Amount is automatically calculated ($\text{no\_of\_units} \times \text{per\_unit\_price}$); no manual amount entry required. Clean response with zero payment null fields.
  * **Dedicated Payment (`POST /vendor/{id}/payment`)**: Supports payment methods (`cash`, `card`, `loan`) and optional transaction references. Live response immediately returns `total_paid` and `remaining_amount`.
  * **Vendor Ledger (`GET /vendors/{id}/ledger`)**: Full running ledger statement with total purchases, total payments, remaining balance, and itemized transaction list.

* **👥 Customer Management & Dedicated Ledger**
  * Create, view, update, and delete customer profiles.
  * **Dedicated Sale (`POST /customers/{id}/sale`)**: Amount auto-calculated from units and price. **Automatically checks and deducts stock from Inventory**. Clean response with zero payment null fields.
  * **Dedicated Payment (`POST /customers/{id}/payment`)**: Records customer payments (`cash`, `card`, `loan`) with reference. Live response returns `total_paid` and `remaining_amount`.
  * **Customer Ledger (`GET /customers/{id}/ledger`)**: Full customer ledger statement with real-time outstanding balances.

* **📦 Inventory Management**
  * Track product quantities, purchase costs, and selling prices.
  * Automatically import stock directly from vendor purchases (`GET /inventory/transaction/{id}`) with 10% default profit margin calculation.
  * Automatic stock validation & deduction when customers make a purchase.
  * Full manual CRUD operations on inventory items.

* **📈 Financial Reports & Analytics**
  * **Executive Summary (`/reports/summary`)**: High-level financial overview across vendors, customers, inventory stock value, and net balance position.
  * **Vendor Report (`/reports/vendors`)**: Aggregated total purchases, total payments, and outstanding payables.
  * **Customer Report (`/reports/customers`)**: Aggregated sales, collections, and outstanding receivables.
  * **Inventory Report (`/reports/inventory`)**: Stock quantities, total purchase valuation, projected selling value, and projected gross profit.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
* **Server:** [Uvicorn](https://www.uvicorn.org/) (ASGI Web Server)
* **ORM & Database:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) with SQLite (configurable to PostgreSQL/MySQL)
* **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/)
* **Security & Auth:** `bcrypt` (password hashing), `PyJWT` (JWT tokens), `HTTPBearer` (OpenAPI Bearer scheme)

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

## 🔐 How to Authenticate in Swagger UI (Step-by-Step)

By default, **all business APIs are locked 🔒** and require authentication. Only `/login` and `/` are public.

### 1. Default Admin Account (Auto-Seeded)
On application startup, a default administrator account is automatically created:
* **Email:** `admin@ledger.com`
* **Password:** `admin123`
* **Role:** `admin`

### 2. Unlocking Swagger UI APIs:
1. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2. Expand the `POST /login` endpoint and click **Try it out**.
3. In the Request body, enter the admin credentials:
   ```json
   {
     "email": "admin@ledger.com",
     "password": "admin123"
   }
   ```
4. Click **Execute**. The response body will return your JWT access token:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer",
     "role": "admin"
   }
   ```
5. **Copy** the `access_token` string (without quotes).
6. Scroll to the top right of the page and click the green **Authorize** 🔒 button.
7. In the popup dialog under **HTTPBearer (http, Bearer)**, paste your copied token into the **`Value:`** field:
   ```text
   Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
8. Click **Authorize**, then click **Close**.
9. All padlock icons (🔒) are now authenticated! All protected endpoints are ready to execute.

### 3. Creating Additional Staff Users (Admin Only)
Once authorized as Admin, you can provision accounts for staff members:
* Call `POST /admin/create-user`:
  ```json
  {
    "name": "Staff Member",
    "email": "staff@ledger.com",
    "password": "staffpassword123",
    "role": "user"
  }
  ```
* That user can now log in via `POST /login` with their credentials to access operational endpoints.

---

## 🗂️ Complete API Reference

### 1. Authentication & Admin
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/login` | **Public** | Login with email & password; returns JWT Bearer token |
| `POST` | `/admin/create-user` | **Admin Only** 🔒 | Provision new admin or user credentials |
| `GET` | `/admin/users` | **Admin Only** 🔒 | List all registered accounts |

### 2. Vendors & Vendor Ledger
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/vendors` | **Authenticated** 🔒 | Create a new vendor profile |
| `GET` | `/vendors` | **Authenticated** 🔒 | List all vendors |
| `GET` | `/vendor/{id}` | **Authenticated** 🔒 | Get single vendor details and current balance |
| `PUT` | `/vendor/{id}` | **Authenticated** 🔒 | Update vendor information |
| `DELETE` | `/vendor/{id}` | **Authenticated** 🔒 | Delete vendor and associated records |
| `POST` | `/vendor/{id}/purchase` | **Authenticated** 🔒 | Record purchase from vendor (auto-calculates amount) |
| `POST` | `/vendor/{id}/payment` | **Authenticated** 🔒 | Record payment to vendor (`cash`/`card`/`loan`); returns live `total_paid` & `remaining_amount` |
| `GET` | `/vendors/{id}/ledger` | **Authenticated** 🔒 | Complete vendor statement with totals and transaction history |

### 3. Customers & Customer Ledger
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/customers` | **Authenticated** 🔒 | Create a new customer profile |
| `GET` | `/customers` | **Authenticated** 🔒 | List all customers |
| `GET` | `/customers/{id}` | **Authenticated** 🔒 | Get single customer details and current balance |
| `PUT` | `/customers/{id}` | **Authenticated** 🔒 | Update customer information |
| `DELETE` | `/customers/{id}` | **Authenticated** 🔒 | Delete customer and associated records |
| `POST` | `/customers/{id}/sale` | **Authenticated** 🔒 | Sell product to customer (validates price/stock, auto-deducts inventory) |
| `POST` | `/customers/{id}/payment` | **Authenticated** 🔒 | Record payment from customer (`cash`/`card`/`loan`); returns live `total_paid` & `remaining_amount` |
| `GET` | `/customers/{id}/ledger` | **Authenticated** 🔒 | Complete customer statement with totals and transaction history |

### 4. Inventory Management
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/inventory` | **Authenticated** 🔒 | List all inventory items and quantities |
| `GET` | `/inventory/{id}` | **Authenticated** 🔒 | Get details of a single inventory item |
| `POST` | `/inventory` | **Authenticated** 🔒 | Manually add a new product to inventory |
| `PUT` | `/inventory/{id}` | **Authenticated** 🔒 | Update inventory pricing or stock quantity |
| `DELETE` | `/inventory/{id}` | **Authenticated** 🔒 | Remove item from inventory |

### 5. Financial Reports
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/reports/summary` | **Authenticated** 🔒 | Executive summary across vendors, customers, stock valuation, and net balance |
| `GET` | `/reports/vendors` | **Authenticated** 🔒 | Summary of total purchases, payments, and payable balances for all vendors |
| `GET` | `/reports/customers` | **Authenticated** 🔒 | Summary of total sales, payments, and receivable balances for all customers |
| `GET` | `/reports/inventory` | **Authenticated** 🔒 | Total stock units, cost valuation, sales valuation, and projected profit |

---

## 🧪 Quick Walkthrough: Step-by-Step Business Flow

Follow this end-to-end flow in Swagger UI to test the complete accounting and inventory cycle:

### 1. Authenticate in Swagger
* Call `POST /login` with:
  ```json
  {
    "email": "admin@ledger.com",
    "password": "admin123"
  }
  ```
* Copy the returned `access_token`.
* Click the green **Authorize** 🔒 button at the top right, paste the token into **`Value:`**, and click **Authorize** → **Close**.

### 2. Create a Vendor
* `POST /vendors`
  ```json
  {
    "name": "ABC Wholesalers",
    "vendor_role": "Supplier",
    "contact_number": "+1234567890"
  }
  ```

### 3. Record a Vendor Purchase (Auto Restocks Inventory)
* `POST /vendor/1/purchase`
  ```json
  {
    "product_name": "iPhone 15",
    "no_of_units": 10,
    "per_unit_price": 800.0,
    "paid_amount": 0,
    "payment_method": "loan",
    "description": "Stock order #101"
  }
  ```
  *(Total amount is automatically calculated to $8,000.00; this purchase **automatically adds 10 units of "iPhone 15" to Inventory**).*

### 4. Verify Stock in Inventory
* `GET /inventory`
  * Displays 10 units of "iPhone 15" in stock with purchase price 800.0.

### 5. Make a Vendor Payment
* `POST /vendor/1/payment`
  ```json
  {
    "amount": 5000.0,
    "payment_method": "card",
    "payment_reference": "card ending in 4762",
    "description": "Paid initial advance via company debit card"
  }
  ```
  * Response immediately reports `total_paid: 5000.0` and `remaining_amount: 3000.0`.

### 6. Create a Customer
* `POST /customers`
  ```json
  {
    "name": "Modern Retailers",
    "phone": "+9876543210",
    "address": "789 Commercial Ave"
  }
  ```

### 7. Sell to Customer (Auto Stock Deduction)
* `POST /customers/1/sale`
  ```json
  {
    "product_name": "iPhone 15",
    "no_of_units": 3,
    "per_unit_price": 950.0,
    "received_amount": 0,
    "payment_method": "loan",
    "description": "Customer order #SO-50"
  }
  ```
  * Total amount calculates to $2,850.00.
  * System validates that selling price ($950) is not lower than buying cost ($800).
  * Inventory stock for "iPhone 15" automatically drops from 10 to 7 units!

### 8. Record Customer Payment
* `POST /customers/1/payment`
  ```json
  {
    "amount": 2000.0,
    "payment_method": "cash",
    "payment_reference": "Receipt #REC-101",
    "description": "Cash on delivery"
  }
  ```
  * Response confirms `total_paid: 2000.0` and `remaining_amount: 850.0`.

### 9. Check Statements & Reports
* `GET /vendors/1/ledger`: Full vendor statement with purchases, payments, and remaining payable balance ($3,000.00).
* `GET /customers/1/ledger`: Full customer statement with purchases, collections, and remaining receivable balance ($850.00).
* `GET /reports/summary`: Complete executive dashboard displaying net receivables/payables and stock valuations.

---

## 📁 Project Directory Structure

```text
FastAPI-Ledger/
│
├── auth.py             # HTTPBearer auth, bcrypt hashing, JWT decode/encode & RBAC
├── database.py         # SQLAlchemy engine, session maker, and Base declarative setup
├── models.py           # Database models (User, Customer, Vendor, Inventory, Transactions)
├── schemas.py          # Pydantic v2 schemas, dedicated purchase/payment models & reports
├── main.py             # FastAPI application, route handlers, and default admin seeding
├── requirements.txt    # Production dependency requirements
└── README.md           # Project documentation and setup instructions
```

---

## 💡 Troubleshooting & FAQ

* **Q: How do I authorize in Swagger UI?**
  * Call `POST /login` with your email and password (`admin@ledger.com` / `admin123`).
  * Copy the `access_token` value from the response body.
  * Click the green **Authorize** 🔒 button at the top right of the Swagger UI page.
  * Paste your token into the **`Value:`** field and click **Authorize**.

* **Q: Why does my customer purchase fail with "Not enough stock"?**
  * Customer purchases automatically validate and deduct stock from Inventory.
  * Ensure the product exists in Inventory with sufficient stock before selling, or add stock via `GET /inventory/transaction/{id}` or `POST /inventory`.

* **Q: How do I reset the database to a fresh state?**
  * Stop the server (`Ctrl + C`).
  * Delete the `ledger.db` file in the project folder.
  * Restart the server (`uvicorn main:app --reload`). SQLAlchemy will recreate fresh tables and automatically seed the default admin account.

* **Q: Script execution is disabled on Windows PowerShell?**
  * Open PowerShell as Administrator and run:
    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

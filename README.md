# 🛒 Ecommerce Backend API

A production-style Ecommerce Backend built using Django and Django REST Framework. This project provides REST APIs for user authentication, product management, cart, wishlist, orders, payments, shipping, coupons, and notifications. It follows a modular architecture where each feature is organized into a separate Django app, making the project clean, scalable, and easy to maintain.

---

## 🚀 Features

- User Registration & Login
- JWT Authentication
- Role-Based Authorization
- Product & Category Management
- Product Reviews
- Wishlist
- Shopping Cart
- Coupon System
- Shipping Address Management
- Order Management
- Payment Integration (Cash on Delivery & Razorpay)
- Email Notifications
- Admin Dashboard APIs
- Swagger API Documentation
- Unit Testing
- PostgreSQL Database Support

---

## 🛠️ Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Razorpay
- Swagger (drf-spectacular)
- Docker
- Git & GitHub
- Postman

---

## 📁 Project Structure

```
ecommerce_backend/
│
├── apps/
│   ├── accounts/
│   ├── products/
│   ├── wishlist/
│   ├── cart/
│   ├── coupons/
│   ├── shipping/
│   ├── orders/
│   ├── payments/
│   └── notifications/
│
├── ecommerce_backend/
├── media/
├── static/
├── manage.py
├── requirements.txt
└── .env.example
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/ecommerce-backend.git

cd ecommerce-backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add the required environment variables.

### Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

Server will start at

```
http://127.0.0.1:8000/
```

---

## 📖 API Documentation

Swagger UI

```
http://127.0.0.1:8000/api/docs/
```

ReDoc

```
http://127.0.0.1:8000/api/redoc/
```

---

## 🔄 Project Workflow

```
Register
      ↓
Login
      ↓
Browse Products
      ↓
Wishlist
      ↓
Cart
      ↓
Apply Coupon
      ↓
Shipping Address
      ↓
Checkout
      ↓
Create Order
      ↓
Payment
      ↓
Notification
```

---

## 📌 Main Modules

- Accounts
- Products
- Wishlist
- Cart
- Coupons
- Shipping
- Orders
- Payments
- Notifications

---

## 🔒 Authentication

This project uses JWT Authentication.

After login, the user receives:

- Access Token
- Refresh Token

These tokens are required to access protected APIs.

---

## 🧪 Testing

Run all tests

```bash
python manage.py test
```

Run coverage

```bash
coverage run manage.py test

coverage report
```

---

## 👨‍💻 Author

**Onkar Ambhore**

Python Backend Developer



GitHub: https://github.com/your-github

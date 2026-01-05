🌱 Agriculture Linkage Platform -- Authentication & Authorization Service

This service handles **user registration**, **authentication**, and
**role-based access control** for the Agriculture Linkage Platform.\
It is built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and
**JWT**.


## 📌 Features

-   User registration with **email & username uniqueness**
-   Secure password hashing
-   JWT-based authentication
-   Role-based access control (Farmer, Buyer, Admin)
-   Protected routes
-   Swagger / OpenAPI documentation


## 🧱 Tech Stack

  Layer              Technology
  ------------------ -------------------
  Backend            FastAPI (Python)
  Database           PostgreSQL
  ORM                SQLAlchemy
  Authentication     JWT
  Password Hashing   bcrypt
  API Docs           Swagger (OpenAPI)



## 🗂 Project Structure

    app/
    ├── core/
    │   ├── config.py
    │   ├── security.py
    │   └── dependencies.py
    │
    ├── db/
    │   └── database.py
    │
    ├── models/
    │   └── user.py
    │
    ├── routes/
    │   ├── routes.py
    │   ├── farmer.py
    │   ├── buyer.py
    │   └── admin.py
    │
    ├── schemas/
    │   └── user_schema.py
    │
    ├── services/
    │   └── auth_service.py
    │
    └── main.py



## 👤 User Roles

-   farmer\
-   buyer\
-   admin


## 🔐 Authentication Flow

1.  User registers
2.  Password is hashed
3.  User logs in
4.  JWT token is issued
5.  Token is sent via Authorization header
6.  Role-based access is enforced



## 📖 Swagger API Documentation

Access Swagger UI at:

http://127.0.0.1:8000/docs

## ▶️ Running the Project


uvicorn app.main:app --reload

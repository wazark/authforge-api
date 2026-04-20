# 🚀 AuthForge API

A **production-ready authentication system** built with **FastAPI**, following clean architecture and modern backend best practices.

---

## 🧩 Overview

AuthForge is a modular and scalable authentication system designed to simulate a real-world backend service.
It includes secure user authentication, token management, and a clean separation of concerns.

This project is intended as a **portfolio-level backend system** demonstrating professional engineering standards.

---

## ⚙️ Tech Stack

* **Python 3.11**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy (ORM)**
* **Alembic (migrations)**
* **JWT (Access & Refresh Tokens)**
* **Passlib (bcrypt hashing)**
* **Docker & Docker Compose**
* **Pytest (testing)**

---

## 📐 Architecture

The project follows a **clean and modular architecture**:

```
app/
├── api/            # Routes (controllers)
├── core/           # Config, security, dependencies
├── db/             # Database setup
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas
├── repositories/   # Data access layer
├── services/       # Business logic
├── tests/          # Unit tests
```

### Principles:

* Separation of concerns
* Scalability
* Maintainability
* Testability

---

## 🔐 Features

### ✅ Core Features

* User registration
* User login
* JWT authentication (access token)
* Refresh token system (stored in DB)
* Password hashing (bcrypt)
* Protected routes
* Basic role system (user/admin)
* Logout (refresh token revocation)
* Input validation (Pydantic)

---

### 🚧 Planned Improvements

* Role-based authorization (RBAC enforcement)
* Token blacklist (true logout for access tokens)
* Rate limiting
* Login attempt tracking
* Email verification (mocked)
* Password reset flow
* Two-factor authentication (2FA)
* Audit logging

---

## 🐳 Running with Docker

### 1. Build and start services

```bash
docker compose up --build
```

---

### 2. Access the API

* API: http://localhost:8000
* Docs: http://localhost:8000/docs

---

## 🧪 Running Tests

```bash
pytest -v
```

### Covered flows:

* User registration
* User login
* Protected route (/auth/me)
* Invalid login

---

## 🔑 Authentication Flow

1. Register user
2. Login → receive:

   * access_token
   * refresh_token
3. Use access_token for protected routes
4. Refresh access_token using refresh_token
5. Logout → refresh token revoked

---

## ⚠️ Environment Variables

Create a `.env` file:

```env
# App
PROJECT_NAME=AuthForge
API_V1_STR=/api/v1
DEBUG=True

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=authforge
POSTGRES_PORT=5432
```

---

## 🧠 What This Project Demonstrates

* Clean backend architecture
* Real-world authentication flows
* Secure password handling
* Token lifecycle management
* Dockerized environment
* Database migrations with Alembic
* Automated testing

---

## 📌 Future Improvements

This project is actively evolving to include:

* Advanced security mechanisms
* Distributed caching (Redis)
* Full RBAC system
* Production-grade observability

---

## 👨‍💻 Author

Built as a backend engineering project focused on **real-world production patterns**.

---

## ⭐ Contributing

Feel free to fork, explore, and improve the project.

---

## 📄 License

MIT License

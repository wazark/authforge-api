# 🚀 AuthForge API

A **production-ready authentication system** built with **FastAPI**, following clean architecture and real-world backend practices.

---

## 🧩 Overview

AuthForge is a modular and scalable authentication service designed to simulate a **real-world backend system**.

It provides secure authentication, token lifecycle management, and a clean separation of concerns, making it suitable for production-like environments and portfolio demonstration.

---

## ⚙️ Tech Stack

* **Python 3.14**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy (ORM)**
* **Alembic (migrations)**
* **JWT (Access & Refresh Tokens)**
* **Passlib (bcrypt hashing)**
* **Docker & Docker Compose**
* **Pytest (testing)**
* **SlowAPI (rate limiting)**

---

## 📐 Architecture

The project follows a **clean and modular architecture**:

```
app/
├── api/            # Routes (controllers)
├── core/           # Config, security, dependencies
├── db/             # Database setup
├── models/         # SQLAlchemy models
├── repositories/   # Data access layer
├── schemas/        # Pydantic schemas
├── services/       # Business logic
├── tests/          # Unit tests
```

### Principles

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
* Logout (refresh token revocation + access token blacklist)
* Input validation (Pydantic)
* Rate limiting (login protection)

---

## 🔐 Security Highlights

* Secure password hashing (bcrypt)
* Token-based authentication (JWT)
* Token invalidation via blacklist (JTI)
* Refresh token persistence and revocation
* Rate limiting against brute-force attacks

---

## 🐳 Running with Docker

### Start services

```bash
docker compose up --build
```

---

### Access

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
* Protected routes
* Invalid credentials
* Logout invalidation
* Role-based access
* Rate limiting

---

## 🔑 Authentication Flow

1. Register user
2. Login → receive:

   * access_token
   * refresh_token
3. Use access_token for protected routes
4. Refresh access token when expired
5. Logout:

   * refresh token revoked
   * access token blacklisted

---

## 🗄️ Database Models

* **User**
* **Role**
* **Token (refresh tokens)**
* **BlacklistedToken (revoked access tokens)**

---

## ⚠️ Environment Variables

### `.env` (local development)

```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=authforge
POSTGRES_PORT=5432

SECRET_KEY=your_secret_key
```

### `.env.docker`

```env
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=authforge
POSTGRES_PORT=5432

SECRET_KEY=your_secret_key
```

---

## 🧠 What This Project Demonstrates

* Clean backend architecture
* Secure authentication flows
* Token lifecycle management
* Real-world logout strategy (blacklist)
* Dockerized environment
* Database migrations with Alembic
* Automated testing
* API protection via rate limiting

---

## 🚧 Next Steps

* Audit logging (security tracking)
* Email verification
* Password reset flow
* Two-factor authentication (2FA)
* Redis integration (caching / rate limiting)

---

## 👨‍💻 Author

Built as a backend engineering project focused on **real-world production patterns**.

---

## 📄 License

MIT License

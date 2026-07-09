# Week 3: Backend Frameworks & Web APIs

Welcome to Week 3 of the Python Full Stack Engineer (Python FSE) learning path. This week focuses on the fundamentals of backend web development, studying three major Python web frameworks (Django, Flask, and FastAPI), designing robust REST APIs, understanding microservices architecture, and securing web applications.

## Overview

Modern web applications rely on solid backend systems that process business logic, store and retrieve data, authenticate users, and expose APIs. This week's curriculum transitions from databases and testing (Week 2) into the world of web frameworks, API design, and distributed systems.

You will explore:
1. **Web Framework Foundations**: The concepts common to all web frameworks (Request-Response, MVC/MVT, WSGI/ASGI).
2. **Django**: Python's premium "batteries-included" framework for rapid development.
3. **Flask**: A lightweight, flexible micro-framework.
4. **FastAPI**: A high-performance, modern framework designed for building asynchronous APIs with automatic Swagger documentation.
5. **REST API Design & Microservices**: Core architecture patterns for modern web APIs and services.
6. **Authentication & Security**: Safeguarding applications using secure hashing, JWTs, and avoiding OWASP Top 10 vulnerabilities.

---

## Folder Structure

```text
Week-3/
├── README.md                           # Week 3 overview and learning path
└── BackendFrameworks/
    ├── web_framework_foundations.md    # Core web server and framework concepts
    ├── django_demo/                     # Demonstration of Django components
    │   ├── README.md                   # Explanation of Django structure
    │   ├── models.py                   # ORM data models and relationships
    │   ├── views.py                    # Class-based and function-based views
    │   ├── urls.py                     # URL routing configuration
    │   ├── forms.py                    # ModelForm and user input validation
    │   └── admin.py                    # Django Admin customization panel
    ├── flask_demo.py                   # Flask routing, templates, blueprints, and SQL Alchemy
    ├── fastapi_demo.py                 # FastAPI endpoints, Pydantic schemas, and dependencies
    ├── rest_api_design.md              # Best practices for designing RESTful APIs
    ├── microservices.md                # Monoliths vs. Microservices architecture
    └── authentication_security.py      # Hashing, JWTs, OWASP examples, and CORS
```

---

## Topics Covered

### 1. Web Framework Foundations
* Understanding MVC (Model-View-Controller) vs MVT (Model-View-Template) paradigms.
* The Request-Response Cycle and routing middleware.
* Gateways: WSGI (synchronous) vs ASGI (asynchronous).

### 2. The Python Framework Suite
* **Django**: Exploring Django's structure, standard fields, forms, and admin interface.
* **Flask**: Working with routes, rendering templates with Jinja2, connecting SQLite with SQLAlchemy, blueprints, and custom error handling.
* **FastAPI**: Implementing async endpoints, Pydantic schemas, dependency injection, and leveraging self-documenting OpenAPI schemas.

### 3. API Design & Architecture
* REST principles, HTTP methods, status codes, and query filtering.
* Designing scalable systems: monoliths vs microservices, inter-service communication, and gateways.

### 4. Security & Authentication
* Safe password storage using `bcrypt`.
* Core authentication mechanisms (JWT workflow and Session-based).
* Mitigating security issues (OWASP Top 10) and configuring CORS (Cross-Origin Resource Sharing).

---

## Learning Outcomes

By the end of this week, you will be able to:
- Choose the correct Python framework (Django, Flask, or FastAPI) for a given backend task.
- Understand the internal mechanics of a web server (WSGI/ASGI, middleware).
- Build functional CRUD applications and define databases using Django ORM and SQLAlchemy.
- Create secure, structured REST APIs with path validation and query parameters.
- Articulate the differences between monolithic and microservices systems, knowing when to transition.
- Secure web endpoints using password hashing, validation, CORS headers, and JWT verification.

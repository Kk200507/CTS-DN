# Web Framework Foundations

This module introduces the underlying concepts of web frameworks. Before diving into Django, Flask, or FastAPI, it is critical to understand the architecture, cycles, and gateways that govern how modern web applications process HTTP traffic.

---

## 1. What is a Web Framework?

A **Web Framework** is a software library or collection of packages that provides a structured way to build and run web applications. Instead of writing low-level code to listen to network sockets, parse raw HTTP requests, map URLs, format HTML strings, or manage database connections manually, a framework provides pre-built modules for these repetitive tasks.

### Core Responsibilities of a Web Framework:
1. **Routing**: Mapping incoming HTTP request URIs to specific handlers (views or controllers).
2. **HTTP Handling**: Parsing headers, cookies, query parameters, form data, and payloads, then constructing appropriate HTTP responses (HTML, JSON, XML).
3. **Database Integration (ORM)**: Translating Python objects into SQL queries and vice versa.
4. **Templating**: Generating dynamic HTML by injecting backend data into markup files.
5. **Security Controls**: Providing protection against common threats (CSRF, XSS, SQL Injection).
6. **Middleware**: Providing hooks to inspect or alter requests and responses globally.

---

## 2. MVC vs. MVT Architecture

Architectural patterns help separate concerns in an application: separating data storage, business logic, and presentation.

### MVC (Model-View-Controller)
Common in frameworks like Ruby on Rails, ASP.NET, or Spring.
* **Model**: Manages data structure, database access, and core business rules.
* **View**: The user interface representation (HTML/CSS/JS or JSON format).
* **Controller**: The brain of the application. It receives inputs (via routing), manipulates the Model, and selects the View to render.

### MVT (Model-View-Template)
Specifically popularized by **Django**.
* **Model**: Represents the database table schemas (similar to MVC's Model).
* **View**: Contains the business logic. It handles the request, interacts with the Model, and calls the Template. (Similar to MVC's *Controller*).
* **Template**: The presentation layer (HTML with Django Template Language). It controls how data is displayed. (Similar to MVC's *View*).

### Mapping Comparison

| MVC Layer | Django (MVT) equivalent | Responsibility |
| :--- | :--- | :--- |
| **Model** | **Model** | Manages data schemas and database transactions. |
| **Controller** | **View** | Executes business logic, handles requests, and fetches data. |
| **View** | **Template** | Decides how to render and present the data to the user. |

---

## 3. The Request-Response Cycle

Every interaction on the web follows the **Request-Response Cycle**. Here is what happens when a user navigates to `https://example.com/books/`:

```text
  [ Client Browser ]
         │
    1. HTTP Request (GET /books/)
         ▼
  [ Web Server / Gateway (Nginx/Gunicorn) ]
         │
    2. Maps request to WSGI/ASGI application
         ▼
  [ Framework Middleware ]
         │ (Inspects request headers, authentication status, etc.)
         ▼
  [ Router / URL Resolver ]
         │ (Matches '/books/' to books_list_view())
         ▼
  [ View / Controller (Business Logic) ] ───► 3. Queries [ Model / DB ]
         │                               ◄─── Returns recordsets
    4. Passes data to [ Template / Serializer ]
         ▼
  [ Framework Middleware ]
         │ (Inspects/modifies outbound HTTP response headers)
         ▼
  [ Web Server / Gateway ]
         │
    5. HTTP Response (200 OK + HTML/JSON payload)
         ▼
  [ Client Browser ]
```

---

## 4. Routing

Routing is the mechanism that maps an incoming HTTP request path and HTTP method to a specific block of executable code.

### Static Routing
Matches exact string paths.
```python
# Example: Matches 'https://example.com/about'
@app.route("/about")
def about():
    return "About Us Page"
```

### Dynamic Routing (Path Parameters)
Captures variables from the URL path.
```python
# Example: Matches 'https://example.com/user/10' or 'https://example.com/user/42'
@app.route("/user/<int:user_id>")
def show_user_profile(user_id):
    # 'user_id' is captured as an integer and passed to the function
    return f"User ID: {user_id}"
```

---

## 5. Middleware

**Middleware** is a system of hooks or software layers that execute sequentially during the request-response lifecycle. It allows you to process request parameters before they reach the view, or alter the response before it goes back to the client.

### Common Middleware Tasks:
* **Authentication**: Checking if a request has a valid session cookie or authorization header.
* **Logging**: Recording incoming requests, performance metrics, and errors.
* **Security Headers**: Adding `X-Frame-Options` or `Content-Security-Policy` to the response.
* **Session Management**: Loading session data into `request.session`.
* **CORS (Cross-Origin Resource Sharing)**: Appending headers to permit client apps from other domains to call the API.

---

## 6. Gateways: WSGI vs. ASGI

Python web frameworks do not talk directly to production web servers (like Nginx, Apache, or IIS). They communicate through standard interface specifications.

### WSGI (Web Server Gateway Interface)
* **Introduced**: 2003 (PEP 333 / PEP 3333).
* **Model**: **Synchronous** (One thread/process per request).
* **Usage**: Django (traditionally), Flask.
* **Production Servers**: Gunicorn, uWSGI.
* **Limitation**: Not designed for long-lived connections, WebSockets, or high-concurrency async operations. A single slow database query blocks the process.

### ASGI (Asynchronous Server Gateway Interface)
* **Introduced**: 2016 (designed as a successor to WSGI).
* **Model**: **Asynchronous** (Event loop based, single thread handling thousands of requests concurrently).
* **Usage**: FastAPI, Django Channels, Starlette.
* **Production Servers**: Uvicorn, Daphne, Hypercorn.
* **Benefits**: Native support for WebSockets, HTTP/2, Server-Sent Events (SSE), and asynchronous Python features (`async`/`await`).

---

## 7. Synchronous vs. Asynchronous Frameworks

The fundamental difference lies in how they handle I/O bound operations (database calls, external API queries, file reads).

### Synchronous (Blocking)
When a synchronous framework executes a database query, the executing thread **blocks** and waits for the database response. 
* **Analogy**: A single chef in a kitchen who puts a steak on the grill and stands still watching it cook before starting to chop vegetables.
* **Scale Strategy**: Run multiple processes/threads. This consumes significant RAM and CPU.

```python
# Synchronous Example
import time

def fetch_data_from_db():
    time.sleep(2)  # Blocks the entire process/thread for 2 seconds
    return {"data": "sync results"}
```

### Asynchronous (Non-Blocking)
An asynchronous framework uses an event loop. When it encounters an I/O operation, it relinquishes control back to the event loop, allowing other requests to run in the meantime.
* **Analogy**: A chef who puts the steak on the grill, sets a timer, and immediately chops vegetables while the steak cooks, returning to the steak only when the timer rings.
* **Scale Strategy**: Handles thousands of concurrent requests using a single thread, keeping resource usage light.

```python
# Asynchronous Example
import asyncio

async def fetch_data_from_db_async():
    await asyncio.sleep(2)  # Yields control; thread is free to handle other requests
    return {"data": "async results"}
```

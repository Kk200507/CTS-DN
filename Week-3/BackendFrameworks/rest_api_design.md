# REST API Design Guidelines

This document outlines the core principles, standards, and best practices for designing **Representational State Transfer (REST)** web APIs.

---

## 1. Core Principles of REST

REST is an architectural style first introduced by Roy Fielding in 2000. For an API to be considered RESTful, it must follow six constraints:

1. **Client-Server Architecture**: Separates the user interface concerns (client) from the data storage and business logic concerns (server).
2. **Statelessness**: Each request from a client must contain all the information necessary to understand and process the request. The server must not store any session context about the client.
3. **Cacheability**: Responses must declare themselves as cacheable or non-cacheable to improve network efficiency and load times.
4. **Uniform Interface**: Simplifies and decouples the architecture. All components must interact using a single, unified interface. This is achieved by:
   - Resource identification in requests (usually URI paths).
   - Resource manipulation through representations (e.g., JSON payload).
   - Self-descriptive messages (declaring `Content-Type` headers).
   - Hypermedia As The Engine Of Application State (HATEOAS).
5. **Layered System**: A client cannot tell whether it is connected directly to the end server or to an intermediate box (e.g., load balancer, CDN, API Gateway).
6. **Code on Demand (Optional)**: Servers can temporarily extend client functionality by transferring executable code (e.g., JavaScript scripts).

---

## 2. Resources & URI Design

In REST, everything is a **resource** (an object or representation). A resource is addressed using a **Uniform Resource Identifier (URI)**.

### Rules for Resource Naming:
* **Use nouns, not verbs**: URIs should represent objects, not actions.
  - ❌ *Bad*: `GET /get_all_users` or `POST /create_user`
  -  *Good*: `GET /users` or `POST /users`
* **Use plural nouns**: Keep collection names plural for consistency.
  - ❌ *Bad*: `GET /user/42`
  -  *Good*: `GET /users/42`
* **Maintain hierarchy**: Nest sub-resources logically.
  -  *Good*: `GET /authors/12/books/` (Retrieves books written by author 12)

---

## 3. HTTP Methods & CRUD Mapping

REST uses standard HTTP methods to perform Create, Read, Update, and Delete (CRUD) operations.

| HTTP Method | CRUD Operation | Safe? | Idempotent? | Success Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | Read | **Yes** | **Yes** | `200 OK` |
| **POST** | Create | No | No | `201 Created` |
| **PUT** | Update (Replace) | No | **Yes** | `200 OK` or `204 No Content` |
| **PATCH** | Update (Partial) | No | No | `200 OK` or `204 No Content` |
| **DELETE** | Delete | No | **Yes** | `200 OK` or `204 No Content` |

> **Idempotent** means making multiple identical requests has the same side-effect on the server as making a single request. (e.g., Deleting an object twice doesn't delete it again; the result is still that the object is gone).

---

## 4. Common HTTP Status Codes

Status codes are grouped into classes. A REST API must return the correct code to represent the outcome of the request.

### 2xx: Success
* `200 OK`: Request succeeded. Often returns resource data.
* `201 Created`: Request succeeded and a new resource was created. (Include `Location` header pointing to new resource URI).
* `204 No Content`: Request succeeded, but there is no body payload in the response (common for DELETE operations).

### 4xx: Client Errors
* `400 Bad Request`: General client error (malformed JSON payload, missing required field parameters).
* `401 Unauthorized`: Client lacks credentials. Must authenticate.
* `403 Forbidden`: Client authenticated but does not have permission to access the resource.
* `404 Not Found`: The requested resource or path does not exist.
* `409 Conflict`: Request conflicts with current server state (e.g., email address already registered).

### 5xx: Server Errors
* `500 Internal Server Error`: General server failure (exceptions, database connection drops).
* `503 Service Unavailable`: Server is overloaded or down for maintenance.

---

## 5. API Versioning

API versioning prevents breaking changes from crashing client applications when you update the API structure.

### Method 1: URI Path Versioning (Recommended & Common)
The version is clearly visible in the URL path.
```text
GET /api/v1/users/
GET /api/v2/users/
```

### Method 2: Custom Request Header Versioning
Clients specify the target version inside headers.
```text
Accept: application/vnd.company.v1+json
# Or custom header:
X-API-Version: 2
```

---

## 6. Pagination, Filtering, and Sorting

When collections have thousands of records, returning all of them blocks databases and wastes bandwidth. Use query parameters to partition results.

### Pagination
* **Limit-Offset Pagination**:
  `GET /users?limit=20&offset=40`
* **Cursor-Based Pagination** (Preferred for high performance / infinite scrolling):
  `GET /users?limit=20&after_id=4592`

### Filtering
Allow clients to restrict results based on fields:
```text
GET /books?author=rowling&status=published
GET /employees?department=engineering&min_salary=80000
```

### Sorting
Allow clients to define list sorting:
```text
GET /products?sort=price_asc
GET /products?sort=-created_at   # Minus sign represents descending order
```

---

## 7. Best Practices & Standard Error Payloads

1. **Always return JSON**: Ensure responses use header `Content-Type: application/json`.
2. **Be consistent in casing**: Choose `camelCase` or `snake_case` for payloads and adhere to it across all endpoints.
3. **Structured error responses**: Never return raw server traces. Return consistent error payloads:
   ```json
   {
     "error": "validation_failed",
     "message": "The request payload did not pass validation.",
     "details": {
       "email": ["Please enter a valid email address."]
     }
   }
   ```
4. **Use Rate Limiting**: Protect endpoints from denial of service (DoS) by returning `429 Too Many Requests` when limits are breached.

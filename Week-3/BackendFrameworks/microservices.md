# Microservices Architecture

This document covers the architectural concepts of microservices, comparing them to traditional monoliths, exploring key patterns, and analyzing how services communicate.

---

## 1. Monolith vs. Microservices

### Monolithic Architecture
A monolithic application is built as a single, unified unit. All components—database access layer, business logic, rendering templates, user management, payment processing—are packaged and deployed together.

```text
       [ Single Monolithic Application ]
┌─────────────────────────────────────────────┐
│  User Auth  │  Billing  │  Catalog  │ Order │
└─────────────────────────────────────────────┘
                     │
             [ Single Database ]
```

### Microservices Architecture
A microservices architecture breaks down the application into a collection of small, autonomous, and loosely coupled services. Each service represents a single business capability, has its own codebase, and manages its own database.

```text
  [ User Auth ]    [ Billing ]    [ Catalog ]    [ Order ]
  ┌───────────┐    ┌─────────┐    ┌─────────┐    ┌───────┐
  │ Service   │    │ Service │    │ Service │    │Service│
  └───────────┘    └─────────┘    └─────────┘    └───────┘
        │               │              │             │
   [ Auth DB ]    [ Billing DB ]  [ Catalog DB ] [ Order DB ]
```

---

## 2. Comparison: Advantages vs. Disadvantages

| Feature | Monolith | Microservices |
| :--- | :--- | :--- |
| **Development** | Simple. Single repository, easy to start. | Complex. Requires managing multiple repositories/APIs. |
| **Scaling** | Scaled by duplicating the whole app. Heavy. | Finely scaled. Scale only the bottleneck service. |
| **Fault Isolation** | Poor. A bug in payment can crash the whole app. | Good. If billing crashes, catalog still works. |
| **Tech Diversity** | Bound to one programming language/stack. | Polyglot. Different services can use different stacks. |
| **Deployment** | Long build times; risky redeployment of entire code. | Independent deployment. Rapid CI/CD. |
| **Data Integrity** | Simple (SQL ACID transactions). | Complex (Eventual consistency, Sagas). |

---

## 3. Service Decomposition Patterns

The key to building a successful microservices system is deciding how to split a large application.

* **Decomposition by Business Capability**: Mapping services to specific functions, such as Product Catalog, Shipping, or Inventory.
* **Decomposition by Subdomain (Domain-Driven Design)**: Grouping modules based on DDD subdomains:
  - *Core Domain*: Key competitive advantage (e.g., matching algorithm for Uber).
  - *Supporting Domain*: Related to core but not unique (e.g., inventory management).
  - *Generic Domain*: Standard utilities (e.g., authentication, payments).
* **Decomposition Guidelines**:
  - Services should follow the **Single Responsibility Principle (SRP)**.
  - Minimize database joins across services. A service should never directly query another service's database.

---

## 4. API Gateway Pattern

In a microservices system, a single client page might need data from multiple microservices. Instead of making the client call dozens of different backend services directly, an **API Gateway** acts as the single entry point.

```text
               [ Client Browser ]
                       │
         HTTP GET /dashboard (Single Call)
                       ▼
               [ API Gateway ]
               /       │       \
       (Fan-out calls to backend services)
             /         │         \
     [ Auth Service ]  │   [ Order Service ]
                       ▼
              [ Catalog Service ]
```

### Gateway Responsibilities:
* **Routing / Reverse Proxy**: Maps external routes to internal microservice IP addresses.
* **Request Aggregation**: Merges multiple internal responses into a single client payload.
* **Security & Auth**: Validates incoming API keys or JWT credentials at the edge.
* **Rate Limiting / Throttling**: Protects downstream services from being overwhelmed.

---

## 5. Service Discovery

In a cloud environment, microservice instances are dynamic. They scale up, down, crash, and restart, meaning their IP addresses change constantly. **Service Discovery** solves this.

* **Service Registry**: A database containing the network locations of all active service instances (e.g., HashiCorp Consul, Netflix Eureka).
* **Self-Registration**: On startup, a microservice instance sends its IP and port to the Service Registry.
* **Querying / Lookup**:
  - *Client-Side Discovery*: Client queries the registry directly for instance locations, then applies load-balancing algorithms.
  - *Server-Side Discovery*: Client calls a load balancer, which queries the registry and routes the traffic internally.

---

## 6. Inter-Service Communication

Since microservices must work together to complete tasks, they need ways to communicate.

### Synchronous Communication (Request-Response)
Services make direct connections to each other.
* **Protocols**: HTTP/REST, gRPC (using HTTP/2 for high performance).
* **Pros**: Simple to write and debug; immediate feedback.
* **Cons**: Direct coupling. If Service B is slow, Service A slows down too, creating cascading failures.

### Asynchronous Communication (Message / Event-Driven)
Services communicate indirectly by publishing events to a message broker.
* **Brokers**: RabbitMQ, Apache Kafka, Amazon SQS.
* **Pattern (Publish/Subscribe)**:
  - Service A publishes an event `OrderCreated` to the broker.
  - Service B (Billing) and Service C (Inventory) subscribe to the broker and receive the message independently. Service A does not wait for them.
* **Pros**: Decouples services, high throughput, resilient to temporary downtime of downstream services.
* **Cons**: System is eventually consistent; debugging trace logs is more complex.

---

## 7. When NOT to Use Microservices

Microservices are **not** a silver bullet. They introduce massive operational complexity.

Do **NOT** use microservices if:
1. **You are a small startup / early stage project**: Your domain boundaries are changing rapidly. Splitting them early leads to a "distributed monolith" where every change requires editing five different services.
2. **You have a small team**: A small team will spend all their time managing infrastructure (Kubernetes, registries, pipelines) rather than writing business features.
3. **Low concurrency requirements**: If your app handles low traffic, a monolith running on a single instance is cheaper, faster, and easier to monitor.
4. **Strong ACID transaction requirement**: If your business cannot tolerate eventual consistency and requires immediate, bulletproof database transaction locks (e.g., high-stakes financial operations), keep those tables inside a single monolith database.

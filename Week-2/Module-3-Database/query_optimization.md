# Query Optimization and Performance Tuning

Writing queries that work is only the first step. For full stack applications, writing queries that execute efficiently at scale is vital. This guide details query optimization and analysis techniques in relational databases and MongoDB.

---

## 1. Indexing Strategies

Indexes are specialized search helper structures that allow the database to locate rows quickly without scanning the entire table (Sequential Scan).

### Index Types (SQL)
- **B-Tree Index (Default)**: Balanced tree structure. Excellent for range queries (`>`, `<`), equality comparisons (`=`), and sorting (`ORDER BY`).
- **Hash Index**: Good only for exact equality (`=`) lookups. Does not support range queries or sorting.
- **GIN (Generalized Inverted Index)**: Primarily used in Postgres for JSONB paths or full-text search terms.
- **Partial Index**: Indexing only a subset of a table (e.g., `CREATE INDEX ON orders(user_id) WHERE status = 'active'`). Saves space and speed.

---

## 2. Analyzing Execution Plans: `EXPLAIN` vs. `EXPLAIN ANALYZE`

To optimize a query, you must first check the database's query planner.

- **`EXPLAIN`**: Shows the execution plan that the planner estimates it will use without executing the query. It reports estimated costs and expected rows.
- **`EXPLAIN ANALYZE`**: Actually runs the query, showing the estimated plan side-by-side with actual execution times, memory usage, and actual rows processed.

### Example (Postgres)
```sql
EXPLAIN ANALYZE
SELECT name, salary 
FROM employees 
WHERE department_id = 5 
ORDER BY salary DESC;
```

### Key Metrics to Look For:
1. **Seq Scan (Sequential Scan)**: The database is scanning the entire table. If the table is large, you probably need an index on the filtered column (`department_id`).
2. **Index Scan**: The database used an index to find rows. (Generally much faster than Seq Scan).
3. **Cost**: Estimates of the workspace resources needed to execute the query. (Lower is better).
4. **Actual Loop Time**: The time spent in each node of the plan.

---

## 3. Query Rewriting and Best Practices

### A. Avoid `SELECT *`
Only query the columns you need. Asking for all columns forces the database to read extra data from disk and increases network payload sizes.
- **Bad**: `SELECT * FROM users;`
- **Good**: `SELECT id, email, username FROM users;`

### B. Eliminate the N+1 Query Problem
When fetching a list of parent rows and then executing an individual query per row to fetch child details, you end up doing `N + 1` separate database trips.
- **Bad (Looping queries in ORM)**:
  ```python
  users = session.query(User).all()
  for user in users:
      print(user.orders) # Triggers a separate SQL query for every single user
  ```
- **Good (Eager loading / Join)**:
  ```python
  # Fetches users and orders in a single SQL JOIN query
  users = session.query(User).options(joinedload(User.orders)).all()
  ```

### C. Write Search-Friendly (Sargable) Queries
Avoid wrapping indexed columns in functions within `WHERE` clauses, as this invalidates the index.
- **Bad**: `SELECT * FROM transactions WHERE DATE_PART('year', created_at) = 2026;`
- **Good**: `SELECT * FROM transactions WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01';`

---

## 4. MongoDB Profiling and `explain()`

MongoDB provides equivalent query optimization features.

### Aggregation or Find Explain
Add `.explain("executionStats")` to any query to see stats:
```javascript
db.products.find({ category: "Electronics" }).explain("executionStats");
```

### Key Explain Outputs:
- **COLLSCAN**: Collection scan (searched every document in the collection). Indicates a missing index.
- **IXSCAN**: Index scan. Used an index to isolate documents.
- **nReturned**: Number of documents returned.
- **totalDocsExamined**: Number of documents MongoDB had to check. Ideally, `totalDocsExamined` should match `nReturned`. If `totalDocsExamined` is much larger, the query is inefficient.

### Database Profiler
To record slow operations (e.g., queries taking longer than 100ms):
```javascript
// Set profiling level 1 (log slow operations)
db.setProfilingLevel(1, { slowms: 100 });

// View the profile log
db.system.profile.find({ millis: { $gt: 100 } }).sort({ ts: -1 });
```

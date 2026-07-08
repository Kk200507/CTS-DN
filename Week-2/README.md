# Week 2 - Databases & Testing

This week focuses on database development (advanced SQL, PostgreSQL, MongoDB, Schema Design, and ORMs) and software testing concepts & practices (PyTest, unittest, Jest, Mocha, TDD, Mocking, and Code Coverage).

## Folder Guide

### [Module 3: Database](./Module-3-Database/)
- `advanced_sql.sql`: Window functions, CTEs, advanced joins, subqueries, and grouping sets.
- `postgresql_examples.sql`: Postgres-specific features (JSONB, full-text search, triggers, arrays, and upsert).
- `mongodb_examples.js`: MongoDB shell JavaScript operations (CRUD, indexing, and aggregation pipelines).
- `schema_design.md`: Normalization vs. denormalization, primary/foreign keys, and SQL vs. NoSQL modeling.
- `query_optimization.md`: Indexing strategies, execution plans (`EXPLAIN`), and query rewrite optimizations.
- `migrations.md`: Database versioning concepts, migrations (Alembic, Flyway), and best practices.
- `orm_examples.py`: SQLAlchemy 2.0 ORM definitions, CRUD operations, relationships, and eager/lazy loading.

### [Module 4: Testing](./Module-4-Testing/)
- `testing_fundamentals.md`: Testing pyramid, Arrange-Act-Assert (AAA), and boundary conditions.
- `pytest_examples.py`: PyTest test cases, fixtures, parametrization, and exception handling.
- `unittest_examples.py`: Python's built-in `unittest` library (setUp/tearDown, assertions, and test suites).
- `jest_examples.js`: Jest testing for JavaScript (matchers, mock functions, async, and snapshots).
- `mocha_examples.js`: Mocha/Chai framework syntax (describe/it, hooks, and Chai assertions).
- `mocking.md`: Mocks, stubs, spies, fakes, Python's `unittest.mock`, and JS mocking libraries.
- `tdd.md`: Test-Driven Development flow (Red-Green-Refactor) and practical walkthrough.
- `code_coverage.md`: Coverage types (statement, branch, path), tools (coverage.py, nyc), and interpretations.

## How to Run

### Python Examples
Run ORM, PyTest, or unittest files from the command line:
```bash
# Run SQLAlchemy ORM examples
python Module-3-Database/orm_examples.py

# Run unittest suite
python Module-4-Testing/unittest_examples.py

# Run PyTest suite (requires pytest)
pytest Module-4-Testing/pytest_examples.py
```

### JavaScript / Node.js Examples
Run Jest or Mocha tests (requires Node.js and packages installed):
```bash
# Run Jest tests
npx jest Module-4-Testing/jest_examples.js

# Run Mocha tests
npx mocha Module-4-Testing/mocha_examples.js
```

### SQL Examples
SQL and Mongo Shell files are reference files. You can execute them inside their respective database clients (e.g., `psql` for PostgreSQL, `mongosh` for MongoDB).

## Learning Goals
- Write and optimize complex relational queries using window functions and CTEs.
- Choose between normalization and denormalization based on access patterns.
- Design database schemas and manage schema migrations effectively.
- Write clean and maintainable unit tests in Python and JavaScript.
- Apply Test-Driven Development (TDD) and Mocking to isolate unit tests.
- Interpret code coverage metrics to identify untested execution paths.

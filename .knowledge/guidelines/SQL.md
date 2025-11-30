# SQL Guidelines

> SQL and database best practices

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Query Style](#2-query-style)
- [3. Schema Design](#3-schema-design)
- [4. Performance](#4-performance)
- [5. Security](#5-security)
- [6. Migrations](#6-migrations)
- [7. ORM Patterns](#7-orm-patterns)

---

## 1. Overview

### 1.1 Core Principles

| Principle       | Description                              |
|-----------------|------------------------------------------|
| **Clarity**     | Write readable, self-documenting queries |
| **Performance** | Consider query plans and indexes         |
| **Security**    | Prevent injection, least privilege       |
| **Consistency** | Follow naming conventions                |

### 1.2 Naming Conventions

| Element     | Convention            | Example                 |
|-------------|-----------------------|-------------------------|
| Tables      | `snake_case`, plural  | `users`, `order_items`  |
| Columns     | `snake_case`          | `created_at`, `user_id` |
| Primary Key | `id` or `table_id`    | `id`, `user_id`         |
| Foreign Key | `referenced_table_id` | `user_id`, `order_id`   |
| Indexes     | `idx_table_columns`   | `idx_users_email`       |
| Constraints | `type_table_columns`  | `uq_users_email`        |

---

## 2. Query Style

### 2.1 Formatting

```sql
-- ✅ Good - Clear formatting
SELECT u.id,
       u.name,
       u.email,
       COUNT(o.id) AS order_count
FROM users u
         LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active'
  AND u.created_at > '2024-01-01'
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) > 0
ORDER BY order_count DESC
LIMIT 100;

-- ❌ Bad - Hard to read
SELECT u.id, u.name, u.email, COUNT(o.id) AS order_count
FROM users u
         LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active'
  AND u.created_at > '2024-01-01'
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) > 0
ORDER BY order_count DESC
LIMIT 100;
```
### 2.2 Keywords and Capitalization

| Style         | Usage                              |
|---------------|------------------------------------|
| **UPPERCASE** | SQL keywords (SELECT, FROM, WHERE) |
| **lowercase** | Table names, column names, aliases |

### 2.3 Aliasing

```sql
-- ✅ Good - Meaningful aliases
SELECT c.name AS customer_name,
       p.name AS product_name,
       oi.quantity
FROM customers c
         JOIN orders o ON o.customer_id = c.id
         JOIN order_items oi ON oi.order_id = o.id
         JOIN products p ON p.id = oi.product_id;

-- ❌ Bad - Single letter aliases without context
SELECT a.name, b.name, c.quantity
FROM customers a
         JOIN orders b ON b.customer_id = a.id
         JOIN order_items c ON c.order_id = b.id;
```
### 2.4 Comments

```sql
-- Single line comment for simple explanations

/*
 * Multi-line comment for complex queries
 * Explains business logic or performance considerations
 */

-- ✅ Good - Document complex logic
SELECT user_id,
       -- Calculate 30-day rolling average
       AVG(amount) OVER (
           PARTITION BY user_id
           ORDER BY created_at
           ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
           ) AS rolling_avg
FROM transactions;
```
---

## 3. Schema Design

### 3.1 Table Structure

```sql
-- ✅ Good - Well-structured table
CREATE TABLE users
(
    id BIGSERIAL PRIMARY KEY,
    email         VARCHAR(255) NOT NULL,
    name          VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status        VARCHAR(20) DEFAULT 'active',
    created_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at    TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT chk_users_status CHECK (status IN ('active', 'inactive', 'suspended'))
);

-- Create index for common queries
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_status ON users (status);
```
### 3.2 Data Types

| Use Case    | Recommended Type           | Avoid                  |
|-------------|----------------------------|------------------------|
| Primary Key | `BIGSERIAL` / `UUID`       | `INTEGER` (for scale)  |
| Money       | `DECIMAL(19,4)`            | `FLOAT`, `DOUBLE`      |
| Timestamp   | `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP` without TZ |
| Boolean     | `BOOLEAN`                  | `INTEGER`, `CHAR(1)`   |
| Status/Enum | `VARCHAR` + CHECK          | Integer codes          |
| JSON data   | `JSONB` (PostgreSQL)       | `TEXT`                 |

### 3.3 Relationships

```sql
-- One-to-Many
CREATE TABLE orders
(
    id BIGSERIAL PRIMARY KEY,
    user_id    BIGINT      NOT NULL REFERENCES users (id),
    status     VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Many-to-Many
CREATE TABLE user_roles
(
    user_id     BIGINT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    role_id     BIGINT NOT NULL REFERENCES roles (id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    PRIMARY KEY (user_id, role_id)
);
```
### 3.4 Normalization Guidelines

| Normal Form | Rule                       | When to Denormalize   |
|-------------|----------------------------|-----------------------|
| 1NF         | No repeating groups        | Never skip            |
| 2NF         | No partial dependencies    | Never skip            |
| 3NF         | No transitive dependencies | Read-heavy analytics  |
| BCNF        | Every determinant is a key | Rare, complex domains |

---

## 4. Performance

### 4.1 Index Strategy

```sql
-- ✅ Good - Index for WHERE clause columns
CREATE INDEX idx_orders_status ON orders (status);

-- ✅ Good - Composite index for multi-column queries
CREATE INDEX idx_orders_user_status ON orders (user_id, status);

-- ✅ Good - Partial index for common filter
CREATE INDEX idx_orders_active ON orders (user_id) WHERE status = 'active';

-- ✅ Good - Covering index to avoid table lookup
CREATE INDEX idx_users_email_name ON users (email) INCLUDE (name);
```
### 4.2 Query Optimization

```sql
-- ✅ Good - Use EXISTS instead of IN for large subqueries
SELECT *
FROM users u
WHERE EXISTS (SELECT 1
              FROM orders o
              WHERE o.user_id = u.id
                AND o.status = 'completed');

-- ✅ Good - Use LIMIT with ORDER BY
SELECT *
FROM orders
ORDER BY created_at DESC
LIMIT 10;

-- ❌ Bad - SELECT * in production
SELECT *
FROM users;

-- ✅ Good - Select only needed columns
SELECT id, name, email
FROM users;
```
### 4.3 Avoiding N+1 Queries

```sql
-- ❌ Bad - N+1 pattern (in application)
-- for user in users:
--     orders = SELECT * FROM orders WHERE user_id = user.id

-- ✅ Good - Single query with JOIN
SELECT u.id,
       u.name,
       o.id AS order_id,
       o.total
FROM users u
         LEFT JOIN orders o ON o.user_id = u.id
WHERE u.status = 'active';

-- ✅ Good - Or use array aggregation
SELECT u.id,
       u.name,
       ARRAY_AGG(o.id) AS order_ids
FROM users u
         LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;
```
### 4.4 EXPLAIN Usage

```sql
-- Always check query plan for complex queries
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id)
FROM users u
         JOIN orders o ON o.user_id = u.id
GROUP BY u.name;

-- Key metrics to watch:
-- - Seq Scan vs Index Scan
-- - Actual vs Estimated rows
-- - Sort operations
-- - Hash joins vs Nested loops
```
---

## 5. Security

### 5.1 Parameterized Queries

```python
# ✅ Good - Parameterized query
cursor.execute(
    "SELECT * FROM users WHERE email = %s",
    (user_email,)
)

# ❌ Bad - String interpolation (SQL injection risk)
cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")
```
### 5.2 Least Privilege

```sql
-- Create role with minimal permissions
CREATE ROLE app_reader;
GRANT SELECT ON users, orders TO app_reader;

CREATE ROLE app_writer;
GRANT SELECT, INSERT, UPDATE ON users, orders TO app_writer;

-- Application user with specific role
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT app_writer TO app_user;
```
### 5.3 Row-Level Security

```sql
-- Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own orders
CREATE
POLICY user_orders ON orders
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::bigint);
```
---

## 6. Migrations

### 6.1 Migration Best Practices

| Practice       | Description                      |
|----------------|----------------------------------|
| **Reversible** | Always include rollback SQL      |
| **Atomic**     | One logical change per migration |
| **Safe**       | Avoid locks on large tables      |
| **Tested**     | Test on copy of production data  |

### 6.2 Safe Schema Changes

```sql
-- ✅ Good - Add column with default (fast in PostgreSQL 11+)
ALTER TABLE users
    ADD COLUMN verified BOOLEAN DEFAULT false;

-- ✅ Good - Create index concurrently (no lock)
CREATE INDEX CONCURRENTLY idx_users_verified ON users (verified);

-- ⚠️ Caution - Adding NOT NULL requires table rewrite
-- Do in steps:
-- 1. Add nullable column
ALTER TABLE users
    ADD COLUMN phone VARCHAR(20);
-- 2. Backfill data
UPDATE users
SET phone = ''
WHERE phone IS NULL;
-- 3. Add constraint
ALTER TABLE users
    ALTER COLUMN phone SET NOT NULL;

-- ✅ Good - Rename with view for compatibility
ALTER TABLE users RENAME TO users_v2;
CREATE VIEW users AS
SELECT *
FROM users_v2;
```
### 6.3 Migration File Format

```sql
-- migrations/20240101120000_add_user_verified.sql

-- Up
ALTER TABLE users
    ADD COLUMN verified BOOLEAN DEFAULT false;
CREATE INDEX idx_users_verified ON users (verified);

-- Down
DROP INDEX IF EXISTS idx_users_verified;
ALTER TABLE users
    DROP COLUMN IF EXISTS verified;
```
---

## 7. ORM Patterns

### 7.1 SQLAlchemy (Python)

```python
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Query patterns
# ✅ Good - Explicit columns
users = session.query(User.id, User.name).filter(User.status == 'active').all()

# ✅ Good - Eager loading to avoid N+1
users = session.query(User).options(joinedload(User.orders)).all()
```
### 7.2 Prisma (TypeScript)

```typescript
// schema.prisma
model
User
{
    id
    BigInt
@id @default
    (autoincrement())
    email
    String
@unique
    name
    String
    orders
    Order[]
    createdAt
    DateTime
@default
    (now())
}

// Query patterns
// ✅ Good - Select specific fields
const users = await prisma.user.findMany({
    select: {id: true, name: true},
    where: {status: 'active'}
});

// ✅ Good - Include relations
const usersWithOrders = await prisma.user.findMany({
    include: {orders: true}
});
```
### 7.3 Raw Queries When Needed

```python
# Use raw SQL for complex queries
result = session.execute(
    """
        SELECT
            u.id,
            u.name,
            COUNT(o.id) as order_count,
            SUM(o.total) as total_spent
        FROM users u
        LEFT JOIN orders o ON o.user_id = u.id
        WHERE u.created_at > :since
        GROUP BY u.id, u.name
        HAVING COUNT(o.id) > :min_orders
    """, {
        'since'     : datetime(2024, 1, 1),
        'min_orders': 5
    }
)
```
---

## Quick Reference

### Common Query Patterns

| Pattern     | SQL                                |
|-------------|------------------------------------|
| Pagination  | `LIMIT 10 OFFSET 20`               |
| Upsert      | `INSERT ... ON CONFLICT DO UPDATE` |
| Soft Delete | `WHERE deleted_at IS NULL`         |
| Count       | `SELECT COUNT(*) FROM table`       |
| Exists      | `SELECT EXISTS(SELECT 1 FROM ...)` |

### Performance Checklist

| Check             | Description                       |
|-------------------|-----------------------------------|
| ☐ Indexes exist   | For WHERE, JOIN, ORDER BY columns |
| ☐ EXPLAIN checked | No unexpected seq scans           |
| ☐ N+1 avoided     | Use JOINs or batch queries        |
| ☐ Pagination used | LIMIT on large result sets        |
| ☐ SELECT specific | No SELECT * in production         |

---

## Related

- `.knowledge/guidelines/ENGINEERING.md` — Engineering practices
- `.knowledge/practices/engineering/API_DESIGN.md` — API patterns
- `.knowledge/guidelines/SECURITY.md` — Security guidelines

---

*AI Collaboration Knowledge Base*

# Database Best Practices

> Guidelines for effective database design and usage

---

## Table of Contents

- [1. Design Principles](#1-design-principles)
- [2. Query Optimization](#2-query-optimization)
- [3. Connection Management](#3-connection-management)
- [4. Data Integrity](#4-data-integrity)

---

## 1. Design Principles

### Schema Design

| Principle                   | Description                              |
|-----------------------------|------------------------------------------|
| **Normalize appropriately** | 3NF for OLTP, denormalize for read-heavy |
| **Choose types carefully**  | Use smallest type that fits              |
| **Define constraints**      | NOT NULL, UNIQUE, FK where applicable    |
| **Plan for growth**         | Consider partitioning early              |

### Naming Conventions

```sql
-- Tables: plural, snake_case
CREATE TABLE users (...);
CREATE TABLE order_items (...);

-- Columns: singular, snake_case
user_id, created_at, is_active

-- Indexes: ix_table_columns
CREATE INDEX ix_users_email ON users(email);

-- Foreign keys: fk_table_referenced
CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id)
```
### Index Strategy

| Index Type    | Use Case                         |
|---------------|----------------------------------|
| **B-tree**    | Range queries, sorting (default) |
| **Hash**      | Equality lookups only            |
| **Composite** | Multi-column WHERE/ORDER         |
| **Partial**   | Filtered subset of rows          |
| **Covering**  | Include all SELECT columns       |

```sql
-- Composite index (column order matters!)
CREATE INDEX ix_orders_user_date ON orders(user_id, created_at DESC);

-- Partial index
CREATE INDEX ix_active_users ON users(email) WHERE is_active = true;

-- Covering index
CREATE INDEX ix_orders_covering ON orders(user_id) INCLUDE (total, status);
```
---

## 2. Query Optimization

### Query Patterns

```sql
-- ❌ Bad: SELECT *
SELECT * FROM users WHERE id = 1;

-- ✅ Good: Select only needed columns
SELECT id, name, email FROM users WHERE id = 1;

-- ❌ Bad: N+1 queries (in application loop)
-- ✅ Good: JOIN or batch query
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.id IN (1, 2, 3);

-- ❌ Bad: LIKE with leading wildcard
SELECT * FROM users WHERE name LIKE '%john%';

-- ✅ Good: Full-text search for text searching
SELECT * FROM users WHERE to_tsvector(name) @@ to_tsquery('john');
```
### Pagination

```sql
-- ❌ Bad: OFFSET for large datasets
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 10000;

-- ✅ Good: Keyset pagination
SELECT * FROM orders
WHERE id > :last_seen_id
ORDER BY id
LIMIT 20;
```
### EXPLAIN Usage

```sql
-- Always analyze slow queries
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- Look for:
-- - Seq Scan (may need index)
-- - High cost estimates
-- - Row count mismatches
```
---

## 3. Connection Management

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=10,           # Base connections
    max_overflow=20,        # Extra when needed
    pool_timeout=30,        # Wait time for connection
    pool_recycle=1800,      # Recycle after 30 min
    pool_pre_ping=True,     # Verify before use
)
```
### Async Connections

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=10,
    max_overflow=20,
)

async with AsyncSession(engine) as session:
    result = await session.execute(query)
```
---

## 4. Data Integrity

### Transactions

```python
# Always use transactions for multi-step operations
async with session.begin():
    user = await session.get(User, user_id)
    user.balance -= amount
    
    transfer = Transfer(from_user=user_id, amount=amount)
    session.add(transfer)
    # Auto-commit on exit, rollback on exception
```
### Constraints

```sql
-- Use database constraints, not just application logic
ALTER TABLE users ADD CONSTRAINT chk_email CHECK (email LIKE '%@%');
ALTER TABLE orders ADD CONSTRAINT chk_amount CHECK (amount > 0);

-- Unique constraints
ALTER TABLE users ADD CONSTRAINT uq_users_email UNIQUE (email);
```
### Soft Deletes

```sql
-- Soft delete pattern
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;

-- Query active records
SELECT * FROM users WHERE deleted_at IS NULL;

-- Create partial index for performance
CREATE INDEX ix_users_active ON users(email) WHERE deleted_at IS NULL;
```
---

## Quick Reference

### Performance Checklist

- [ ] Indexes on WHERE/JOIN columns
- [ ] Connection pooling configured
- [ ] N+1 queries eliminated
- [ ] Large result sets paginated
- [ ] Slow query logging enabled
- [ ] EXPLAIN used for optimization

### Common Anti-Patterns

| Anti-Pattern       | Solution                |
|--------------------|-------------------------|
| N+1 queries        | Batch/JOIN              |
| SELECT *           | Select specific columns |
| No indexes         | Add appropriate indexes |
| No connection pool | Configure pooling       |
| OFFSET pagination  | Keyset pagination       |

---

## Related

- `.knowledge/frameworks/performance/OPTIMIZATION_STRATEGIES.md` — Performance guide
- `.knowledge/practices/engineering/BATCH_OPTIMIZATION.md` — Batch processing

---

*AI Collaboration Knowledge Base*

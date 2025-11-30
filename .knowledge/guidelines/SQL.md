# SQL Guidelines

> SQL and database conventions and best practices

---

## Table of Contents

- [1. Core Principles](#1-core-principles)
- [2. Naming Conventions](#2-naming-conventions)
- [3. Style Guide](#3-style-guide)
- [4. Quick Reference](#4-quick-reference)

---

## 1. Core Principles

| Principle       | Description                              |
|-----------------|------------------------------------------|
| **Clarity**     | Write readable, self-documenting queries |
| **Performance** | Consider query plans and indexes         |
| **Security**    | Prevent injection, least privilege       |
| **Consistency** | Follow naming conventions                |

---

## 2. Naming Conventions

| Element     | Convention            | Example                 |
|-------------|-----------------------|-------------------------|
| Tables      | `snake_case`, plural  | `users`, `order_items`  |
| Columns     | `snake_case`          | `created_at`, `user_id` |
| Primary Key | `id` or `table_id`    | `id`, `user_id`         |
| Foreign Key | `referenced_table_id` | `user_id`, `order_id`   |
| Indexes     | `idx_table_columns`   | `idx_users_email`       |
| Constraints | `type_table_columns`  | `uq_users_email`        |

---

## 3. Style Guide

### 3.1 Keywords and Capitalization

| Style         | Usage                              |
|---------------|------------------------------------|
| **UPPERCASE** | SQL keywords (SELECT, FROM, WHERE) |
| **lowercase** | Table names, column names, aliases |

### 3.2 Formatting Rules

| Rule                | Description                          |
|---------------------|--------------------------------------|
| One clause per line | SELECT, FROM, WHERE on separate lines |
| Indent JOINs        | Align JOIN clauses for readability   |
| Align columns       | Vertically align selected columns    |
| Use aliases         | Meaningful table aliases (not a, b, c) |

### 3.3 Data Types

| Use Case    | Recommended Type           | Avoid                  |
|-------------|----------------------------|------------------------|
| Primary Key | `BIGSERIAL` / `UUID`       | `INTEGER` (for scale)  |
| Money       | `DECIMAL(19,4)`            | `FLOAT`, `DOUBLE`      |
| Timestamp   | `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP` without TZ |
| Boolean     | `BOOLEAN`                  | `INTEGER`, `CHAR(1)`   |
| Status/Enum | `VARCHAR` + CHECK          | Integer codes          |
| JSON data   | `JSONB` (PostgreSQL)       | `TEXT`                 |

---

## 4. Quick Reference

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

### Security Checklist

| Check                  | Description                    |
|------------------------|--------------------------------|
| ☐ Parameterized queries | Never use string interpolation |
| ☐ Least privilege      | Minimal permissions per role   |
| ☐ Input validation     | Validate before query          |
| ☐ Row-level security   | When multi-tenant              |

### Migration Checklist

| Check              | Description                      |
|--------------------|----------------------------------|
| ☐ Reversible       | Include rollback SQL             |
| ☐ Atomic           | One logical change per migration |
| ☐ Non-blocking     | Use CONCURRENTLY for indexes     |
| ☐ Tested           | Test on production copy          |

---

## Related

- `.knowledge/practices/engineering/SQL_PATTERNS.md` — Query patterns, schema design, and implementations
- `.knowledge/guidelines/ENGINEERING.md` — Engineering practices
- `.knowledge/guidelines/SECURITY.md` — Security guidelines

---

*AI Collaboration Knowledge Base*

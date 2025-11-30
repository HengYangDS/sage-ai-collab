# API Design Patterns

> Principles and patterns for designing clean, consistent APIs

---

## Table of Contents

- [1. Design Principles](#1-design-principles)
- [2. Naming Conventions](#2-naming-conventions)
- [3. HTTP Methods](#3-http-methods)
- [4. Response Patterns](#4-response-patterns)
- [5. Pagination](#5-pagination)
- [6. Versioning](#6-versioning)
- [7. Best Practices](#7-best-practices)

---

## 1. Design Principles

| Principle       | Description                   |
|-----------------|-------------------------------|
| Consistency     | Same patterns throughout      |
| Predictability  | Behavior matches expectations |
| Simplicity      | Easy to understand and use    |
| Discoverability | Self-documenting structure    |

---

## 2. Naming Conventions

### 2.1 Resources

| Type        | Convention       | Example               |
|-------------|------------------|-----------------------|
| Collection  | Plural nouns     | `/users`, `/orders`   |
| Single item | Singular with ID | `/users/{id}`         |
| Nested      | Parent/child     | `/users/{id}/orders`  |
| Actions     | Verb suffix      | `/orders/{id}/cancel` |

### 2.2 Parameters

| Type  | Convention | Example                 |
|-------|------------|-------------------------|
| Path  | snake_case | `/users/{user_id}`      |
| Query | snake_case | `?page_size=10`         |
| Body  | snake_case | `{"first_name": "..."}` |

---

## 3. HTTP Methods

| Method | Purpose          | Idempotent |
|--------|------------------|------------|
| GET    | Read resource    | Yes        |
| POST   | Create resource  | No         |
| PUT    | Replace resource | Yes        |
| PATCH  | Partial update   | Yes        |
| DELETE | Remove resource  | Yes        |

---

## 4. Response Patterns

### 4.1 Success Responses

| Status | Use For                        |
|--------|--------------------------------|
| 200    | Successful GET, PUT, PATCH     |
| 201    | Successful POST (created)      |
| 204    | Successful DELETE (no content) |

### 4.2 Error Responses

| Status | Use For                  |
|--------|--------------------------|
| 400    | Bad request (validation) |
| 401    | Unauthorized             |
| 403    | Forbidden                |
| 404    | Not found                |
| 409    | Conflict                 |
| 500    | Server error             |

### 4.3 Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Invalid format"
      }
    ]
  }
}
```
---

## 5. Pagination

### 5.1 Request

```
GET /users?page=2&page_size=20
```
### 5.2 Response

```json
{
  "data": [
    ...
  ],
  "pagination": {
    "page": 2,
    "page_size": 20,
    "total": 150,
    "total_pages": 8
  }
}
```
---

## 6. Versioning

| Strategy | Example          | Use When       |
|----------|------------------|----------------|
| URL path | `/v1/users`      | Major versions |
| Header   | `API-Version: 1` | Fine control   |
| Query    | `?version=1`     | Simple cases   |

---

## 7. Best Practices

| Practice                | Benefit              |
|-------------------------|----------------------|
| Use nouns for resources | RESTful clarity      |
| Return created resource | Immediate access     |
| Include pagination      | Handle large sets    |
| Version from start      | Future compatibility |
| Document thoroughly     | Developer experience |

---

## Related

- `.knowledge/guidelines/CODE_STYLE.md` — Code conventions
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns

---

*AI Collaboration Knowledge Base*

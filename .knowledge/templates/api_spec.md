# API Specification Template

> **Purpose**: Document API endpoints, request/response schemas, and behaviors
> **Use When**: Designing new APIs or documenting existing endpoints

---

## Template

```markdown
# [API Name] Specification

> **Version**: [x.y.z]
> **Base URL**: [https://api.example.com/v1]
> **Last Updated**: [YYYY-MM-DD]

---

## Overview

[Brief description of what this API does and its primary use cases]

---

## Authentication

| Method | Header | Format |
|--------|--------|--------|
| [Bearer Token / API Key / OAuth2] | `Authorization` | `Bearer <token>` |

---

## Endpoints

### [Resource Name]

#### [METHOD] [/path/{param}]

**Description**: [What this endpoint does]

**Authentication**: [Required / Optional / None]

**Rate Limit**: [requests/minute]

##### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param` | string | Yes | [Description] |

##### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number |
| `limit` | integer | No | 20 | Items per page |

##### Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | Yes | `application/json` |
| `X-Request-ID` | No | Correlation ID |

##### Request Body

```json
{
  "field1": "string",
  "field2": 123,
  "nested": {
    "subfield": "value"
  }
}
```

| Field             | Type    | Required | Description   |
|-------------------|---------|----------|---------------|
| `field1`          | string  | Yes      | [Description] |
| `field2`          | integer | No       | [Description] |
| `nested.subfield` | string  | No       | [Description] |

##### Response

**Success (200 OK)**

```json
{
  "id": "abc123",
  "field1": "string",
  "created_at": "2025-01-01T00:00:00Z"
}
```

| Field        | Type     | Description        |
|--------------|----------|--------------------|
| `id`         | string   | Unique identifier  |
| `field1`     | string   | [Description]      |
| `created_at` | datetime | ISO 8601 timestamp |

##### Error Responses

| Status | Code              | Description               |
|--------|-------------------|---------------------------|
| 400    | `INVALID_REQUEST` | Request validation failed |
| 401    | `UNAUTHORIZED`    | Authentication required   |
| 403    | `FORBIDDEN`       | Insufficient permissions  |
| 404    | `NOT_FOUND`       | Resource not found        |
| 429    | `RATE_LIMITED`    | Too many requests         |
| 500    | `INTERNAL_ERROR`  | Server error              |

##### Example

**Request**:

```bash
curl -X POST https://api.example.com/v1/resource \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{"field1": "value"}'
```

**Response**:

```json
{
  "id": "abc123",
  "field1": "value",
  "created_at": "2025-01-01T00:00:00Z"
}
```

---

## Data Models

### [ModelName]

| Field      | Type   | Required | Description                     |
|------------|--------|----------|---------------------------------|
| `id`       | string | Yes      | Unique identifier (UUID)        |
| `name`     | string | Yes      | Display name                    |
| `status`   | enum   | Yes      | `active`, `inactive`, `pending` |
| `metadata` | object | No       | Additional key-value pairs      |

---

## Error Format

All errors follow this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

---

## Pagination

List endpoints support cursor-based pagination:

```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "has_more": true
  }
}
```

---

## Rate Limiting

| Tier       | Limit     | Window   |
|------------|-----------|----------|
| Free       | 100       | 1 minute |
| Pro        | 1000      | 1 minute |
| Enterprise | Unlimited | -        |

Rate limit headers:

- `X-RateLimit-Limit`: Maximum requests
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset timestamp

---

## Changelog

| Version | Date       | Changes         |
|---------|------------|-----------------|
| 1.0.0   | YYYY-MM-DD | Initial release |

---

*API Specification from SAGE Knowledge Base*

```

---

## Instructions

### 1. Endpoint Documentation Order

1. HTTP Method and Path
2. Description
3. Authentication requirements
4. Parameters (path → query → header → body)
5. Response (success → errors)
6. Example

### 2. Best Practices

| Practice | Description |
|----------|-------------|
| Use consistent naming | snake_case for fields |
| Include examples | Real, working examples |
| Document all errors | Every possible error code |
| Version the API | Semantic versioning |
| Add rate limits | Prevent abuse documentation |

### 3. HTTP Methods

| Method | Use Case |
|--------|----------|
| GET | Retrieve resource(s) |
| POST | Create resource |
| PUT | Full update |
| PATCH | Partial update |
| DELETE | Remove resource |

### 4. Status Codes

| Range | Meaning |
|-------|---------|
| 2xx | Success |
| 4xx | Client error |
| 5xx | Server error |

---

## Related

- `practices/engineering/api_design.md` — API design patterns
- `guidelines/engineering.md` — Engineering standards
- `frameworks/patterns/persistence.md` — Data patterns

---

*Template from SAGE Knowledge Base*

---
title: SAGE Knowledge Base - HTTP API Reference
version: 3.1.0
date: 2025-11-28
status: production-ready
---

# HTTP API Reference

> **RESTful API for SAGE Knowledge Base powered by FastAPI**

## Overview

The SAGE HTTP API provides RESTful access to the knowledge base with:

- **Timeout Protection**: All endpoints support configurable timeouts
- **OpenAPI Documentation**: Auto-generated at `/docs` (Swagger UI) and `/redoc` (ReDoc)
- **CORS Support**: Configurable cross-origin resource sharing
- **Versioned Endpoints**: API versioning via URL path (`/v1/`)

### Base URL

```
http://localhost:8000
```

### Authentication

Currently, the API does not require authentication. For production deployments, configure authentication middleware as
needed.

---

## Endpoints

### System

#### Health Check

Check the API server health status.

```
GET /health
```

**Response**

| Field      | Type   | Description                 |
|------------|--------|-----------------------------|
| `status`   | string | Health status ("healthy")   |
| `version`  | string | API version                 |
| `services` | object | Status of internal services |

**Example Request**

```bash
curl http://localhost:8000/health
```

**Example Response**

```json
{
  "status": "healthy",
  "version": "3.1.0",
  "services": {
    "loader": "operational",
    "search": "operational"
  }
}
```

---

### Knowledge

#### List Layers

Get information about available knowledge layers.

```
GET /v1/layers
```

**Response**

Array of layer information objects:

| Field         | Type    | Description                    |
|---------------|---------|--------------------------------|
| `name`        | string  | Layer name                     |
| `tokens`      | integer | Estimated token count          |
| `always_load` | boolean | Whether layer is always loaded |

**Example Request**

```bash
curl http://localhost:8000/v1/layers
```

**Example Response**

```json
[
  {"name": "core", "tokens": 500, "always_load": true},
  {"name": "guidelines", "tokens": 1200, "always_load": false},
  {"name": "frameworks", "tokens": 2000, "always_load": false},
  {"name": "practices", "tokens": 1500, "always_load": false},
  {"name": "scenarios", "tokens": 500, "always_load": false}
]
```

---

#### Get Knowledge (POST)

Retrieve knowledge content with timeout protection.

```
POST /v1/knowledge
```

**Request Body**

| Field        | Type    | Required | Default    | Description                         |
|--------------|---------|----------|------------|-------------------------------------|
| `layers`     | array   | No       | `["core"]` | Layers to load                      |
| `query`      | string  | No       | `null`     | Optional query for smart loading    |
| `timeout_ms` | integer | No       | `5000`     | Timeout in milliseconds (100-30000) |

**Response**

| Field           | Type    | Description            |
|-----------------|---------|------------------------|
| `content`       | string  | Knowledge content      |
| `tokens`        | integer | Token count            |
| `status`        | string  | Load status            |
| `duration_ms`   | integer | Request duration in ms |
| `layers_loaded` | array   | List of loaded layers  |

**Example Request**

```bash
curl -X POST http://localhost:8000/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "layers": ["core", "guidelines"],
    "timeout_ms": 5000
  }'
```

**Example Response**

```json
{
  "content": "# Core Principles\n\n...",
  "tokens": 1700,
  "status": "complete",
  "duration_ms": 245,
  "layers_loaded": ["core", "guidelines"]
}
```

---

#### Get Layer (GET)

Retrieve knowledge from a specific layer.

```
GET /v1/knowledge/{layer}
```

**Path Parameters**

| Parameter | Type   | Description                                                     |
|-----------|--------|-----------------------------------------------------------------|
| `layer`   | string | Layer name (core, guidelines, frameworks, practices, scenarios) |

**Query Parameters**

| Parameter    | Type    | Required | Default | Description                         |
|--------------|---------|----------|---------|-------------------------------------|
| `timeout_ms` | integer | No       | `5000`  | Timeout in milliseconds (100-30000) |

**Response**

Same as POST `/v1/knowledge` response.

**Example Request**

```bash
curl "http://localhost:8000/v1/knowledge/core?timeout_ms=3000"
```

**Example Response**

```json
{
  "content": "# Core Principles\n\n## Xin-Da-Ya Philosophy\n...",
  "tokens": 500,
  "status": "complete",
  "duration_ms": 89,
  "layers_loaded": ["core"]
}
```

**Error Response (Invalid Layer)**

```json
{
  "detail": "Invalid layer. Valid layers: ['core', 'guidelines', 'frameworks', 'practices', 'scenarios']"
}
```

---

### Search

#### Search Knowledge

Search the knowledge base.

```
GET /v1/search
```

**Query Parameters**

| Parameter     | Type    | Required | Default | Description                         |
|---------------|---------|----------|---------|-------------------------------------|
| `q`           | string  | Yes      | -       | Search query (min 1 character)      |
| `max_results` | integer | No       | `5`     | Maximum results (1-20)              |
| `timeout_ms`  | integer | No       | `3000`  | Timeout in milliseconds (100-10000) |

**Response**

| Field         | Type    | Description             |
|---------------|---------|-------------------------|
| `query`       | string  | Original search query   |
| `results`     | array   | Array of search results |
| `count`       | integer | Number of results       |
| `duration_ms` | integer | Search duration in ms   |

**Search Result Item**

| Field     | Type   | Description     |
|-----------|--------|-----------------|
| `path`    | string | File path       |
| `score`   | float  | Relevance score |
| `preview` | string | Content preview |
| `layer`   | string | Source layer    |

**Example Request**

```bash
curl "http://localhost:8000/v1/search?q=timeout&max_results=3"
```

**Example Response**

```json
{
  "query": "timeout",
  "results": [
    {
      "path": "content/frameworks/timeout/hierarchy.md",
      "score": 0.95,
      "preview": "## Timeout Hierarchy\n\nThe 5-tier timeout system...",
      "layer": "frameworks"
    },
    {
      "path": "content/core/defaults.md",
      "score": 0.72,
      "preview": "Default timeout values for all operations...",
      "layer": "core"
    }
  ],
  "count": 2,
  "duration_ms": 156
}
```

---

## Error Handling

The API uses standard HTTP status codes:

| Status Code | Description                      |
|-------------|----------------------------------|
| `200`       | Success                          |
| `400`       | Bad Request (invalid parameters) |
| `404`       | Not Found                        |
| `408`       | Request Timeout                  |
| `500`       | Internal Server Error            |

**Error Response Format**

```json
{
  "detail": "Error message describing the issue"
}
```

---

## Running the Server

### Start Server

```bash
# Using CLI
sage serve --port 8000

# Using Python module
python -m sage serve

# Using uvicorn directly
uvicorn sage.services.http_server:app --host 0.0.0.0 --port 8000
```

### Configuration

Environment variables:

| Variable            | Description                     | Default   |
|---------------------|---------------------------------|-----------|
| `SAGE_API_HOST`     | Server host                     | `0.0.0.0` |
| `SAGE_API_PORT`     | Server port                     | `8000`    |
| `SAGE_CORS_ORIGINS` | Allowed CORS origins            | `[]`      |
| `SAGE_DEBUG`        | Enable debug mode (shows /docs) | `false`   |

---

## OpenAPI Documentation

When debug mode is enabled, interactive API documentation is available:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## References

- **Architecture Design**: See `../design/01-architecture.md`
- **Services Design**: See `../design/03-services.md`
- **MCP Protocol**: See `mcp_protocol.md`
- **CLI Reference**: See `cli_reference.md`

---

**Document Status**: Production Ready  
**Last Updated**: 2025-11-28

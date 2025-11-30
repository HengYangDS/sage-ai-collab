---
title: SAGE Knowledge Base - HTTP API Service Design
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~900
---

# HTTP API Service Design

> **RESTful API with FastAPI**

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Request/Response Models](#2-requestresponse-models)
- [3. Endpoints](#3-endpoints)
- [4. Configuration](#4-configuration)

---

## 1. Overview

The HTTP API Service provides RESTful access to SAGE Knowledge Base.

| Feature            | Technology | Description                      |
|--------------------|------------|----------------------------------|
| Framework          | FastAPI    | High-performance async API       |
| Documentation      | OpenAPI    | Auto-generated API docs          |
| Validation         | Pydantic   | Request/response validation      |
| CORS               | Middleware | Configurable cross-origin        |

---

## 2. Request/Response Models

```python
from pydantic import BaseModel, Field
from typing import Optional, List


class KnowledgeRequest(BaseModel):
    """Request for knowledge retrieval."""
    layers: List[str] = Field(default=["core"], description="Layers to load")
    query: Optional[str] = Field(None, description="Optional query for smart loading")
    timeout_ms: int = Field(5000, ge=100, le=30000, description="Timeout in ms")


class KnowledgeResponse(BaseModel):
    """Response with knowledge content."""
    content: str
    tokens: int
    status: str
    duration_ms: int
    layers_loaded: List[str]


class SearchResultItem(BaseModel):
    """Single search result."""
    path: str
    score: float
    preview: str
    layer: str


class SearchResponse(BaseModel):
    """Response with search results."""
    query: str
    results: List[SearchResultItem]
    count: int
    duration_ms: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    services: dict


class LayerInfo(BaseModel):
    """Information about a knowledge layer."""
    name: str
    tokens: int
    always_load: bool
```

---

## 3. Endpoints

### 3.1 System Endpoints

| Method | Endpoint  | Description       | Response           |
|--------|-----------|-------------------|--------------------|
| GET    | `/health` | Health check      | `HealthResponse`   |

### 3.2 Knowledge Endpoints

| Method | Endpoint              | Description              | Response              |
|--------|-----------------------|--------------------------|-----------------------|
| GET    | `/v1/layers`          | List available layers    | `List[LayerInfo]`     |
| POST   | `/v1/knowledge`       | Get knowledge (flexible) | `KnowledgeResponse`   |
| GET    | `/v1/knowledge/{layer}` | Get specific layer     | `KnowledgeResponse`   |

### 3.3 Search Endpoints

| Method | Endpoint     | Description           | Response          |
|--------|--------------|-----------------------|-------------------|
| GET    | `/v1/search` | Search knowledge base | `SearchResponse`  |

### 3.4 Endpoint Details

#### GET /health

```bash
curl http://localhost:8080/health
```

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "services": {
    "loader": "operational",
    "search": "operational"
  }
}
```

#### GET /v1/layers

```bash
curl http://localhost:8080/v1/layers
```

```json
[
  {"name": "core", "tokens": 500, "always_load": true},
  {"name": "guidelines", "tokens": 1200, "always_load": false},
  {"name": "frameworks", "tokens": 2000, "always_load": false},
  {"name": "practices", "tokens": 1500, "always_load": false}
]
```

#### POST /v1/knowledge

```bash
curl -X POST http://localhost:8080/v1/knowledge \
  -H "Content-Type: application/json" \
  -d '{"layers": ["core", "guidelines"], "timeout_ms": 5000}'
```

#### GET /v1/knowledge/{layer}

```bash
curl "http://localhost:8080/v1/knowledge/core?timeout_ms=5000"
```

#### GET /v1/search

```bash
curl "http://localhost:8080/v1/search?q=timeout&max_results=5"
```

```json
{
  "query": "timeout",
  "results": [
    {
      "path": ".knowledge/frameworks/resilience/timeout_patterns.md",
      "score": 0.95,
      "preview": "5-level timeout hierarchy...",
      "layer": "frameworks"
    }
  ],
  "count": 1,
  "duration_ms": 45
}
```

---

## 4. Configuration

### 4.1 Application Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_api_app() -> FastAPI:
    app = FastAPI(
        title="SAGE Knowledge Base API",
        version="0.1.0",
        description="Production-grade knowledge management",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure in production
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

    return app
```

### 4.2 Running the Server

```python
import uvicorn

def run_api_server(host: str = "localhost", port: int = 8080):
    """Run the API server."""
    uvicorn.run(
        "sage.services.http_server:create_api_app",
        factory=True,
        host=host,
        port=port,
        reload=False,
    )
```

### 4.3 Query Parameters

| Parameter     | Type | Default | Range       | Description     |
|---------------|------|---------|-------------|-----------------|
| `timeout_ms`  | int  | 5000    | 100-30000   | Timeout in ms   |
| `max_results` | int  | 5       | 1-20        | Max results     |
| `q`           | str  | -       | min 1 char  | Search query    |

---

## Related

- `docs/design/03-services.md` — Services overview
- `docs/design/03a-cli-service.md` — CLI service design
- `docs/design/03b-mcp-service.md` — MCP service design
- `docs/api/python.md` — Python API reference

---

*Part of SAGE Knowledge Base*

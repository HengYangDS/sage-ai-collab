# API Service

> HTTP REST API service using FastAPI

---

## 1. Overview

The API service provides HTTP REST access to SAGE knowledge base for web applications and external system integration using FastAPI framework.

---

## 2. Technology Stack

| Component | Library | Purpose |
|-----------|---------|---------|
| **Framework** | FastAPI | Async HTTP framework |
| **Server** | Uvicorn | ASGI server |
| **Validation** | Pydantic | Request/response validation |
| **Docs** | OpenAPI | Auto-generated API docs |

---

## 3. Endpoints

### 3.1 Endpoint Registry

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/knowledge` | Get knowledge content |
| GET | `/v1/search` | Search knowledge base |
| GET | `/v1/frameworks` | Get framework content |
| GET | `/v1/layers` | List knowledge layers |
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus metrics |

### 3.2 Request/Response Models

```python
from pydantic import BaseModel

class KnowledgeRequest(BaseModel):
    query: str
    layer: int | None = None
    content_type: str | None = None
    timeout_ms: int = 5000

class KnowledgeResponse(BaseModel):
    content: str
    layer: int
    content_type: str
    token_count: int
    cached: bool = False

class SearchRequest(BaseModel):
    query: str
    max_results: int = 10
    fuzzy: bool = False

class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int
    took_ms: int
```

---

## 4. Implementation

### 4.1 Application Setup

```python
from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    container = get_container()
    app.state.container = container
    yield
    # Shutdown
    container.dispose()

app = FastAPI(
    title="SAGE Knowledge Base API",
    version="1.0.0",
    lifespan=lifespan
)
```

### 4.2 Endpoints Implementation

```python
@app.get("/v1/knowledge", response_model=KnowledgeResponse)
async def get_knowledge(
    query: str,
    layer: int = None,
    content_type: str = None,
    loader: SourceProtocol = Depends(get_loader)
):
    result = loader.source(KnowledgeRequest(
        query=query,
        layer=layer,
        content_type=content_type
    ))
    return KnowledgeResponse(
        content=result.content,
        layer=result.layer,
        content_type=result.content_type,
        token_count=result.token_count
    )

@app.get("/v1/search", response_model=SearchResponse)
async def search_knowledge(
    query: str,
    max_results: int = 10,
    fuzzy: bool = False,
    searcher: AnalyzeProtocol = Depends(get_searcher)
):
    start = time.monotonic()
    results = searcher.search(query, max_results, fuzzy)
    took_ms = int((time.monotonic() - start) * 1000)
    
    return SearchResponse(
        results=results,
        total=len(results),
        took_ms=took_ms
    )
```

### 4.3 Health Check

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## 5. Authentication

### 5.1 Bearer Token Auth

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    token = credentials.credentials
    if not validate_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/v1/knowledge")
async def get_knowledge(
    query: str,
    token: str = Depends(verify_token)
):
    ...
```

### 5.2 API Key Auth

```python
from fastapi import Header

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in valid_api_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
```

---

## 6. Error Handling

### 6.1 Exception Handlers

```python
@app.exception_handler(TimeoutError)
async def timeout_handler(request: Request, exc: TimeoutError):
    return JSONResponse(
        status_code=504,
        content={
            "error": {
                "code": "SAGE-1001",
                "message": "Operation timed out",
                "details": {"timeout_ms": exc.timeout_ms}
            }
        }
    )

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "SAGE-1002",
                "message": str(exc)
            }
        }
    )
```

### 6.2 HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Success |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Auth failed |
| 404 | Not Found | Content not found |
| 504 | Gateway Timeout | Operation timeout |
| 500 | Internal Error | Unexpected error |

---

## 7. Configuration

```yaml
services:
  api:
    host: "0.0.0.0"
    port: 8080
    workers: 4
    timeout_ms: 30000
    cors_origins:
      - "http://localhost:3000"
    auth:
      enabled: true
      type: bearer
```

---

## 8. Middleware

### 8.1 CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
```

### 8.2 Request Logging

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    duration = time.monotonic() - start
    
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s"
    )
    return response
```

---

## 9. Testing

### 9.1 API Testing

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_knowledge():
    response = client.get("/v1/knowledge?query=test")
    assert response.status_code == 200
    data = response.json()
    assert "content" in data

def test_search():
    response = client.get("/v1/search?query=architecture")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## Related

- `SERVICE_LAYER.md` — Service layer overview
- `CLI_SERVICE.md` — CLI service
- `MCP_SERVICE.md` — MCP service
- `../timeout_resilience/INDEX.md` — Timeout patterns

---

*AI Collaboration Knowledge Base*

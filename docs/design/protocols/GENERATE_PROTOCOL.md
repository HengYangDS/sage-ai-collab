# Generate Protocol

> Output formatting, rendering, and multi-channel delivery

---

## 1. Overview

The Generate protocol (G in SAGE) transforms analyzed knowledge into user-facing outputs across multiple delivery channels.

---

## 2. Responsibilities

| Operation | Purpose | Output |
|-----------|---------|--------|
| **Format** | Structure for target | FormattedContent |
| **Render** | Apply templates | RenderedContent |
| **Deliver** | Send to channel | DeliveryResult |

---

## 3. Formatting

### 3.1 Format Types

| Format | Use Case | Example |
|--------|----------|---------|
| **Markdown** | Documentation | `.md` files |
| **HTML** | Web output | Web pages |
| **JSON** | API responses | REST API |
| **Plain** | CLI output | Terminal |
| **Structured** | MCP protocol | Tool responses |

### 3.2 Formatting Flow

```mermaid
graph TD
    KG[KnowledgeGraph]
    subgraph Formatter
        Query["Query<br/>What? (intent)"]
        Select["Select<br/>Which? (nodes)"]
        Transform["Transform<br/>How? (format)"]
        Query --> Select --> Transform
    end
    FC[FormattedContent]
    
    KG --> Query
    Transform --> FC
```

### 3.3 Formatted Content Structure

```python
@dataclass
class FormattedContent:
    id: str
    format_type: str
    content: str | dict | list
    metadata: dict[str, Any]
    source_nodes: list[str]
```

---

## 4. Rendering

### 4.1 Template System

| Template Type | Purpose | Example |
|---------------|---------|---------|
| **Document** | Full documents | Design doc template |
| **Section** | Document parts | Code block template |
| **Component** | UI components | Table template |
| **Inline** | Text fragments | Link template |

### 4.2 Rendering Flow

```mermaid
graph TD
    FC[FormattedContent]
    subgraph Renderer
        TL[Template Loader]
        CB[Context Builder]
        Engine["Engine (Jinja2)"]
        TL --> Engine
        CB --> Engine
    end
    RC[RenderedContent]
    
    FC --> TL
    FC --> CB
    Engine --> RC
```

### 4.3 Rendered Content Structure

```python
@dataclass
class RenderedContent:
    id: str
    content: str
    content_type: str  # text/markdown, text/html, etc.
    byte_size: int
    token_count: int | None
    render_time_ms: float
```

---

## 5. Delivery

### 5.1 Delivery Channels

| Channel | Interface | Format |
|---------|-----------|--------|
| **CLI** | Terminal | Plain text, colored |
| **MCP** | Protocol | Structured JSON |
| **API** | HTTP | JSON, HTML |
| **File** | Filesystem | Any format |
| **Stream** | Real-time | Chunked |

### 5.2 Delivery Flow

```mermaid
graph TD
    RC[RenderedContent]
    subgraph Deliverer
        Router[Channel Router]
        CLI[CLI]
        MCP[MCP]
        API[API]
        File[File]
        Collector[Result Collector]
        Router --> CLI
        Router --> MCP
        Router --> API
        Router --> File
        CLI --> Collector
        MCP --> Collector
        API --> Collector
        File --> Collector
    end
    DR[DeliveryResult]
    
    RC --> Router
    Collector --> DR
```

### 5.3 Delivery Result Structure

```python
@dataclass
class DeliveryResult:
    success: bool
    channel: str
    delivered_at: datetime
    byte_count: int
    duration_ms: float
    error: str | None
```

---

## 6. Generation Pipeline

```mermaid
graph TD
    KG[KnowledgeGraph]
    Format["Format<br/>Structure for target channel"]
    Render["Render<br/>Apply templates and styles"]
    Deliver["Deliver<br/>Send to CLI/MCP/API/File"]
    DR[DeliveryResult]
    
    KG --> Format --> Render --> Deliver --> DR
```

---

## 7. Channel Adapters

### 7.1 CLI Adapter

```python
class CLIAdapter:
    def deliver(self, content: RenderedContent) -> DeliveryResult:
        # Handle terminal width
        # Apply ANSI colors
        # Manage pagination
        ...
```

### 7.2 MCP Adapter

```python
class MCPAdapter:
    def deliver(self, content: RenderedContent) -> DeliveryResult:
        # Format as MCP response
        # Handle token limits
        # Include metadata
        ...
```

### 7.3 API Adapter

```python
class APIAdapter:
    def deliver(self, content: RenderedContent) -> DeliveryResult:
        # Set content type
        # Handle compression
        # Manage caching
        ...
```

---

## 8. Configuration

```yaml
generate:
  formatting:
    default_format: markdown
    max_length: 50000
  
  rendering:
    template_path: "templates/"
    cache_templates: true
  
  delivery:
    cli:
      color: true
      pager: auto
    mcp:
      max_tokens: 8000
    api:
      compression: gzip
```

---

## Related

- `ANALYZE_PROTOCOL.md` — Previous phase
- `EVOLVE_PROTOCOL.md` — Next phase
- `../services/INDEX.md` — Service layer

---

*AI Collaboration Knowledge Base*

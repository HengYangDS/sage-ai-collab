# Extension Points

> Where and how plugins can extend SAGE functionality

---

## 1. Overview

Extension points are well-defined interfaces where plugins can inject custom behavior into SAGE's processing pipeline.

---

## 2. Extension Point Types

| Type | Purpose | Example |
|------|---------|---------|
| **Capability** | Add new capabilities | Custom analyzer |
| **Hook** | Intercept operations | Pre-process hook |
| **Event** | React to events | On-load handler |
| **Config** | Custom configuration | Plugin settings |
| **Service** | Add service endpoints | Custom API route |

---

## 3. Capability Extensions

### 3.1 Capability Families

Plugins can add capabilities to any of the 5 families:

| Family | Extension Interface |
|--------|---------------------|
| **Analyzers** | `AnalyzerCapability` |
| **Checkers** | `CheckerCapability` |
| **Monitors** | `MonitorCapability` |
| **Converters** | `ConverterCapability` |
| **Generators** | `GeneratorCapability` |

### 3.2 Capability Interface

```python
class CapabilityExtension(Protocol):
    """Base protocol for capability extensions."""
    
    @property
    def name(self) -> str:
        """Unique capability name."""
        ...
    
    @property
    def family(self) -> str:
        """Capability family (analyzers, checkers, etc.)."""
        ...
    
    def execute(self, context: Context, *args, **kwargs) -> Result:
        """Execute the capability."""
        ...

# Example: Custom analyzer
class CustomAnalyzer(CapabilityExtension):
    name = "custom_analyzer"
    family = "analyzers"
    
    def execute(self, context: Context, content: str) -> AnalysisResult:
        # Custom analysis logic
        return AnalysisResult(...)
```

### 3.3 Registration

```python
class MyPlugin(Plugin):
    def register(self, container: Container) -> None:
        container.register_capability(CustomAnalyzer())
```

---

## 4. Hook Extensions

### 4.1 Hook Points

| Hook | Trigger | Use Case |
|------|---------|----------|
| `pre_source` | Before sourcing | Input validation |
| `post_source` | After sourcing | Data enrichment |
| `pre_analyze` | Before analysis | Pre-processing |
| `post_analyze` | After analysis | Result enhancement |
| `pre_generate` | Before generation | Template customization |
| `post_generate` | After generation | Output post-processing |

### 4.2 Hook Interface

```python
class Hook(Protocol):
    """Hook extension interface."""
    
    @property
    def name(self) -> str:
        """Hook identifier."""
        ...
    
    @property
    def point(self) -> str:
        """Hook point (pre_source, post_analyze, etc.)."""
        ...
    
    @property
    def priority(self) -> int:
        """Execution order (lower = earlier)."""
        return 100
    
    def execute(self, context: Context, data: Any) -> Any:
        """Execute hook, may modify data."""
        ...
```

### 4.3 Hook Registration

```python
class ValidationHook(Hook):
    name = "input_validator"
    point = "pre_source"
    priority = 10
    
    def execute(self, context: Context, sources: list[str]) -> list[str]:
        # Validate and filter sources
        return [s for s in sources if self._is_valid(s)]

# Register in plugin
container.register_hook(ValidationHook())
```

---

## 5. Event Extensions

### 5.1 Subscribable Events

| Event | Payload | Description |
|-------|---------|-------------|
| `system.initialized` | `{version, mode}` | System startup complete |
| `system.shutdown` | `{reason}` | System shutting down |
| `source.completed` | `{count, duration}` | Sourcing finished |
| `analyze.completed` | `{nodes, edges}` | Analysis finished |
| `generate.delivered` | `{channel, size}` | Output delivered |
| `plugin.loaded` | `{name, version}` | Plugin loaded |
| `error.occurred` | `{type, message}` | Error happened |

### 5.2 Event Subscription

```python
class MyPlugin(Plugin):
    def on_load(self) -> None:
        event_bus = self.container.resolve(EventBus)
        event_bus.subscribe("source.completed", self._on_source_complete)
        event_bus.subscribe("error.*", self._on_error)
    
    def _on_source_complete(self, event: Event) -> None:
        count = event.payload["count"]
        self.logger.info(f"Sourced {count} items")
    
    def _on_error(self, event: Event) -> None:
        # Handle errors
        pass
```

---

## 6. Config Extensions

### 6.1 Custom Configuration

```python
@dataclass
class MyPluginConfig:
    enabled: bool = True
    threshold: float = 0.8
    options: dict = field(default_factory=dict)

class MyPlugin(Plugin):
    def register(self, container: Container) -> None:
        # Register config schema
        container.register_config_schema(
            "my_plugin",
            MyPluginConfig
        )
```

### 6.2 Config Access

```python
def execute(self, context: Context) -> Result:
    config = context.get_plugin_config("my_plugin")
    if config.threshold > 0.5:
        # Use threshold
        pass
```

---

## 7. Service Extensions

### 7.1 API Routes

```python
class MyPlugin(Plugin):
    def register(self, container: Container) -> None:
        api_service = container.resolve(APIService)
        api_service.add_route(
            method="GET",
            path="/plugins/my-plugin/status",
            handler=self._status_handler
        )
    
    async def _status_handler(self, request: Request) -> Response:
        return {"status": "ok", "version": self.version}
```

### 7.2 CLI Commands

```python
class MyPlugin(Plugin):
    def register(self, container: Container) -> None:
        cli_service = container.resolve(CLIService)
        cli_service.add_command(
            name="my-command",
            handler=self._cli_handler,
            help="My custom command"
        )
```

---

## 8. Extension Point Registry

```python
class ExtensionRegistry:
    def __init__(self):
        self.capabilities: dict[str, list[CapabilityExtension]] = {}
        self.hooks: dict[str, list[Hook]] = {}
        self.event_handlers: dict[str, list[Callable]] = {}
    
    def register_capability(self, capability: CapabilityExtension) -> None:
        family = capability.family
        if family not in self.capabilities:
            self.capabilities[family] = []
        self.capabilities[family].append(capability)
    
    def get_capabilities(self, family: str) -> list[CapabilityExtension]:
        return self.capabilities.get(family, [])
```

---

## 9. Best Practices

| Practice | Description |
|----------|-------------|
| **Single responsibility** | Each extension does one thing |
| **Fail gracefully** | Don't break core on plugin error |
| **Document behavior** | Explain what extension does |
| **Version compatibility** | Declare supported versions |
| **Test thoroughly** | Test extension in isolation |

---

## 10. Extension Point Matrix

| Extension Point | Phase | Can Modify | Can Block |
|-----------------|-------|------------|-----------|
| `pre_source` | Source | ✅ Input | ✅ Yes |
| `post_source` | Source | ✅ Output | ❌ No |
| `pre_analyze` | Analyze | ✅ Input | ✅ Yes |
| `post_analyze` | Analyze | ✅ Output | ❌ No |
| `pre_generate` | Generate | ✅ Input | ✅ Yes |
| `post_generate` | Generate | ✅ Output | ❌ No |
| `event.*` | Any | ❌ No | ❌ No |

---

## Related

- `PLUGIN_ARCHITECTURE.md` — Plugin system design
- `PLUGIN_LIFECYCLE.md` — Plugin states
- `../capabilities/INDEX.md` — Capability families

---

*AI Collaboration Knowledge Base*

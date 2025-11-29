---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

﻿---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~450
---

# MCP Integration Checklist

> Task checklist for Model Context Protocol (MCP) server and client integration

---

## Planning

- [ ] MCP use case defined
- [ ] Server vs client role determined
- [ ] Resource types identified
- [ ] Tool capabilities planned
- [ ] Prompt templates designed

## Server Setup

- [ ] MCP server framework chosen (FastMCP, etc.)
- [ ] Server configuration created
- [ ] Transport layer configured (stdio/SSE/WebSocket)
- [ ] Server lifecycle managed
- [ ] Health checks implemented

## Resources

- [ ] Resource URIs designed
- [ ] Resource schemas defined
- [ ] Resource listing implemented
- [ ] Resource reading implemented
- [ ] Resource subscriptions (if needed)

## Tools

- [ ] Tool definitions created
- [ ] Input schemas validated
- [ ] Tool handlers implemented
- [ ] Error handling standardized
- [ ] Tool results formatted

## Prompts

- [ ] Prompt templates defined
- [ ] Arguments validated
- [ ] Dynamic content supported
- [ ] Prompt versioning considered
- [ ] Context injection working

## Client Integration

- [ ] Client SDK chosen
- [ ] Connection management implemented
- [ ] Request/response handling
- [ ] Streaming support (if needed)
- [ ] Reconnection logic

## Security

- [ ] Authentication configured
- [ ] Authorization rules defined
- [ ] Input validation strict
- [ ] Rate limiting implemented
- [ ] Secrets properly managed

## Error Handling

- [ ] Error codes standardized
- [ ] Error messages helpful
- [ ] Timeout handling implemented
- [ ] Graceful degradation planned
- [ ] Retry logic configured

## Testing

- [ ] Unit tests for tools
- [ ] Integration tests for resources
- [ ] End-to-end protocol tests
- [ ] Load testing performed
- [ ] Error scenario testing

## Documentation

- [ ] API documentation complete
- [ ] Usage examples provided
- [ ] Configuration guide written
- [ ] Troubleshooting guide created
- [ ] Changelog maintained

---

*SAGE Knowledge Base - MCP Integration Checklist*
---

## Related

- `.knowledge/scenarios/mcp_integration/context.md` — MCP integration context
- `.knowledge/practices/engineering/api_design.md` — API design patterns
- `.knowledge/practices/engineering/error_handling.md` — Error handling patterns

---

*Part of SAGE Knowledge Base*

# Bolt API Framework

A high-performance, async Python web framework built on **Granian** and **msgspec**.
Designed for maximum throughput and zero overhead.

## Features
- **Zero-Copy Validation** using `msgspec`
- **Leak-Proof Dependency Injection** for Databases
- **Auto-Generated Swagger UI** (`/docs`)
- **Background Tasks** built-in
- **Granian**: Rust-based ASGI server.
- **msgspec**: The fastest JSON serialization/validation library.
- **Starlette**: The lightweight ASGI toolkit.


## Quick Start

```python
from bolt import Bolt
from bolt.background import BackgroundTasks

app = Bolt()

@app.get("/")
async def home():
    return {"message": "Hello from Bolt ⚡"}
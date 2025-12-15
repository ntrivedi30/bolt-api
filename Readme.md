# Bolt API Framework

**A high-performance, async Python web framework built on Granian and msgspec.**
Designed for maximum throughput, zero overhead, and developer ergonomics.

---

## Why Bolt?
Most Python frameworks trade performance for ease of use. Bolt does not.
It sits directly on top of **Granian** (Rust-based ASGI) and uses **msgspec** for zero-copy JSON validation, making it significantly faster.

## Features
- ** Blazing Fast:** Built on **Granian** (Rust) and **Starlette**.
- ** Zero-Copy Validation:** Powered by `msgspec`.
- ** Leak-Proof Dependency Injection:** Robust resource management for Databases.
- ** Auto-Generated Docs:** Swagger UI (`/docs`) and ReDoc (`/redoc`) built-in.
- ** Background Tasks:** Fire-and-forget task handling out of the box.

## Installation

**From GitHub (Recommended for now):**
```bash
pip install git+https://github.com/ntrivedi30/bolt-api.git
```

## Quickstart
```python
from bolt import Bolt

app = Bolt()

@app.get("/")
async def home():
    return {"message": "Hello from Bolt ⚡"}
```

## Credits & Acknowledgements
Bolt stands on the shoulders of giants. This framework is possible thanks to these incredible open-source projects:
- Granian: For the blazing fast Rust-based ASGI server foundation.
- msgspec: For the high-performance, zero-copy JSON serialization and validation.
- Starlette: For the robust ASGI toolkit and routing system.
Special thanks to **FastAPI** for inspiring the modern, type-safe design patterns used in this framework.
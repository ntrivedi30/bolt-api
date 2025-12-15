# Bolt API Framework

**A high-performance, async Python web framework built on Granian and msgspec.**
Designed for maximum throughput, zero overhead, and developer ergonomics.

---

## Why Bolt?
Most Python frameworks trade performance for ease of use. Bolt does not.
It sits directly on top of **Granian** (Rust-based ASGI) and uses **msgspec** for zero-copy JSON validation, making it significantly faster.

## Features
- **Blazing Fast:** Built on **Granian** (Rust) and **Starlette**.
- **Zero-Copy Validation:** Powered by `msgspec`.
- **Leak-Proof Dependency Injection:** Robust resource management for Databases.
- **Auto-Generated Docs:** Swagger UI (`/docs`) and ReDoc (`/redoc`) built-in.
- **Background Tasks:** Fire-and-forget task handling.

## Design Philosophy

Bolt is designed with a clear focus on performance-first API development without sacrificing clarity or ergonomics. Its goal is to stay close to the ASGI metal, minimize abstraction overhead, and make costs—both runtime and cognitive—explicit. Bolt favors predictable behavior, explicit resource lifecycles, and fast failure over hidden magic, making it well-suited for long-lived services and high-load production systems.


## Installation

**Install directly from GitHub (recommended for now):**

```bash
pip install git+https://github.com/ntrivedi30/bolt-api.git
```

---

## Quick Start

Create a minimal Bolt application in just a few lines:

```python
from bolt import Bolt

app = Bolt()

@app.get("/")
async def home():
    return {"message": "Hello from Bolt ⚡"}
```

Bolt applications are typically run using **Granian**, which provides the Rust-powered ASGI runtime. For example:

```bash
granian app:app --interface asgi --reload
```

Once running, your API will be available immediately and ready to handle high-throughput traffic.

---

## Credits & Acknowledgements

Bolt is built on top of outstanding open-source projects:

- **Granian** — for the high-performance, Rust-based ASGI server  
- **msgspec** — for ultra-fast, zero-copy JSON serialization and validation  
- **Starlette** — for the robust ASGI toolkit and routing foundation  

Special thanks to **FastAPI** for inspiring modern, type-safe API design patterns that influenced Bolt’s developer experience.

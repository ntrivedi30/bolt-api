# ⚡ Bolt

**A high-performance, async Python web framework built on Granian and msgspec.**
Designed for maximum throughput, zero overhead, and developer ergonomics.

---

## 🚀 Why Bolt?
Most Python frameworks trade performance for ease of use. Bolt does not.
It sits directly on top of **Granian** (Rust-based ASGI) and uses **msgspec** for zero-copy JSON validation, making it significantly faster than standard FastAPI setups while maintaining the same developer experience.

## ✨ Features
- **⚡ Blazing Fast:** Built on **Granian** (Rust) and **Starlette**.
- **📏 Zero-Copy Validation:** Powered by `msgspec` (10-50x faster than Pydantic).
- **🛡️ Leak-Proof Dependency Injection:** Robust resource management for Databases.
- **📑 Auto-Generated Docs:** Swagger UI (`/docs`) and ReDoc (`/redoc`) built-in.
- **⏳ Background Tasks:** Fire-and-forget task handling out of the box.

## 📦 Installation

**From GitHub (Recommended for now):**
```bash
pip install git+https://github.com/ntrivedi30/bolt-api.git
```

## 📦 Quickstart
```python
from bolt import Bolt

app = Bolt()

@app.get("/")
async def home():
    return {"message": "Hello from Bolt ⚡"}

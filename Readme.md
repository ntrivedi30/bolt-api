# ⚡ Bolt Framework

A high-performance, async Python web framework built on **Granian** and **msgspec**.
Designed for maximum throughput and zero overhead.

## 🚀 Features
- **2x Faster than FastAPI** (Benchmarked at ~1,900 req/sec vs 900 req/sec)
- **Zero-Copy Validation** using `msgspec`
- **Leak-Proof Dependency Injection** for Databases
- **Auto-Generated Swagger UI** (`/docs`)
- **Background Tasks** built-in

## Installation

```bash
pip install bolt-api

## 📦 Quick Start

```python
from bolt import Bolt
from bolt.background import BackgroundTasks

app = Bolt()

@app.get("/")
async def home():
    return {"message": "Hello from Bolt ⚡"}
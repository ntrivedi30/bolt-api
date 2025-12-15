#!/bin/bash

echo "=========================================="
echo "🚀 Starting Code Formatting (Bolt Style)"
echo "=========================================="

echo ""
echo "[1/3] Sorting Imports (isort)..."
isort .

echo ""
echo "[2/3] Formatting Code (Black)..."
black .

echo ""
echo "[3/3] Checking for Errors (Flake8)..."
flake8 .

echo ""
echo "=========================================="
echo "✅ Done!"
echo "=========================================="
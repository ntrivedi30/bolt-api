@echo off
echo ==========================================
echo 🚀 Starting Code Formatting
echo ==========================================

echo [1/4] Sorting Imports...
isort .

echo [2/4] Auto-Fixing PEP8 Issues...
autopep8 --in-place --aggressive --recursive .

echo [3/4] Formatting Code (Black)...
black .

echo [4/4] Checking for Logic Errors (Flake8)...
flake8 .

echo ==========================================
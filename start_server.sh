#!/bin/bash
echo "Starting Hospital OpenEnv API Server..."
echo ""
echo "Server will start on: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
cd "$(dirname "$0")"
python main.py

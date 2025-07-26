#!/bin/bash

echo "Starting Health AI API Server..."
echo "Python version: $(python3 --version)"
echo "Working directory: $(pwd)"
echo ""
echo "Server will be available at:"
echo "  - API: http://localhost:8000"
echo "  - Swagger Documentation: http://localhost:8000/docs"
echo "  - ReDoc Documentation: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the FastAPI server
python3 main.py
#!/bin/bash

# Second Brain Research Dashboard - Development Server Initialization
# This script starts both the FastAPI backend and React frontend in parallel

set -e

echo "========================================"
echo "Second Brain Research Dashboard"
echo "Development Environment Setup"
echo "========================================"
echo ""

# Configuration
BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_PORT=3010
BACKEND_DIR="./backend"
FRONTEND_DIR="./frontend"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_section() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check for required directories
if [ ! -d "$BACKEND_DIR" ]; then
    echo "Error: Backend directory not found at $BACKEND_DIR"
    exit 1
fi

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "Error: Frontend directory not found at $FRONTEND_DIR"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    print_section "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    wait $BACKEND_PID 2>/dev/null || true
    wait $FRONTEND_PID 2>/dev/null || true
    print_success "Servers stopped"
}

trap cleanup EXIT

# Start Backend
print_section "Starting Backend (FastAPI)"
print_info "Setting up Python virtual environment..."

if [ ! -d "$BACKEND_DIR/venv" ]; then
    python -m venv "$BACKEND_DIR/venv"
    print_success "Virtual environment created"
fi

# Activate virtual environment
source "$BACKEND_DIR/venv/bin/activate"

# Install backend dependencies
print_info "Installing backend dependencies..."
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip install -q -r "$BACKEND_DIR/requirements.txt"
    print_success "Backend dependencies installed"
else
    print_info "No requirements.txt found, skipping pip install"
fi

# Start backend server
print_info "Starting FastAPI server on port $BACKEND_PORT..."
cd "$BACKEND_DIR"
python -m uvicorn main:app --reload --port $BACKEND_PORT &
BACKEND_PID=$!
cd ..
print_success "Backend started (PID: $BACKEND_PID)"

echo ""

# Start Frontend
print_section "Starting Frontend (React)"
print_info "Installing frontend dependencies..."

cd "$FRONTEND_DIR"

if [ ! -d "node_modules" ]; then
    npm install
    print_success "Frontend dependencies installed"
else
    print_info "node_modules already exists, skipping npm install"
fi

print_info "Starting React dev server on port $FRONTEND_PORT..."
npm run dev &
FRONTEND_PID=$!
cd ..
print_success "Frontend started (PID: $FRONTEND_PID)"

echo ""
print_section "Development Servers Running"
echo ""
print_info "Frontend: http://localhost:$FRONTEND_PORT"
print_info "Backend: http://localhost:$BACKEND_PORT"
print_info "AG-UI endpoint: http://localhost:$BACKEND_PORT/ag-ui/stream"
echo ""
print_section "Running servers... Press Ctrl+C to stop"
echo ""

# Wait for both processes
wait

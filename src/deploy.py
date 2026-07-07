"""
Task 2: Deployment - Week 5
-----------------------------
Deployment script for RAG Educational System.
Starts both Flask backend and Streamlit frontend together.

Run with:
    python deploy.py
"""

import subprocess
import sys
import os
import time

print("=" * 50)
print("  RAG Educational System - Deployment")
print("=" * 50)

# Step 1: Install dependencies
print("\n📦 Installing dependencies...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
print("✅ Dependencies installed!")

# Step 2: Start Flask backend
print("\n🚀 Starting Flask backend on port 5000...")
backend = subprocess.Popen(
    [sys.executable, "app.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
time.sleep(3)

if backend.poll() is None:
    print("✅ Backend is running on http://localhost:5000")
else:
    print("❌ Backend failed to start. Check app.py for errors.")
    sys.exit(1)

# Step 3: Start Streamlit frontend
print("\n🌐 Starting Streamlit frontend on port 8501...")
print("✅ Frontend will open at http://localhost:8501")
print("\n" + "=" * 50)
print("  Both services are running!")
print("  Backend  → http://localhost:5000")
print("  Frontend → http://localhost:8501")
print("  Press CTRL+C to stop both services")
print("=" * 50 + "\n")

try:
    frontend = subprocess.run(
        ["streamlit", "run", "frontend.py"],
    )
except KeyboardInterrupt:
    print("\n🛑 Stopping all services...")
    backend.terminate()
    print("✅ All services stopped.")

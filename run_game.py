#!/usr/bin/env python3
"""
Adventure Game - Integrated Server Launcher
This script starts the Flask server that serves both the API and React frontend.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the backend directory
    backend_dir = Path(__file__).parent / "backend"
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Install requirements
    print("\n" + "="*60)
    print("Adventure Game - Integrated Backend & Frontend Server")
    print("="*60)
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            check=True
        )
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError:
        print("⚠ Warning: Could not install some dependencies, attempting to start anyway...")
    
    # Start the Flask server
    print("\n🚀 Starting the server...")
    print("   Server: http://localhost:5000")
    print("   Serving React frontend from: frontend/build/")
    print("=" * 60 + "\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

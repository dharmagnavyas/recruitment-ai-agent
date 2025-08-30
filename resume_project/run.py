#!/usr/bin/env python3
"""
Recruitment AI Agent - Application Launcher
Run this file to start the FastAPI server
"""

import uvicorn
import os
from pathlib import Path

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['uploads', 'templates', 'static', 'models', 'services']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        
    print("✅ Directory structure verified")

# run.py  (replace check_dependencies() body or just the import loop)

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'python-multipart', 'jinja2',
        'python-docx', 'PyPDF2', 'openai', 'pydantic'
    ]

    # Map package names (pip) to importable module names
    IMPORT_NAME = {
        'python-multipart': 'multipart',
        'python-docx': 'docx',
        'PyPDF2': 'PyPDF2',
        # all others import by the same name (or with - replaced by _)
    }

    missing_packages = []
    for dist in required_packages:
        mod = IMPORT_NAME.get(dist, dist.replace('-', '_'))
        try:
            __import__(mod)
        except ImportError:
            missing_packages.append(dist)

    if missing_packages:
        print("❌ Missing required packages:")
        for p in missing_packages:
            print(f"   - {p}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False

    print("✅ All dependencies satisfied")
    return True


def main():
    """Main application launcher"""
    print("🤖 Recruitment AI Agent")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key-here":
        print("⚠️  OpenAI API key not configured")
        print("   The application will use fallback methods for AI features")
        print("   Set OPENAI_API_KEY environment variable for full AI functionality")
    else:
        print("✅ OpenAI API key configured")
    
    print("\n🚀 Starting server...")
    print("📍 Application will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start the server
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
"""
Quick start script for DataDeck application.
"""
import sys
import subprocess
from pathlib import Path


def check_env_file():
    """Check if .env file exists."""
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("Run 'python setup_env.py' first to create environment configuration.")
        sys.exit(1)
    print("✓ Environment file found")


def run_application():
    """Run the FastAPI application."""
    print("\n" + "=" * 60)
    print("Starting DataDeck Application")
    print("=" * 60 + "\n")
    
    try:
        subprocess.run([
            "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\nApplication stopped.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running application: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    check_env_file()
    
    print("Starting DataDeck...")
    print("API will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    run_application()


if __name__ == "__main__":
    main()


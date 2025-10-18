"""
Setup script to create environment file and directories.
"""
import os
from pathlib import Path
import secrets


def generate_secret_key():
    """Generate a secure random secret key."""
    return secrets.token_urlsafe(32)


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✓ .env file already exists")
        return
    
    secret_key = generate_secret_key()
    
    env_content = f"""# DataDeck Environment Configuration

# Application
APP_NAME=DataDeck
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# API
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1

# Security
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://datadeck:datadeck@localhost:5432/datadeck
DATABASE_ECHO=False

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# OpenAI
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000

# File Storage
STORAGE_TYPE=local
UPLOAD_DIR=./data/uploads
TEMPLATE_DIR=./data/templates
REPORT_DIR=./data/reports

# S3/MinIO
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=datadeck
S3_REGION=us-east-1

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/datadeck.log

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# File Upload Limits
MAX_UPLOAD_SIZE=52428800
ALLOWED_EXTENSIONS=.xlsx,.xls,.csv
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✓ Created .env file with secure SECRET_KEY")


def create_directories():
    """Create necessary directories."""
    directories = [
        "data/uploads",
        "data/templates",
        "data/reports",
        "logs",
        "alembic/versions"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def main():
    """Run setup."""
    print("DataDeck Setup")
    print("=" * 50)
    
    create_env_file()
    create_directories()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OPENAI_API_KEY")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Start database: docker-compose up -d db redis")
    print("4. Run migrations: alembic upgrade head")
    print("5. Start application: python app/main.py")
    print("\nOr use Docker Compose: docker-compose up -d")


if __name__ == "__main__":
    main()


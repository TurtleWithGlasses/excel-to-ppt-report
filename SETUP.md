# DataDeck Setup Guide

This guide will help you set up and run the DataDeck application.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 14+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis**: [Download Redis](https://redis.io/download/)
- **Git**: [Download Git](https://git-scm.com/downloads/)

Or alternatively:
- **Docker Desktop**: [Download Docker](https://www.docker.com/products/docker-desktop/)

## Setup Options

Choose one of the following setup methods:

### Option 1: Quick Setup with Docker (Recommended)

This is the easiest way to get started. Docker will handle all dependencies.

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd excel-to-ppt-report
```

2. **Run the setup script**
```bash
python setup_env.py
```

3. **Edit the .env file**
- Open `.env` in a text editor
- Add your OpenAI API key: `OPENAI_API_KEY=sk-...`
- Save the file

4. **Start all services with Docker**
```bash
docker-compose up -d
```

5. **Access the application**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MinIO Console: http://localhost:9001 (credentials: minioadmin/minioadmin)

6. **Create your first user**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "SecurePassword123"
  }'
```

That's it! You're ready to use DataDeck.

---

### Option 2: Local Development Setup

For development or if you prefer not to use Docker.

#### Step 1: Install Dependencies

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd excel-to-ppt-report
```

2. **Create a virtual environment**

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install Python packages**
```bash
pip install -r requirements.txt
```

#### Step 2: Set Up Database

1. **Install and start PostgreSQL**

On Windows (with installer):
- Download and run the PostgreSQL installer
- Remember the password you set for the postgres user

On macOS (with Homebrew):
```bash
brew install postgresql@14
brew services start postgresql@14
```

On Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install postgresql-14
sudo systemctl start postgresql
```

2. **Create the database**
```bash
# Connect to PostgreSQL
psql -U postgres

# In psql prompt:
CREATE DATABASE datadeck;
CREATE USER datadeck WITH PASSWORD 'datadeck';
GRANT ALL PRIVILEGES ON DATABASE datadeck TO datadeck;
\q
```

#### Step 3: Set Up Redis

On Windows:
- Download Redis for Windows from [GitHub](https://github.com/microsoftarchive/redis/releases)
- Or use Docker: `docker run -d -p 6379:6379 redis:7-alpine`

On macOS:
```bash
brew install redis
brew services start redis
```

On Linux:
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

#### Step 4: Configure Environment

1. **Run the setup script**
```bash
python setup_env.py
```

2. **Edit the .env file**
- Open `.env` in your favorite text editor
- Set `OPENAI_API_KEY=sk-your-actual-api-key`
- Verify `DATABASE_URL` matches your PostgreSQL configuration
- Save the file

#### Step 5: Initialize Database

```bash
# Run database migrations
alembic upgrade head
```

#### Step 6: Run the Application

```bash
# Quick start
python run.py

# Or with more control
python app/main.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## Post-Installation Steps

### 1. Create Your First User

Using the API docs (http://localhost:8000/docs):
1. Navigate to the `/api/v1/auth/register` endpoint
2. Click "Try it out"
3. Enter your details:
```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "YourSecurePassword",
  "role": "admin"
}
```
4. Click "Execute"

Or use curl:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "YourSecurePassword",
    "role": "admin"
  }'
```

### 2. Login and Get Access Token

1. Go to `/api/v1/auth/login` in the docs
2. Use your username and password
3. Copy the `access_token` from the response
4. Click "Authorize" at the top of the docs page
5. Enter: `Bearer <your-access-token>`

Now you can use all authenticated endpoints!

### 3. Create a Test Client

```json
POST /api/v1/clients/
{
  "name": "Test Company",
  "industry": "Technology"
}
```

### 4. Create a Template

```json
POST /api/v1/templates/
{
  "client_id": "<client-uuid-from-previous-step>",
  "name": "Monthly Report Template",
  "structure": {
    "template_name": "Monthly Report",
    "sections": [
      {
        "name": "Executive Summary",
        "type": "text_analysis",
        "data_source": ["Sheet1"],
        "ai_processing": true
      },
      {
        "name": "Data Table",
        "type": "data_table",
        "data_source": ["Sheet1"]
      }
    ]
  }
}
```

### 5. Upload Data

Use the `/api/v1/data/upload` endpoint:
- Select an Excel file (.xlsx, .xls, or .csv)
- Enter the client_id
- Upload

### 6. Generate Your First Report

```json
POST /api/v1/reports/generate
{
  "client_id": "<client-uuid>",
  "template_id": "<template-uuid>",
  "data_upload_id": "<upload-uuid>"
}
```

The report will be generated in the background. Check its status with:
```
GET /api/v1/reports/<report-uuid>
```

Once `status` is `"completed"`, download it:
```
GET /api/v1/reports/<report-uuid>/download
```

---

## Troubleshooting

### Database Connection Error

**Error**: `could not connect to server: Connection refused`

**Solution**:
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env matches your PostgreSQL configuration
- Verify username, password, and database name

### Redis Connection Error

**Error**: `Error connecting to Redis`

**Solution**:
- Ensure Redis is running: `redis-cli ping` (should return "PONG")
- Check REDIS_HOST and REDIS_PORT in .env

### OpenAI API Error

**Error**: `401 Unauthorized` or `Invalid API key`

**Solution**:
- Verify your OPENAI_API_KEY in .env
- Ensure you have credits in your OpenAI account
- Check the API key has the correct permissions

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
- Change the port in .env: `API_PORT=8001`
- Or kill the process using port 8000

On Windows:
```bash
netstat -ano | findstr :8000
taskkill /PID <pid> /F
```

On macOS/Linux:
```bash
lsof -ti:8000 | xargs kill -9
```

---

## Testing the Application

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py -v
```

---

## Development Tools

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Add new field"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

### Code Formatting

```bash
# Format code
black app/

# Check linting
flake8 app/

# Type checking
mypy app/
```

### View Logs

Local:
```bash
tail -f logs/datadeck.log
```

Docker:
```bash
docker-compose logs -f api
docker-compose logs -f worker
```

---

## Next Steps

- Read the [README.md](README.md) for full documentation
- Check out the API documentation at http://localhost:8000/docs
- Explore the example templates in the documentation
- Set up a web frontend (coming soon!)

---

## Getting Help

If you encounter any issues:

1. Check the logs for error messages
2. Ensure all services are running
3. Verify your .env configuration
4. Check the troubleshooting section above
5. Review the API documentation

Happy reporting! 🚀


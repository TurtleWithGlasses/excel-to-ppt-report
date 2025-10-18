# Quick Start Guide
## Running DataDeck Locally

### ✅ Successfully Configured!

Your DataDeck application is now ready to run locally with SQLite.

---

## 🚀 How to Run

### Option 1: Using run.py (Recommended)
```bash
python run.py
```

### Option 2: Using uvicorn directly
```bash
python -m uvicorn app.main:app --reload
```

### Option 3: Using the venv explicitly
```bash
venv/Scripts/python -m uvicorn app.main:app --reload
```

---

## 📋 Access Points

Once running, you can access:

- **Application**: http://127.0.0.1:8000
- **API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative API Docs (ReDoc)**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

---

## 🔧 Configuration

The `.env` file has been created with development defaults:

### Key Settings:
- **Database**: SQLite (`datadeck.db`)
- **API Port**: 8000
- **Debug Mode**: Enabled

### ⚠️ Important:
To use AI features, you need to add your OpenAI API key:

1. Open `.env` file
2. Find the line: `OPENAI_API_KEY=sk-test-key-replace-with-real-key`
3. Replace with your actual OpenAI API key

---

## 🗄️ Database

The application uses **SQLite** for local development.

- Database file: `datadeck.db` (created automatically on first run)
- No PostgreSQL needed for local development
- Migrations are already applied

---

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token

### Clients
- `POST /api/v1/clients/` - Create client
- `GET /api/v1/clients/` - List clients
- `GET /api/v1/clients/{id}` - Get client details

### Templates
- `POST /api/v1/templates/` - Create template
- `GET /api/v1/templates/` - List templates
- `GET /api/v1/templates/{id}` - Get template

### Data Management
- `POST /api/v1/data/upload` - Upload Excel file
- `GET /api/v1/data/` - List uploads
- `GET /api/v1/data/{id}` - Get upload details

### Reports
- `POST /api/v1/reports/generate` - Generate report
- `GET /api/v1/reports/` - List reports
- `GET /api/v1/reports/{id}` - Get report status
- `GET /api/v1/reports/{id}/download` - Download report

**Full API documentation**: http://127.0.0.1:8000/docs

---

## 🧪 Testing the Application

### 1. Check if it's running:
```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{"status":"healthy"}
```

### 2. View API info:
```bash
curl http://127.0.0.1:8000/
```

Expected response:
```json
{
  "app":"DataDeck",
  "version":"1.0.0",
  "status":"running",
  "docs":"/docs"
}
```

### 3. Register a user:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"test@example.com",
    "password":"testpass123"
  }'
```

---

## 📁 Project Structure

```
excel-to-ppt-report/
├── app/                    # Main application
│   ├── api/               # API endpoints
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── main.py           # Application entry
├── data/                  # Data storage
│   ├── uploads/          # Uploaded Excel files
│   ├── templates/        # Template files
│   └── reports/          # Generated reports
├── logs/                  # Application logs
├── datadeck.db           # SQLite database
└── .env                  # Environment configuration
```

---

## 🐛 Troubleshooting

### Application won't start?

1. **Check if port 8000 is in use:**
   ```bash
   netstat -ano | findstr :8000
   ```

2. **Try a different port:**
   ```bash
   python -m uvicorn app.main:app --reload --port 8001
   ```

3. **Check venv is activated:**
   ```bash
   venv\Scripts\activate
   ```

### Database errors?

Delete the database and restart:
```bash
del datadeck.db
python run.py
```

### Import errors?

Reinstall dependencies:
```bash
pip install -r requirements.txt
```

---

## 🔄 What Changes Were Made?

### Fixed Issues:
1. ✅ Added SQLite support (no PostgreSQL needed)
2. ✅ Fixed UUID type compatibility
3. ✅ Fixed JSONB type compatibility
4. ✅ Made OpenAI API key optional
5. ✅ Fixed CORS configuration
6. ✅ Created cross-platform database types

### Files Modified:
- `app/core/config.py` - Updated configuration parsing
- `app/utils/helpers.py` - Added GUID and JSONB types
- `app/models/*.py` - Updated to use cross-platform types
- `app/main.py` - Fixed CORS origins parsing

---

## 📖 Next Steps

1. **Add your OpenAI API key** to `.env` file
2. **Test the API** using the Swagger docs at http://127.0.0.1:8000/docs
3. **Create a client** and upload test data
4. **Generate your first report!**

For detailed documentation, see:
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- [docs/AI_INTEGRATION_GUIDE.md](docs/AI_INTEGRATION_GUIDE.md)
- [docs/DATA_FLOW_GUIDE.md](docs/DATA_FLOW_GUIDE.md)
- [docs/IMPLEMENTATION_CHECKLIST.md](docs/IMPLEMENTATION_CHECKLIST.md)

---

**Happy coding! 🎉**

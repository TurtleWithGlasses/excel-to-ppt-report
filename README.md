# DataDeck

**Automated PPT Report Generation System**

DataDeck is an intelligent system that automates the creation of PowerPoint presentations from Excel data using AI-powered analysis and customizable templates.

## Features

- 📊 **Automated Report Generation**: Convert Excel data to professional PowerPoint presentations
- 🤖 **AI-Powered Insights**: Leverage OpenAI GPT-4 for intelligent data analysis and content generation
- 🎨 **Client-Specific Templates**: Create and manage custom templates for different clients
- 📈 **Data Visualization**: Automatic chart and graph generation from your data
- 🔄 **Historical Data Storage**: Track and analyze trends over time
- 🔐 **Secure & Scalable**: Built with enterprise-grade security and scalability in mind

## Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL
- **Cache/Queue**: Redis, Celery
- **AI**: OpenAI GPT-4
- **Storage**: MinIO/S3
- **Deployment**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 14+
- Redis
- Docker and Docker Compose (optional)

### Installation

#### Option 1: Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd excel-to-ppt-report
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your configuration
# Important: Set your OPENAI_API_KEY, DATABASE_URL, and SECRET_KEY
```

5. **Initialize the database**
```bash
# Run migrations
alembic upgrade head

# Or let the application create tables automatically on first run
```

6. **Create necessary directories**
```bash
mkdir -p data/uploads data/templates data/reports logs
```

7. **Run the application**
```bash
# Development mode with auto-reload
python app/main.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

8. **Access the API**
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

#### Option 2: Docker Compose

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd excel-to-ppt-report
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the services**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- MinIO Console: http://localhost:9001

## Project Structure

```
excel-to-ppt-report/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── clients.py       # Client management
│   │   │   ├── data.py          # Data upload endpoints
│   │   │   ├── reports.py       # Report generation
│   │   │   └── templates.py     # Template management
│   │   └── dependencies.py      # API dependencies
│   ├── core/
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # Database connection
│   │   └── security.py          # Security utilities
│   ├── models/
│   │   ├── user.py              # User model
│   │   ├── client.py            # Client model
│   │   ├── template.py          # Template model
│   │   ├── data_upload.py       # Data upload model
│   │   └── report.py            # Report model
│   ├── schemas/
│   │   └── ...                  # Pydantic schemas
│   ├── services/
│   │   ├── excel_processor.py   # Excel file processing
│   │   ├── ppt_generator.py     # PowerPoint generation
│   │   └── ai_analyzer.py       # AI-powered analysis
│   ├── utils/
│   │   └── helpers.py           # Utility functions
│   └── main.py                  # FastAPI application
├── alembic/                     # Database migrations
├── data/                        # Data storage
│   ├── uploads/                 # Uploaded Excel files
│   ├── templates/               # Template files
│   └── reports/                 # Generated reports
├── logs/                        # Application logs
├── tests/                       # Test suite
├── docker-compose.yml           # Docker services
├── Dockerfile                   # Docker image
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## API Documentation

### Authentication

**Register a new user**
```bash
POST /api/v1/auth/register
{
  "username": "user@example.com",
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Login**
```bash
POST /api/v1/auth/login
Form Data:
  username: user@example.com
  password: securepassword
```

### Client Management

**Create a client**
```bash
POST /api/v1/clients/
{
  "name": "Acme Corporation",
  "industry": "Technology"
}
```

**List clients**
```bash
GET /api/v1/clients/
```

### Template Management

**Create a template**
```bash
POST /api/v1/templates/
{
  "client_id": "uuid",
  "name": "Q4 2024 Report",
  "structure": {
    "template_name": "Q4 2024 Report",
    "sections": [
      {
        "name": "Executive Summary",
        "type": "text_analysis",
        "data_source": ["sheet1.summary_data"],
        "ai_processing": true
      }
    ]
  }
}
```

### Data Upload

**Upload Excel data**
```bash
POST /api/v1/data/upload
Form Data:
  file: <excel_file>
  client_id: <client_uuid>
```

### Report Generation

**Generate a report**
```bash
POST /api/v1/reports/generate
{
  "client_id": "uuid",
  "template_id": "uuid",
  "data_upload_id": "uuid"
}
```

**Download a report**
```bash
GET /api/v1/reports/{report_id}/download
```

## Template Structure

Templates define how your PowerPoint reports will be structured. Here's an example:

```json
{
  "client_id": "uuid",
  "template_name": "Monthly Report",
  "sections": [
    {
      "name": "Executive Summary",
      "type": "text_analysis",
      "data_source": ["sheet1"],
      "ai_processing": true
    },
    {
      "name": "Sales Data",
      "type": "data_table",
      "data_source": ["sheet2.sales"],
      "filters": ["date_range", "region"]
    },
    {
      "name": "Performance Charts",
      "type": "visualization",
      "chart_type": "bar_chart",
      "data_source": ["sheet3.metrics"]
    }
  ]
}
```

## Configuration

Key configuration options in `.env`:

```env
# Application
APP_NAME=DataDeck
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/datadeck

# Security (generate a secure secret key!)
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Storage
STORAGE_TYPE=local
UPLOAD_DIR=./data/uploads
TEMPLATE_DIR=./data/templates
REPORT_DIR=./data/reports
```

## Development

### Running Tests

```bash
pytest tests/ -v --cov=app
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
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

## Deployment

### Production Considerations

1. **Security**
   - Use strong SECRET_KEY
   - Enable HTTPS
   - Configure CORS properly
   - Use environment-specific configurations

2. **Database**
   - Use connection pooling
   - Regular backups
   - Proper indexing

3. **Storage**
   - Use S3 or MinIO for file storage
   - Implement file retention policies
   - Consider CDN for static assets

4. **Monitoring**
   - Set up logging
   - Configure error tracking (e.g., Sentry)
   - Monitor performance metrics

### Docker Production Deployment

```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f

# Scale workers
docker-compose up -d --scale worker=3
```

## Roadmap

- [x] Phase 1: Core functionality
  - [x] Excel processing
  - [x] PPT generation
  - [x] Database models
  - [x] REST API

- [ ] Phase 2: Enhanced Features
  - [ ] Web dashboard UI
  - [ ] Desktop application
  - [ ] Advanced AI features
  - [ ] Real-time preview

- [ ] Phase 3: Enterprise Features
  - [ ] Multi-tenancy
  - [ ] Advanced permissions
  - [ ] API integrations
  - [ ] Analytics dashboard

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## License

This project is proprietary software. All rights reserved.

## Support

For support, please contact your system administrator or create an issue in the repository.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI](https://openai.com/)
- Uses [python-pptx](https://python-pptx.readthedocs.io/)

---

**DataDeck** - Transforming data into insights, automatically.


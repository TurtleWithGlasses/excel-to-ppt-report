# DataDeck Project Overview

## What is DataDeck?

DataDeck is an intelligent automation system that transforms Excel spreadsheets into professional PowerPoint presentations using AI-powered analysis. It's designed to save hours of manual work by automatically:

- Reading and analyzing Excel data
- Generating insights using OpenAI's GPT-4
- Creating beautifully formatted PowerPoint slides
- Applying client-specific templates and branding

## Key Features

### 1. Intelligent Data Processing
- Supports Excel (.xlsx, .xls) and CSV files
- Automatic data type detection
- Data cleaning and validation
- Multi-sheet processing
- Statistical analysis

### 2. AI-Powered Insights
- Executive summary generation
- Trend identification
- Anomaly detection
- Natural language insights
- Context-aware analysis

### 3. Flexible Templating
- Client-specific templates
- Custom section definitions
- Multiple slide types (text, tables, charts)
- Brand customization
- Reusable configurations

### 4. Automated Report Generation
- Background processing
- Multiple output formats
- Batch processing support
- Status tracking
- Download on completion

### 5. Enterprise Ready
- User authentication & authorization
- Multi-client support
- Historical data tracking
- RESTful API
- Docker deployment

## Architecture

```
┌─────────────────────────────────────────────┐
│           User Interface Layer              │
│     (API Docs, Frontend, CLI, etc.)         │
└───────────────┬─────────────────────────────┘
                │
┌───────────────▼─────────────────────────────┐
│           API Layer (FastAPI)               │
│  Authentication │ Clients │ Templates       │
│  Data Upload    │ Reports │ AI Analysis     │
└───────────────┬─────────────────────────────┘
                │
┌───────────────▼─────────────────────────────┐
│         Business Logic Layer                │
│  ExcelProcessor │ PPTGenerator             │
│  AIAnalyzer     │ TemplateEngine           │
└───────────────┬─────────────────────────────┘
                │
┌───────────────▼─────────────────────────────┐
│           Data Layer                        │
│  PostgreSQL │ Redis │ File Storage         │
└─────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Python 3.11+**: Modern Python with type hints
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migrations
- **Pydantic**: Data validation

### Data Processing
- **Pandas**: Data manipulation and analysis
- **OpenPyXL**: Excel file processing
- **python-pptx**: PowerPoint generation
- **Matplotlib/Seaborn**: Data visualization

### AI/ML
- **OpenAI GPT-4**: Natural language processing
- **scikit-learn**: Statistical analysis

### Infrastructure
- **PostgreSQL**: Relational database
- **Redis**: Caching and job queue
- **Celery**: Distributed task queue
- **Docker**: Containerization
- **MinIO**: S3-compatible storage

## Project Structure

```
excel-to-ppt-report/
├── app/                        # Main application
│   ├── api/                   # API routes
│   │   ├── endpoints/        # Endpoint modules
│   │   └── dependencies.py   # Auth dependencies
│   ├── core/                 # Core configuration
│   │   ├── config.py        # Settings management
│   │   ├── database.py      # Database connection
│   │   └── security.py      # Auth utilities
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   │   ├── excel_processor.py
│   │   ├── ppt_generator.py
│   │   └── ai_analyzer.py
│   ├── utils/               # Utility functions
│   └── main.py             # Application entry
├── alembic/                # Database migrations
├── tests/                  # Test suite
├── data/                   # Data storage
│   ├── uploads/           # Uploaded files
│   ├── templates/         # Template files
│   └── reports/           # Generated reports
├── examples/              # Example files
├── logs/                  # Application logs
└── docs/                  # Documentation
```

## Getting Started

### Quick Start (Docker)

```bash
# 1. Setup
python setup_env.py

# 2. Configure
# Edit .env and add your OPENAI_API_KEY

# 3. Start
docker-compose up -d

# 4. Access
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Local Development

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure
python setup_env.py
# Edit .env file

# 3. Start database
docker-compose up -d db redis

# 4. Run migrations
alembic upgrade head

# 5. Start application
python run.py
```

## Usage Flow

### 1. Authentication
```
Register → Login → Get Access Token
```

### 2. Setup
```
Create Client → Create Template → Upload Data
```

### 3. Generate Report
```
Submit Report Request → Wait for Processing → Download PPT
```

### Example Workflow

```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"user","email":"user@example.com","password":"pass123"}'

# Login
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=user&password=pass123" | jq -r '.access_token')

# Create client
CLIENT_ID=$(curl -X POST "http://localhost:8000/api/v1/clients/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Company"}' | jq -r '.id')

# Upload data
UPLOAD_ID=$(curl -X POST "http://localhost:8000/api/v1/data/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@data.xlsx" \
  -F "client_id=$CLIENT_ID" | jq -r '.id')

# Generate report
# (See examples/api_examples.md for complete workflow)
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token

### Clients
- `POST /api/v1/clients/` - Create client
- `GET /api/v1/clients/` - List clients
- `GET /api/v1/clients/{id}` - Get client
- `DELETE /api/v1/clients/{id}` - Delete client

### Templates
- `POST /api/v1/templates/` - Create template
- `GET /api/v1/templates/` - List templates
- `GET /api/v1/templates/{id}` - Get template
- `PUT /api/v1/templates/{id}` - Update template
- `DELETE /api/v1/templates/{id}` - Delete template

### Data
- `POST /api/v1/data/upload` - Upload Excel file
- `GET /api/v1/data/` - List uploads
- `GET /api/v1/data/{id}` - Get upload details
- `DELETE /api/v1/data/{id}` - Delete upload

### Reports
- `POST /api/v1/reports/generate` - Generate report
- `GET /api/v1/reports/` - List reports
- `GET /api/v1/reports/{id}` - Get report status
- `GET /api/v1/reports/{id}/download` - Download report
- `DELETE /api/v1/reports/{id}` - Delete report

## Template Structure

Templates define how your reports are structured:

```json
{
  "template_name": "Quarterly Report",
  "sections": [
    {
      "name": "Executive Summary",
      "type": "text_analysis",
      "data_source": ["Sheet1"],
      "ai_processing": true
    },
    {
      "name": "Financial Data",
      "type": "data_table",
      "data_source": ["Financials"]
    },
    {
      "name": "Performance Chart",
      "type": "visualization",
      "chart_type": "bar_chart",
      "data_source": ["Metrics"]
    }
  ]
}
```

### Section Types

1. **text_analysis**: AI-generated text content
2. **data_table**: Formatted tables from Excel
3. **visualization**: Charts and graphs

### Chart Types
- `bar_chart`: Horizontal bars
- `column_chart`: Vertical bars
- `line_chart`: Line graphs
- `pie_chart`: Pie charts

## Development

### Running Tests
```bash
pytest tests/ -v --cov=app
```

### Code Formatting
```bash
black app/
flake8 app/
mypy app/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Adding New Features

1. **Models**: Add to `app/models/`
2. **Schemas**: Add to `app/schemas/`
3. **Business Logic**: Add to `app/services/`
4. **API Endpoints**: Add to `app/api/endpoints/`
5. **Tests**: Add to `tests/`

## Configuration

Key settings in `.env`:

```env
# Required
SECRET_KEY=<generate-secure-key>
OPENAI_API_KEY=<your-api-key>
DATABASE_URL=postgresql://...

# Optional
DEBUG=True
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=52428800
```

## Deployment

### Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Production Considerations
- Use strong SECRET_KEY
- Enable HTTPS
- Configure proper CORS
- Set up monitoring
- Regular database backups
- Use external storage (S3/MinIO)

## Performance

### Optimization Tips
- Use Redis caching
- Async processing with Celery
- Database connection pooling
- CDN for static assets
- Horizontal scaling with load balancer

### Scaling
```bash
# Scale workers
docker-compose up -d --scale worker=5
```

## Monitoring

### Logs
```bash
# Application logs
tail -f logs/datadeck.log

# Docker logs
docker-compose logs -f api
docker-compose logs -f worker
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env

2. **OpenAI API errors**
   - Verify OPENAI_API_KEY
   - Check API quota/credits

3. **Report generation stuck**
   - Check Celery worker logs
   - Verify Redis is running

See [SETUP.md](SETUP.md) for detailed troubleshooting.

## Security

### Best Practices
- Never commit .env files
- Use strong passwords
- Rotate API keys regularly
- Enable HTTPS in production
- Implement rate limiting
- Regular security updates

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Documentation

- [README.md](README.md) - General overview
- [SETUP.md](SETUP.md) - Setup instructions
- [examples/api_examples.md](examples/api_examples.md) - API usage examples
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- API Docs: http://localhost:8000/docs

## Roadmap

### Phase 1: Foundation ✅
- Core functionality
- REST API
- Basic features

### Phase 2: Enhancement (Q2 2024)
- Web dashboard UI
- Real-time preview
- Advanced AI features
- More chart types

### Phase 3: Enterprise (Q3 2024)
- Multi-tenancy
- Advanced permissions
- Webhook integrations
- Analytics dashboard

### Phase 4: Desktop (Q4 2024)
- Desktop application
- Offline mode
- Sync capabilities

## Support

- Documentation: See docs/ folder
- API Issues: Create GitHub issue
- Email: support@datadeck.example

## License

MIT License - See [LICENSE](LICENSE) file

## Acknowledgments

- FastAPI framework
- OpenAI GPT-4
- python-pptx library
- PostgreSQL
- All contributors

---

**DataDeck** - Transforming data into presentations, intelligently.

Version: 1.0.0 | Last Updated: 2024


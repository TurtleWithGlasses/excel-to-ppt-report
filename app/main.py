"""
DataDeck - Main FastAPI Application
Automated PPT Report Generation System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.endpoints import auth, clients, templates, data, reports

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Automated PPT Report Generation System",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    clients.router,
    prefix=f"{settings.API_PREFIX}/clients",
    tags=["Clients"]
)

app.include_router(
    templates.router,
    prefix=f"{settings.API_PREFIX}/templates",
    tags=["Templates"]
)

app.include_router(
    data.router,
    prefix=f"{settings.API_PREFIX}/data",
    tags=["Data Management"]
)

app.include_router(
    reports.router,
    prefix=f"{settings.API_PREFIX}/reports",
    tags=["Report Generation"]
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    """
    # Initialize database tables
    init_db()
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} started successfully!")


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )


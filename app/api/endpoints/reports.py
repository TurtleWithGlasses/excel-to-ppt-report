"""
Report generation endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import uuid
from app.core.database import get_db
from app.core.config import settings
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.report import Report
from app.models.template import Template
from app.models.data_upload import DataUpload
from app.schemas.report import ReportCreate, ReportResponse
from app.services.excel_processor import ExcelProcessor
from app.services.ppt_generator import PPTGenerator
from app.services.ai_analyzer import AIAnalyzer

router = APIRouter()


def generate_report_task(
    report_id: str,
    template_id: str,
    data_upload_id: str,
    db: Session
):
    """
    Background task to generate a PowerPoint report.
    """
    try:
        # Update report status
        report = db.query(Report).filter(Report.id == report_id).first()
        report.status = "processing"
        db.commit()
        
        # Get template and data upload
        template = db.query(Template).filter(Template.id == template_id).first()
        data_upload = db.query(DataUpload).filter(DataUpload.id == data_upload_id).first()
        
        # Initialize services
        excel_processor = ExcelProcessor()
        ppt_generator = PPTGenerator()
        ai_analyzer = AIAnalyzer()
        
        # Load Excel data
        data_sheets = excel_processor.read_all_sheets(data_upload.file_path)
        
        # Generate AI insights
        ai_insights = ai_analyzer.generate_insights_for_sections(
            template.structure.get('sections', []),
            data_sheets
        )
        
        # Generate PowerPoint
        ppt_generator.generate_from_template(
            template.structure,
            data_sheets,
            ai_insights
        )
        
        # Save presentation
        report_dir = Path(settings.REPORT_DIR)
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_filename = f"report_{report_id}.pptx"
        report_path = report_dir / report_filename
        ppt_generator.save_presentation(str(report_path))
        
        # Update report record
        report.file_path = str(report_path)
        report.status = "completed"
        db.commit()
        
    except Exception as e:
        # Update report status to failed
        report = db.query(Report).filter(Report.id == report_id).first()
        report.status = "failed"
        db.commit()
        raise e


@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def generate_report(
    report_data: ReportCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate a new PowerPoint report from template and data.
    """
    # Validate template exists
    template = db.query(Template).filter(Template.id == report_data.template_id).first()
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Validate data upload exists
    data_upload = db.query(DataUpload).filter(DataUpload.id == report_data.data_upload_id).first()
    if not data_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data upload not found"
        )
    
    # Create report record
    new_report = Report(
        client_id=report_data.client_id,
        template_id=report_data.template_id,
        data_upload_id=report_data.data_upload_id,
        status="pending",
        generated_by=current_user.id
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    # Add background task for report generation
    background_tasks.add_task(
        generate_report_task,
        str(new_report.id),
        str(report_data.template_id),
        str(report_data.data_upload_id),
        db
    )
    
    return new_report


@router.get("/", response_model=List[ReportResponse])
def list_reports(
    client_id: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List all reports, optionally filtered by client.
    """
    query = db.query(Report)
    
    if client_id:
        query = query.filter(Report.client_id == client_id)
    
    reports = query.order_by(Report.generated_at.desc()).offset(skip).limit(limit).all()
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific report by ID.
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report


@router.get("/{report_id}/download")
def download_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Download a generated report file.
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    if report.status != "completed" or not report.file_path:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report is not ready for download"
        )
    
    file_path = Path(report.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found"
        )
    
    return FileResponse(
        path=str(file_path),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=file_path.name
    )


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a report.
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Delete file from disk if it exists
    if report.file_path:
        file_path = Path(report.file_path)
        file_path.unlink(missing_ok=True)
    
    # Delete database record
    db.delete(report)
    db.commit()
    
    return None


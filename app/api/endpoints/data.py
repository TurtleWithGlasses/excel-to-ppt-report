"""
Data upload endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pathlib import Path
import uuid
from app.core.database import get_db
from app.core.config import settings
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.data_upload import DataUpload
from app.schemas.data_upload import DataUploadResponse
from app.services.excel_processor import ExcelProcessor

router = APIRouter()
excel_processor = ExcelProcessor()


@router.post("/upload", response_model=DataUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_data(
    file: UploadFile = File(...),
    client_id: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload an Excel or CSV data file.
    """
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Create upload directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_path = upload_dir / f"{file_id}_{file.filename}"
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Extract data snapshot
    try:
        data_snapshot = excel_processor.extract_data_snapshot(str(file_path))
    except Exception as e:
        # Clean up file on error
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing file: {str(e)}"
        )
    
    # Create database record
    new_upload = DataUpload(
        client_id=client_id,
        file_name=file.filename,
        file_path=str(file_path),
        data_snapshot=data_snapshot,
        uploaded_by=current_user.id
    )
    
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)
    
    return new_upload


@router.get("/", response_model=List[DataUploadResponse])
def list_data_uploads(
    client_id: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List all data uploads, optionally filtered by client.
    """
    query = db.query(DataUpload)
    
    if client_id:
        query = query.filter(DataUpload.client_id == client_id)
    
    uploads = query.order_by(DataUpload.upload_date.desc()).offset(skip).limit(limit).all()
    return uploads


@router.get("/{upload_id}", response_model=DataUploadResponse)
def get_data_upload(
    upload_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific data upload by ID.
    """
    upload = db.query(DataUpload).filter(DataUpload.id == upload_id).first()
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data upload not found"
        )
    
    return upload


@router.delete("/{upload_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_upload(
    upload_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a data upload.
    """
    upload = db.query(DataUpload).filter(DataUpload.id == upload_id).first()
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data upload not found"
        )
    
    # Delete file from disk
    file_path = Path(upload.file_path)
    file_path.unlink(missing_ok=True)
    
    # Delete database record
    db.delete(upload)
    db.commit()
    
    return None


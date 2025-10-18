"""Report schemas."""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid


class ReportBase(BaseModel):
    """Base report schema."""
    client_id: uuid.UUID
    template_id: uuid.UUID
    data_upload_id: uuid.UUID


class ReportCreate(ReportBase):
    """Schema for creating a new report."""
    pass


class ReportResponse(ReportBase):
    """Schema for report response."""
    id: uuid.UUID
    file_path: Optional[str] = None
    status: str
    generated_by: uuid.UUID
    generated_at: datetime
    
    class Config:
        from_attributes = True


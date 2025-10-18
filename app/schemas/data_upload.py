"""Data upload schemas."""
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import uuid


class DataUploadResponse(BaseModel):
    """Schema for data upload response."""
    id: uuid.UUID
    client_id: uuid.UUID
    file_name: str
    file_path: str
    data_snapshot: Optional[Dict[str, Any]] = None
    uploaded_by: uuid.UUID
    upload_date: datetime
    
    class Config:
        from_attributes = True


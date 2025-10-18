"""Template schemas."""
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import uuid


class TemplateBase(BaseModel):
    """Base template schema."""
    name: str
    structure: Dict[str, Any]


class TemplateCreate(TemplateBase):
    """Schema for creating a new template."""
    client_id: uuid.UUID
    version: Optional[int] = 1


class TemplateUpdate(BaseModel):
    """Schema for updating a template."""
    name: Optional[str] = None
    structure: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class TemplateResponse(TemplateBase):
    """Schema for template response."""
    id: uuid.UUID
    client_id: uuid.UUID
    version: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


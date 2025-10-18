"""Client schemas."""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid


class ClientBase(BaseModel):
    """Base client schema."""
    name: str
    industry: Optional[str] = None


class ClientCreate(ClientBase):
    """Schema for creating a new client."""
    pass


class ClientResponse(ClientBase):
    """Schema for client response."""
    id: uuid.UUID
    created_by: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


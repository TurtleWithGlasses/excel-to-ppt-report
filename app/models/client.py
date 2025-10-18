"""Client model."""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.utils.helpers import GUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Client(Base):
    """Client model for managing different organizations."""
    
    __tablename__ = "clients"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    industry = Column(String(100))
    created_by = Column(GUID, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="created_clients")
    templates = relationship("Template", back_populates="client", cascade="all, delete-orphan")
    data_uploads = relationship("DataUpload", back_populates="client", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="client", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Client {self.name}>"


"""Template model."""
import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from app.utils.helpers import GUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Template(Base):
    """Template model for PPT generation templates."""
    
    __tablename__ = "templates"
    
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    client_id = Column(GUID, ForeignKey("clients.id"), nullable=False)
    name = Column(String(255), nullable=False)
    version = Column(Integer, default=1)
    structure = Column(JSONB, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="templates")
    reports = relationship("Report", back_populates="template")
    
    def __repr__(self):
        return f"<Template {self.name} v{self.version}>"


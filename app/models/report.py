"""Report model."""
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Report(Base):
    """Report model for tracking generated PowerPoint reports."""
    
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=False)
    data_upload_id = Column(UUID(as_uuid=True), ForeignKey("data_uploads.id"), nullable=False)
    file_path = Column(Text)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="reports")
    template = relationship("Template", back_populates="reports")
    data_upload = relationship("DataUpload", back_populates="reports")
    generator = relationship("User", back_populates="generated_reports")
    
    def __repr__(self):
        return f"<Report {self.id} - {self.status}>"


"""Data upload model."""
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class DataUpload(Base):
    """Data upload model for tracking Excel file uploads."""
    
    __tablename__ = "data_uploads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    data_snapshot = Column(JSONB)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="data_uploads")
    uploader = relationship("User", back_populates="uploaded_data")
    reports = relationship("Report", back_populates="data_upload")
    
    def __repr__(self):
        return f"<DataUpload {self.file_name}>"


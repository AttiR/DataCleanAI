from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)

    # Dataset metadata
    row_count = Column(Integer, nullable=True)
    column_count = Column(Integer, nullable=True)
    column_info = Column(JSON, nullable=True)

    # Quality metrics
    missing_values_count = Column(Integer, default=0)
    duplicate_rows_count = Column(Integer, default=0)
    outlier_count = Column(Integer, default=0)
    quality_score = Column(Float, default=0.0)

    # Processing status
    status = Column(String(50), default="uploaded")  # uploaded, processing, completed, failed
    processing_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    processing_jobs = relationship("ProcessingJob", back_populates="dataset")

    def __repr__(self):
        return f"<Dataset(id={self.id}, filename='{self.filename}')>"

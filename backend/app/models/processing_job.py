from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)

    # Job configuration
    job_type = Column(String(100), nullable=False)  # analyze, clean, transform
    configuration = Column(JSON, nullable=True)

    # Processing results
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    progress = Column(Integer, default=0)  # 0-100

    # Results and metrics
    results = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    output_file_path = Column(String(500), nullable=True)

    # Error handling
    error_message = Column(Text, nullable=True)
    error_traceback = Column(Text, nullable=True)

    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    dataset = relationship("Dataset", back_populates="processing_jobs")

    def __repr__(self):
        return f"<ProcessingJob(id={self.id}, type='{self.job_type}')>"

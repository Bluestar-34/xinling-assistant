from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

# Create SQLite database engine
engine = create_engine('sqlite:///chat.db', echo=True)

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(36), ForeignKey("sessions.id"))
    role = Column(String(10))  # user or assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    session = relationship("Session", back_populates="messages")

class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("sessions.id"))
    assessment_type = Column(String(50))  # e.g., "PHQ-9", "GAD-7"
    status = Column(String(20))  # "in_progress", "completed"
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    total_score = Column(Integer, nullable=True)
    interpretation = Column(JSON, nullable=True)  # Store assessment results
    answers = relationship("AssessmentAnswer", back_populates="assessment_session", cascade="all, delete-orphan")

class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"
    
    id = Column(Integer, primary_key=True)
    assessment_session_id = Column(String(36), ForeignKey("assessment_sessions.id"))
    question_id = Column(Integer)  # Question number/index
    answer = Column(Integer)  # User's answer (0-3 for PHQ-9)
    created_at = Column(DateTime, default=datetime.utcnow)
    assessment_session = relationship("AssessmentSession", back_populates="answers") 
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# ====================== RESUME MODELS (matches your existing MySQL tables) ======================
class Resume(Base):
    __tablename__ = "resume"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    agency = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    open_date = Column(DateTime)
    close_date = Column(DateTime)
    found_skills = Column(String(255))
    skills = Column(String(255))          # you can keep this or remove later

    # Relationship to skills table
    resume_skills = relationship("ResumeSkill", back_populates="resume")


class ResumeSkill(Base):
    __tablename__ = "resume_skills"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resume.id"))   # ← Correct foreign key
    skill = Column(String(100))

    resume = relationship("Resume", back_populates="resume_skills")



# ====================== DATABASE CONNECTION ======================
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)   # Safe even if tables already exist
    print("✅ Database tables are ready (existing tables were skipped)")






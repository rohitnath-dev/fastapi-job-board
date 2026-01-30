from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------- DATABASE ----------------
DATABASE_URL = "sqlite:///./jobs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ---------------- DB MODEL ----------------
class JobDB(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    salary = Column(Integer)
    description = Column(Text)
    skills = Column(String)   # stored as comma-separated
    favourite = Column(Boolean, default=False)

Base.metadata.create_all(engine)

# ---------------- PYDANTIC SCHEMAS ----------------
class Job(BaseModel):
    title: str
    company: str
    location: str
    salary: int
    description: str
    skills: List[str]

class JobResponse(Job):
    id: int
    favourite: bool

    class Config:
        orm_mode = True

# ---------------- APP ----------------
app = FastAPI(title="AI Job Board API PRO")

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- DEFAULT JOB SEEDER ----------------
def seed_jobs():
    db = SessionLocal()
    if db.query(JobDB).count() == 0:
        default_jobs = [
            JobDB(
                title="AI Intern",
                company="CloudBrain",
                location="Remote",
                salary=15000,
                description="Work on AI models, APIs, and backend pipelines.",
                skills="python,ml,fastapi,numpy",
            ),
            JobDB(
                title="Machine Learning Engineer",
                company="NeuroTech Labs",
                location="Bangalore",
                salary=80000,
                description="Build and deploy ML pipelines and predictive models.",
                skills="python,scikit-learn,pandas,mlops",
            ),
            JobDB(
                title="Data Scientist",
                company="DataHive",
                location="Mumbai",
                salary=70000,
                description="Analyze data and build dashboards.",
                skills="python,statistics,pandas,matplotlib",
            ),
            JobDB(
                title="Backend Engineer (AI Systems)",
                company="DeepStack",
                location="Remote",
                salary=90000,
                description="Develop scalable APIs for AI systems.",
                skills="python,fastapi,sqlalchemy,docker",
            ),
            JobDB(
                title="Prompt Engineer",
                company="GenAI Labs",
                location="Remote",
                salary=60000,
                description="Design prompts and AI workflows.",
                skills="llm,prompt-engineering,ai-tools",
            )
        ]
        db.add_all(default_jobs)
        db.commit()
    db.close()

# Run seeder on startup
seed_jobs()

# ---------------- ROUTES ----------------

@app.get("/")
def home():
    return {"message": "AI Job Board API is running"}

# Add job manually
@app.post("/jobs")
def add_job(job: Job):
    db = SessionLocal()
    new_job = JobDB(
        title=job.title,
        company=job.company,
        location=job.location,
        salary=job.salary,
        description=job.description,
        skills=",".join(job.skills),
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    db.close()
    return new_job

# Get all jobs
@app.get("/jobs")
def get_jobs():
    db = SessionLocal()
    jobs = db.query(JobDB).all()
    db.close()
    return jobs

# Search jobs by text
@app.get("/jobs/search")
def search_jobs(query: str):
    db = SessionLocal()
    jobs = db.query(JobDB).filter(
        (JobDB.title.contains(query)) |
        (JobDB.description.contains(query)) |
        (JobDB.skills.contains(query))
    ).all()
    db.close()
    return jobs

# Mark favourite
@app.post("/jobs/{job_id}/favourite")
def add_favourite(job_id: int):
    db = SessionLocal()
    job = db.query(JobDB).filter(JobDB.id == job_id).first()
    if not job:
        db.close()
        raise HTTPException(404, "Job not found")
    job.favourite = True
    db.commit()
    db.close()
    return {"msg": "Added to favourites"}

# Remove favourite
@app.post("/jobs/{job_id}/unfavourite")
def remove_favourite(job_id: int):
    db = SessionLocal()
    job = db.query(JobDB).filter(JobDB.id == job_id).first()
    if not job:
        db.close()
        raise HTTPException(404, "Job not found")
    job.favourite = False
    db.commit()
    db.close()
    return {"msg": "Removed from favourites"}

# Get favourites
@app.get("/favourites")
def get_favourites():
    db = SessionLocal()
    jobs = db.query(JobDB).filter(JobDB.favourite == True).all()
    db.close()
    return jobs

# ---------------- SORTING ----------------

@app.get("/jobs/salary_asc")
def get_jobs_salary_asc():
    db = SessionLocal()
    jobs = db.query(JobDB).order_by(JobDB.salary.asc()).all()
    db.close()
    return jobs

@app.get("/jobs/salary_desc")
def get_jobs_salary_desc():
    db = SessionLocal()
    jobs = db.query(JobDB).order_by(JobDB.salary.desc()).all()
    db.close()
    return jobs

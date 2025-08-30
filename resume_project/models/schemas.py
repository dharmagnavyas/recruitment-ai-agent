from pydantic import BaseModel
from typing import List, Optional

class JobDescriptionInput(BaseModel):
    job_title: str
    years_experience: str
    must_have_skills: List[str]
    company_name: str
    employment_type: str
    industry: str
    location: str

class JobDescriptionResponse(BaseModel):
    job_description: str
    success: bool
    message: str

class CandidateResult(BaseModel):
    filename: str
    score: int
    missing_skills: List[str]
    remarks: str
    
    class Config:
        from_attributes = True

class EmailResponse(BaseModel):
    email_content: str
    success: bool
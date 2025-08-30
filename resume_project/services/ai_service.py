# ai_service.py
import os
from anthropic import Anthropic

_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-7-sonnet-2025-06-06")
_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def _claude(system: str, user: str, max_tokens: int = 1200, temperature: float = 0.3) -> str:
    msg = _client.messages.create(
        model=_MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    # Concatenate text parts
    return "".join([p.text for p in msg.content if getattr(p, "type", "") == "text"]).strip()

def generate_job_description(payload: dict) -> str:
    user = (
        f"Title: {payload.get('title','')}\n"
        f"Years of experience: {payload.get('years_of_experience','')}\n"
        f"Must-have skills: {payload.get('must_have_skills','')}\n"
        f"Company: {payload.get('company','')}\n"
        f"Employment type: {payload.get('employment_type','')}\n"
        f"Industry: {payload.get('industry','')}\n"
        f"Location: {payload.get('location','')}\n\n"
        "Write a concise, structured job description with headings: Overview, Responsibilities, Requirements, "
        "Preferred Qualifications, About the Company, Benefits. Use bullet points. Keep it 250–450 words."
    )
    system = "You are an expert technical recruiter who writes clear, inclusive job descriptions."
    return _claude(system, user, max_tokens=1600)

def generate_interview_email(candidate_name: str, jd_text: str) -> str:
    system = "You write short, friendly recruiting emails."
    user = (
        f"Candidate: {candidate_name}\n"
        "Write an interview invitation email (subject + body) based on this JD summary:\n"
        f"{jd_text[:2500]}"
    )
    return _claude(system, user, max_tokens=600)

def generate_rejection_email(candidate_name: str, jd_text: str) -> str:
    system = "You write empathetic, brief rejection emails that keep the door open."
    user = (
        f"Candidate: {candidate_name}\n"
        "Write a polite rejection email (subject + body). Do not include private feedback."
    )
    return _claude(system, user, max_tokens=400)

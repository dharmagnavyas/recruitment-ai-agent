# main.py
from __future__ import annotations

import io
import os
from typing import List, Optional

from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ---------------------- Optional project helpers ----------------------
def _safe_imports():
    mods = {}
    try:
        import ai_service  # type: ignore
        mods["ai_service"] = ai_service
    except Exception:
        mods["ai_service"] = None
    try:
        import document_processor  # type: ignore
        mods["document_processor"] = document_processor
    except Exception:
        mods["document_processor"] = None
    try:
        import candidate_matcher  # type: ignore
        mods["candidate_matcher"] = candidate_matcher
    except Exception:
        mods["candidate_matcher"] = None
    return mods

mods = _safe_imports()

# ---------------------- Utilities (with fallbacks) ----------------------
def extract_text_from_upload(file: UploadFile) -> str:
    dp = mods.get("document_processor")
    if dp and hasattr(dp, "extract_text_from_file"):
        try:
            return dp.extract_text_from_file(file)  # type: ignore[attr-defined]
        except Exception:
            pass

    name = (file.filename or "").lower()
    content = file.file.read()
    file.file.seek(0)

    if name.endswith(".pdf"):
        try:
            from PyPDF2 import PdfReader  # type: ignore
            reader = PdfReader(io.BytesIO(content))
            parts = [(p.extract_text() or "") for p in reader.pages]
            return "\n".join(parts).strip()
        except Exception:
            return ""
    if name.endswith(".docx"):
        try:
            import docx  # python-docx
            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs).strip()
        except Exception:
            return ""
    if name.endswith(".txt"):
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    return content.decode("utf-8", errors="ignore")


def generate_job_description(payload: dict) -> str:
    ai = mods.get("ai_service")
    if ai and hasattr(ai, "generate_job_description"):
        try:
            return ai.generate_job_description(payload)  # type: ignore[attr-defined]
        except Exception:
            pass

    title = payload.get("title") or "Role"
    yoe = payload.get("years_of_experience") or "2+"
    skills = payload.get("must_have_skills") or ""
    company = payload.get("company") or "Your Company"
    emp_type = payload.get("employment_type") or "Full-time"
    industry = payload.get("industry") or "General"
    location = payload.get("location") or "Remote"

    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    lines = [
        f"**{title}**", "",
        f"**Company:** {company}",
        f"**Location:** {location}",
        f"**Employment Type:** {emp_type}",
        f"**Industry:** {industry}", "",
        "**Job Overview:**",
        f"We are seeking a qualified {title} to join our team. The ideal candidate will have {yoe} years of experience and strong expertise in the required technologies.", "",
        "**Key Responsibilities:**",
        "- Develop and maintain high-quality software and systems",
        "- Collaborate with cross-functional teams",
        "- Participate in code reviews and technical discussions",
        "- Contribute to project planning and estimation", "",
        "**Required Qualifications:**",
        f"- {yoe} years of professional experience",
        "- Strong proficiency in core technologies",
        "- Bachelor's degree in Computer Science or related field (or equivalent experience)",
        "- Excellent problem-solving and communication skills",
    ]
    if skills_list:
        lines += ["", "**Must-have skills:**"]
        lines += [f"- {s}" for s in skills_list]
    lines += ["", "Join our team and help us build great products in a collaborative environment!"]
    return "\n".join(lines)


def score_candidates(jd_text: str, resume_blobs: List[tuple[str, str]]):
    cm = mods.get("candidate_matcher")
    if cm and hasattr(cm, "match_candidates"):
        try:
            candidates = cm.match_candidates(jd_text, resume_blobs)  # type: ignore[attr-defined]
        except Exception:
            candidates = None
    else:
        candidates = None

    if candidates is None:
        import re
        skills = set(
            s.lower().strip()
            for s in re.split(r"[^a-zA-Z0-9\+\#\.]+", jd_text)
            if len(s.strip()) > 1
        )

        def score_one(text: str) -> int:
            words = set(
                s.lower().strip()
                for s in re.split(r"[^a-zA-Z0-9\+\#\.]+", text)
                if len(s.strip()) > 1
            )
            overlap = len(skills & words)
            denom = max(len(skills), 1)
            return int(min(100, round((overlap / denom) * 100)))

        fallback = []
        for name, text in resume_blobs:
            sc = score_one(text)
            missing = list((skills - set(text.lower().split())))[:8]
            if sc >= 80:
                remark = "Strong alignment with required terminology."
            elif sc >= 60:
                remark = "Good overlap with JD keywords."
            elif sc >= 40:
                remark = "Partial match—consider screening."
            else:
                remark = "Low keyword overlap with JD."
            fallback.append(
                {"name": name, "filename": name, "score": sc, "missing_skills": missing, "remarks": remark}
            )
        candidates = sorted(fallback, key=lambda x: x["score"], reverse=True)

    # Simple emails; swap with ai_service if you have it
    def interview_email(name: str) -> str:
        return (
            f"Subject: Interview Invitation\n\n"
            f"Hi {name.rsplit('.',1)[0].replace('_',' ')},\n\n"
            f"Thanks for applying. Your background appears to align well with our role.\n"
            f"We'd love to schedule a 30–45 minute interview this week.\n\n"
            f"Please share your availability.\n\nBest regards,\nRecruiting Team"
        )

    def rejection_email(name: str) -> str:
        return (
            f"Subject: Application Update\n\n"
            f"Hi {name.rsplit('.',1)[0].replace('_',' ')},\n\n"
            f"Thank you for your interest. After careful review, we will not be moving forward at this time.\n"
            f"We appreciate your time and encourage you to apply for future openings.\n\nBest wishes,\nRecruiting Team"
        )

    best = candidates[0]["name"] if candidates else "Candidate"
    interview = interview_email(best)
    rejections = [{"name": c["name"], "email": rejection_email(c["name"])} for c in candidates[1:]]
    return candidates, interview, rejections

# ---------------------- FastAPI app ----------------------
app = FastAPI(title="Recruitment AI Agent", version="1.0.1")

if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, tags=["UI"])
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "jd_text": ""})

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)

# ---------------------- JD endpoints ----------------------
@app.post("/generate-jd", tags=["Job Description"])
async def generate_jd(payload: dict):
    return JSONResponse({"job_description": generate_job_description(payload or {})})

@app.post("/upload-jd", tags=["Job Description"])
async def upload_jd(file: UploadFile = File(..., description="JD file (PDF/DOC/DOCX)")):
    return JSONResponse({"job_description": extract_text_from_upload(file)})

# ---------- Aliases for older/new frontend names ----------
# /upload-jd-file -> same as /upload-jd, accept "file" or "jd_file"
@app.post("/upload-jd-file", tags=["Job Description"])
async def upload_jd_file(
    file: Optional[UploadFile] = File(None),
    jd_file: Optional[UploadFile] = File(None),
):
    up = file or jd_file
    if not up:
        return JSONResponse({"detail": "Provide a JD file under field 'file' or 'jd_file'."}, status_code=422)
    return JSONResponse({"job_description": extract_text_from_upload(up)})

# ---------------------- Matching endpoints ----------------------
@app.post("/process-resumes", response_class=HTMLResponse, tags=["Matching"])
async def process_resumes(
    request: Request,
    resumes: List[UploadFile] = File(..., description="Resume files (max 10)"),
    jd_text: str = Form(..., description="Job Description text"),
):
    if len(resumes) > 10:
        return JSONResponse({"detail": "Please upload at most 10 resumes."}, status_code=422)

    blobs: List[tuple[str, str]] = []
    for f in resumes:
        blobs.append(((f.filename or "candidate"), extract_text_from_upload(f)))

    candidates, interview_email, rejection_emails = score_candidates(jd_text, blobs)
    ctx = {
        "request": request,
        "results": candidates,
        "candidates": candidates,
        "interview_email": interview_email,
        "rejection_emails": rejection_emails,
        "jd_text": jd_text,
        "job_description": jd_text,
    }
    return templates.TemplateResponse("results.html", ctx)

# Alias: /evaluate-candidates -> same behavior as /process-resumes
@app.post("/evaluate-candidates", response_class=HTMLResponse, tags=["Matching"])
async def evaluate_candidates(
    request: Request,
    # tolerate multiple possible field names from older UIs
    resumes: Optional[List[UploadFile]] = File(None),
    files: Optional[List[UploadFile]] = File(None),
    jd_text: Optional[str] = Form(None),
    job_description: Optional[str] = Form(None),
):
    all_files: List[UploadFile] = []
    if resumes: all_files.extend(resumes)
    if files: all_files.extend(files)
    jd = (jd_text or job_description or "").strip()

    if not jd:
        return JSONResponse({"detail": "Missing job description (jd_text)."}, status_code=422)
    if not all_files:
        return JSONResponse({"detail": "No resumes uploaded (use field 'resumes' or 'files')."}, status_code=422)
    if len(all_files) > 10:
        return JSONResponse({"detail": "Please upload at most 10 resumes."}, status_code=422)

    blobs = [((f.filename or "candidate"), extract_text_from_upload(f)) for f in all_files]
    candidates, interview_email, rejection_emails = score_candidates(jd, blobs)
    ctx = {
        "request": request,
        "results": candidates,
        "candidates": candidates,
        "interview_email": interview_email,
        "rejection_emails": rejection_emails,
        "jd_text": jd,
        "job_description": jd,
    }
    return templates.TemplateResponse("results.html", ctx)

# Health (optional)
@app.get("/health", tags=["Ops"])
def health():
    return {"status": "ok"}

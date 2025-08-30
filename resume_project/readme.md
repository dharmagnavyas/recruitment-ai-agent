---

# 🤖 Recruitment AI Agent

A FastAPI web app that lets recruiters **generate or upload a Job Description**, **analyze up to 10 resumes**, compute **match scores (0–100)**, surface **missing skills**, and auto-draft **interview/rejection emails**—now using **Anthropic Claude 3.7 Sonnet** for the AI bits.

---

## 🌟 Features

* **3 JD input modes**

  * 🧠 **AI-generated JD** from title, YOE, skills, company, type, industry, location
  * ✍️ **Manual** paste/edit
  * 📄 **File upload** (PDF/DOC/DOCX → text extraction)

* **Resume intelligence**

  * Upload **up to 10** resumes (PDF/DOC/DOCX/TXT)
  * Robust text extraction (PyPDF2 / python-docx)
  * **Match score** out of 100 + **missing skills** + **remarks**
  * Best candidate highlighted

* **AI emails**

  * Personalized **interview invite** for the top match
  * Polite **rejection emails** for others
  * Copy/open-in-mail buttons

* **Nice UI**

  * Bootstrap 5, responsive, progress spinners
  * Full results page with analytics

---

## 🔧 Tech & Models

* **Backend:** FastAPI + Uvicorn

* **Templating:** Jinja2 (pages in `templates/`)

* **AI:** **Anthropic Claude 3.7 Sonnet** via `anthropic` SDK
  Used for:

  1. **JD generation**
  2. **Interview email**
  3. **Rejection emails**

* **Matching logic:**

  * If you have a custom `candidate_matcher.py`, it’s used.
  * Otherwise a **deterministic keyword fallback** computes scores & missing skills—so the app works even without an API key.

**Why Claude 3.7 Sonnet?**

* High quality writing for JDs and emails
* Strong instruction-following; consistent, business-ready tone
* Good latency/price balance for interactive apps
* Easy Python SDK

---

## 📁 Project Structure

```
recruitment-ai-agent/
├── main.py
├── requirements.txt
├── README.md
├── ai_service.py                 # Claude integration (JD + emails)
├── candidate_matcher.py          # optional: custom scoring (else fallback)
├── document_processor.py         # file text extraction helpers
├── schemas.py                    # (optional) pydantic models
├── templates/
│   ├── index.html                # upload/generate JD + upload resumes
│   └── results.html              # candidate rankings + emails
└── static/                       # (optional) assets
```

> Make sure you only keep **one** `index.html` (the app’s home). Old templates that post to `/evaluate-candidates` should be removed—this app uses **`/process-resumes`** only.

---

## 🧩 Requirements & Installation

### Prerequisites

* Python **3.9+** recommended

### Install

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include (at minimum):

```
fastapi
uvicorn[standard]
jinja2
python-multipart
PyPDF2
python-docx
anthropic
```

---

## 🔑 Configuration (Claude)

Set your Anthropic API key as an environment variable:

**macOS/Linux**

```bash
export ANTHROPIC_API_KEY="your_rotated_key"
export ANTHROPIC_MODEL="claude-3-7-sonnet-2025-06-06"   # optional: default used if unset
```

**Windows (PowerShell)**

```powershell
$env:ANTHROPIC_API_KEY="your_rotated_key"
$env:ANTHROPIC_MODEL="claude-3-7-sonnet-2025-06-06"
```

> Do **not** hard-code keys. Never commit them. Rotate any previously exposed keys.

---

## 🚀 Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open: **[http://localhost:8000/](http://localhost:8000/)**
API docs: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🧭 How to Use (Quick Start)

1. **Open the app** at `http://localhost:8000/` (don’t open HTML files directly from disk).
2. **Provide a JD**

   * Click **Extract Text** to upload a JD file **or**
   * Fill the **Generate JD** form → **Generate JD** **or**
   * Paste/edit in the **JD Editor**.
3. **Upload resumes** (PDF/DOC/DOCX/TXT) — up to **10** files.
4. Click **Evaluate Candidates**.
   You’ll be taken to the **results** page with scores, missing skills, remarks, and emails.

---

## 🔌 API Endpoints

* `GET /` → Render `index.html`
* `POST /upload-jd` → **form-data**: `file` → returns `{ job_description }`
* `POST /generate-jd` → **JSON** with JD params → returns `{ job_description }`
* `POST /process-resumes` → **form-data**:

  * `resumes` (multiple files)
  * `jd_text` (string)
    → returns **rendered HTML** (`results.html`)

**Form keys (important):**

| Endpoint           | Field        | Type        |
| ------------------ | ------------ | ----------- |
| `/upload-jd`       | `file`       | file        |
| `/generate-jd`     | JSON payload | object      |
| `/process-resumes` | `resumes`    | file\[]     |
| `/process-resumes` | `jd_text`    | string (JD) |

**cURL samples**

```bash
# Generate JD
curl -X POST http://localhost:8000/generate-jd \
  -H "Content-Type: application/json" \
  -d '{"title":"AI Engineer","years_of_experience":"2-4","must_have_skills":"Python, FastAPI, LLMs","company":"Acme AI","employment_type":"Full-time","industry":"AI","location":"Remote"}'
```

```bash
# Upload JD file
curl -X POST http://localhost:8000/upload-jd \
  -F "file=@./samples/jd/AI_Engineer.pdf"
```

```bash
# Process resumes
curl -X POST http://localhost:8000/process-resumes \
  -F "jd_text=$(cat jd.txt)" \
  -F "resumes=@./samples/resumes/Alice.pdf" \
  -F "resumes=@./samples/resumes/Bob.docx"
```

---

## 🧠 AI Logic

* **JD Generation (Claude)**
  `ai_service.py → generate_job_description(payload)`
  Produces a concise, structured JD (Overview, Responsibilities, Requirements, Preferred, etc.).

* **Emails (Claude)**

  * `generate_interview_email(name, jd_text)`
  * `generate_rejection_email(name, jd_text)`

* **Matching**

  * If `candidate_matcher.py` exists with `match_candidates(jd_text, resumes)`, it’s used.
  * Otherwise, fallback **keyword-based** scoring:

    * Tokenize JD & resume text → overlap ratio → **score(0–100)**
    * Derive **missing skills** from JD terms not present in resume
    * Generate simple **remarks** based on score bands

This ensures the app is usable even without an AI key.

---

## 🧪 Samples

Include a small `/samples` folder in your repo:

```
samples/
├── jd/
│   └── AI_Engineer_Job_Description.pdf
└── resumes/
    ├── Alice_SWE.pdf
    ├── Bob_DataEngineer.docx
    └── Carol_MLE.pdf
```

---

## 🛠 Troubleshooting

**422 Unprocessable Entity when evaluating**

* You’re likely using an **old template** posting to `/evaluate-candidates`.
  Use the new UI (it posts to **`/process-resumes`**).
* Make sure **form keys** are correct: `resumes` (one per file) + `jd_text` (non-empty).
* In DevTools → **Network**, click the request and confirm form data names/values.
* Don’t open `templates/index.html` from disk (`file://`). Always use `http://localhost:8000/`.

**JD not appearing after upload**

* Endpoint must be `/upload-jd` with **field name `file`**.
* See server logs for errors.

**Claude errors**

* Verify `ANTHROPIC_API_KEY` is set and valid.
* Network must allow outbound HTTPS.
* The app falls back for matching even if the AI key is missing.

---

## 🔒 Security

* Never commit API keys; use env vars or a `.env` that’s in `.gitignore`.
* Uploaded files are processed transiently; avoid storing PII in production.
* Validate and limit file types/size in production.

---

## 🧭 Roadmap

* Optional embeddings for semantic matching
* ATS/webhook integrations
* Persistent storage (Postgres)
* Multi-language support
* Calendar scheduling links in interview emails

---

**Built with:** FastAPI • Jinja2 • Bootstrap • Anthropic Claude 3.7 Sonnet • PyPDF2 • python-docx

---


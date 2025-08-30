# 🤖 Recruitment AI Agent

A comprehensive AI-powered recruitment system built with FastAPI that intelligently matches candidates to job descriptions, generates personalized emails, and provides detailed candidate analysis.

## 🌟 Features

- **3 Ways to Input Job Descriptions:**
  - 📝 AI-powered JD generation from parameters
  - ✍️ Manual text input
  - 📄 File upload (PDF, DOC, DOCX)

- **Smart Resume Processing:**
  - Upload up to 10 resumes simultaneously
  - Extract text from PDF, DOC, and DOCX files
  - AI-powered candidate scoring (0-100)
  - Identify missing skills and qualifications

- **Automated Email Generation:**
  - Personalized interview invitations for top candidates
  - Professional rejection emails for other applicants
  - Ready-to-send email templates

- **Professional Interface:**
  - Responsive web design
  - Real-time processing feedback
  - Visual candidate ranking
  - Detailed analytics and statistics

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (optional - fallback methods included)

### Installation

1. **Clone or download the project files:**
```bash
# Create project directory
mkdir recruitment-ai-agent
cd recruitment-ai-agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create directory structure:**
```bash
mkdir -p models services templates uploads static
```

4. **Set up environment variables (optional):**
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

5. **Place all files in their respective directories:**
```
recruitment-ai-agent/
├── main.py
├── requirements.txt
├── README.md
├── models/
│   └── schemas.py
├── services/
│   ├── ai_service.py
│   ├── document_processor.py
│   └── candidate_matcher.py
├── templates/
│   ├── index.html
│   └── results.html
├── uploads/ (created automatically)
└── static/ (created automatically)
```

## 🚀 How to Run

1. **Start the application:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Access the application:**
Open your browser and navigate to: `http://localhost:8000`

3. **API Documentation:**
View the interactive API docs at: `http://localhost:8000/docs`

## 🔍 How It Works

### 1. Job Description Processing
The system accepts job descriptions through three methods:

**AI Generation:** Provide job parameters (title, experience, skills, etc.) and the AI creates a comprehensive job description.

**Manual Input:** Paste or type the job description directly into the textarea.

**File Upload:** Upload PDF, DOC, or DOCX files and extract the text automatically.

### 2. Resume Analysis
- Upload multiple resume files (PDF, DOC, DOCX)
- Extract text content using specialized document processors
- Send resume content and job description to AI for analysis

### 3. Candidate Matching Algorithm
Each candidate receives:
- **Score (0-100):** Overall match percentage
- **Missing Skills:** Specific skills mentioned in JD but not found in resume
- **Remarks:** AI-generated insights about strengths and gaps

### 4. Email Generation
- **Best Candidate:** Receives a personalized interview invitation
- **Other Candidates:** Get respectful rejection emails
- All emails are professionally formatted and ready to send

## 🧠 AI Model Choice and Implementation

### Primary AI Model: OpenAI GPT-3.5-turbo

**Why GPT-3.5-turbo?**
- **Cost Effective:** Lower cost per token compared to GPT-4
- **Fast Response Times:** Suitable for real-time web applications
- **Strong Language Understanding:** Excellent for resume analysis and email generation
- **Consistent Output:** Reliable formatting for structured responses

### AI Integration Points:

1. **Job Description Generation:**
   - Input: Job parameters (title, experience, skills, etc.)
   - Output: Professional, comprehensive job description
   - Fallback: Template-based generation if API fails

2. **Resume-JD Matching:**
   - Input: Resume text + Job description
   - Processing: Semantic analysis of skills, experience, and requirements
   - Output: Structured scoring with missing skills and remarks

3. **Email Generation:**
   - Input: Candidate name + Job details
   - Output: Personalized interview/rejection emails
   - Fallback: Template-based emails with candidate personalization

### Fallback Strategy:
If OpenAI API is unavailable or not configured:
- **Job Generation:** Uses professional templates with parameter substitution
- **Resume Matching:** Employs keyword-based matching algorithms
- **Email Generation:** Uses predefined templates with dynamic content

This ensures the application remains functional even without AI API access.

## 🧪 Example Test Files

### Sample Job Description
```
Senior Python Developer

Company: Tech Solutions Inc.
Location: San Francisco, CA
Employment Type: Full-time
Industry: Technology

We are seeking an experienced Senior Python Developer to join our growing team...

Required Skills:
- Python, Django, Flask
- PostgreSQL, MongoDB
- AWS, Docker
- REST APIs, GraphQL
- Git, Agile methodologies

Experience: 5+ years in web development
```

### Sample Resume Content
Create test resume files (PDF/DOCX) with content like:
```
John Smith
Software Developer

Experience:
- 4 years Python development
- Django and Flask frameworks
- PostgreSQL database management
- AWS cloud services
- REST API development

Skills:
Python, Django, PostgreSQL, AWS, Git, JavaScript, HTML, CSS

Education:
Bachelor of Computer Science
```

## 📊 API Endpoints

### Core Endpoints:
- `GET /` - Home page with job description input
- `POST /generate-jd` - Generate job description from parameters
- `POST /upload-jd` - Extract job description from uploaded file
- `POST /process-resumes` - Analyze resumes against job description
- `GET /health` - Health check endpoint

### Request/Response Examples:

**Generate JD:**
```json
POST /generate-jd
{
  "job_title": "Senior Python Developer",
  "years_experience": "5+",
  "must_have_skills": "Python,Django,PostgreSQL",
  "company_name": "Tech Corp",
  "employment_type": "Full-time",
  "industry": "Technology",
  "location": "Remote"
}
```

## 🔧 Configuration

### Environment Variables:
- `OPENAI_API_KEY`: Your OpenAI API key (optional)

### File Limits:
- Maximum 10 resume files per job
- Supported formats: PDF, DOC, DOCX
- File size limit: Based on server configuration

## 🚨 Troubleshooting

### Common Issues:

1. **File Upload Errors:**
   - Ensure files are in supported formats (PDF, DOC, DOCX)
   - Check file permissions in uploads directory

2. **AI Processing Errors:**
   - Verify OpenAI API key is correctly set
   - Check internet connection for API calls
   - Fallback methods will activate automatically

3. **Template Not Found:**
   - Ensure templates directory exists
   - Verify index.html and results.html are in templates/

4. **Import Errors:**
   - Run `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Development Mode:
```bash
uvicorn main:app --reload --log-level debug
```

## 🔒 Security Considerations

- File uploads are temporarily stored and automatically deleted
- No permanent storage of sensitive resume data
- API keys should be stored in environment variables
- Input validation on all file uploads and form data

## 🎯 Performance Optimization

- Asynchronous processing for AI calls
- Temporary file cleanup after processing
- Efficient document text extraction
- Responsive web interface with loading indicators

## 🔮 Future Enhancements

- **Database Integration:** Store job postings and candidate data
- **Advanced Analytics:** Detailed reporting and insights
- **Integration APIs:** Connect with ATS systems
- **Multi-language Support:** Support for non-English resumes
- **Batch Processing:** Handle larger volumes of resumes
- **Video Interview Scheduling:** Automated calendar integration

## 📄 License

This project is provided as an educational example for recruitment AI systems.

---

**Built with:** FastAPI, OpenAI GPT, Bootstrap, and modern web technologies for a seamless recruitment experience.
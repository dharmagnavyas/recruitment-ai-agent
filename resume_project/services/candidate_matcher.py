from models.schemas import CandidateResult
from services.ai_service import AIService

class CandidateMatcher:
    """Service for matching candidates to job descriptions"""
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
    
    async def match_candidate(self, resume_text: str, job_description: str, filename: str) -> CandidateResult:
        """Match a single candidate's resume against job description"""
        
        # Use AI service to analyze the match
        analysis = await self.ai_service.analyze_resume_match(resume_text, job_description)
        
        return CandidateResult(
            filename=filename,
            score=analysis['score'],
            missing_skills=analysis['missing_skills'],
            remarks=analysis['remarks']
        )
    
    def _extract_skills_from_text(self, text: str) -> list:
        """Extract skills from text using keyword matching"""
        
        # Common technical skills to look for
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
            'html', 'css', 'bootstrap', 'tailwind', 'sass', 'less',
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
            'git', 'svn', 'agile', 'scrum', 'devops', 'ci/cd', 'terraform', 'ansible',
            'machine learning', 'ai', 'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch',
            'rest api', 'graphql', 'microservices', 'oauth', 'jwt', 'soap',
            'linux', 'ubuntu', 'centos', 'windows', 'macos',
            'photoshop', 'illustrator', 'figma', 'sketch', 'adobe xd'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _calculate_basic_score(self, resume_skills: list, required_skills: list) -> int:
        """Calculate basic matching score based on skill overlap"""
        
        if not required_skills:
            return 70  # Default score if no specific requirements
        
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        matching_skills = set(resume_skills_lower) & set(required_skills_lower)
        
        if len(required_skills_lower) > 0:
            score = int((len(matching_skills) / len(required_skills_lower)) * 100)
        else:
            score = 70
        
        return min(100, max(0, score))
    
    def _identify_missing_skills(self, resume_text: str, job_description: str) -> list:
        """Identify skills mentioned in JD but not found in resume"""
        
        resume_skills = self._extract_skills_from_text(resume_text)
        jd_skills = self._extract_skills_from_text(job_description)
        
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        missing_skills = []
        
        for skill in jd_skills:
            if skill.lower() not in resume_skills_lower:
                missing_skills.append(skill)
        
        return missing_skills
    
    def _generate_remarks(self, score: int, missing_skills: list, resume_text: str) -> str:
        """Generate remarks based on matching analysis"""
        
        remarks = []
        
        if score >= 80:
            remarks.append("Excellent match for the position.")
        elif score >= 60:
            remarks.append("Good candidate with relevant experience.")
        elif score >= 40:
            remarks.append("Potential candidate with some relevant skills.")
        else:
            remarks.append("Limited alignment with job requirements.")
        
        if missing_skills:
            if len(missing_skills) <= 3:
                remarks.append(f"Could benefit from experience in {', '.join(missing_skills)}.")
            else:
                remarks.append(f"Missing several key skills including {', '.join(missing_skills[:3])}.")
        
        # Check for experience indicators
        if any(year in resume_text.lower() for year in ['years', 'experience', 'worked']):
            remarks.append("Shows relevant work experience.")
        
        return " ".join(remarks)
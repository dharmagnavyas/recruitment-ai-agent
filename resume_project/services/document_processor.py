import PyPDF2
import docx
from pathlib import Path
import re

class DocumentProcessor:
    """Service for extracting text from various document formats"""
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF, DOC, or DOCX files"""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_extension in ['.doc', '.docx']:
            return self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        
        return self._clean_text(text)
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
        
        return self._clean_text(text)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def extract_key_sections(self, text: str) -> dict:
        """Extract key sections from resume text"""
        sections = {
            'education': '',
            'experience': '',
            'skills': '',
            'contact': ''
        }
        
        # Simple keyword-based section detection
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Detect section headers
            if any(word in line_lower for word in ['education', 'qualification']):
                current_section = 'education'
            elif any(word in line_lower for word in ['experience', 'work', 'employment']):
                current_section = 'experience'
            elif any(word in line_lower for word in ['skill', 'technical', 'competenc']):
                current_section = 'skills'
            elif any(word in line_lower for word in ['contact', 'phone', 'email', 'address']):
                current_section = 'contact'
            
            # Add content to current section
            if current_section and line.strip():
                sections[current_section] += line + '\n'
        
        return sections
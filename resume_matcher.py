from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from db_connector import JobDescriptionDB
from logger import Logger
import PyPDF2

class ResumeJDMatcher:
    def __init__(self):
        self.logger = Logger('matcher')
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.db = JobDescriptionDB()
            self.job_descriptions = self.load_job_descriptions()
        except Exception as e:
            self.logger.error(f"Initialization error: {e}")
            raise

    def load_job_descriptions(self):
        try:
            all_jds = self.db.get_all_job_descriptions()
            # print(all_jds)
            formatted_jds = {}
            
            for key, jd in all_jds.items():
                if key not in formatted_jds:
                    formatted_jds[key] = []  #
                formatted_jds[key] = {
                    'title': jd['job_title'],
                    'department': jd['department'],
                    'level': jd['job_level'],
                    'summary': jd['job_summary'],
                    'responsibilities': jd['key_responsibilities'],
                    'required_skills': [
                        *jd['required_skills']['programming_languages'],
                        *jd['required_skills']['frameworks'],
                        jd['required_skills']['database']
                    ],
                    'education': jd['education_requirements'],
                    'experience': f"{jd['experience_requirements']['minimum_years']} years in application development",
                    'preferred': jd['preferred_qualifications']
                }
            return formatted_jds
        except Exception as e:
            self.logger.error(f"Error loading job descriptions: {e}")
            raise
    
    
    def extract_resume_text(self, pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = " ".join(page.extract_text() for page in reader.pages)
            return text.strip()
        except Exception as e:
            self.logger.error(f"Error extracting resume text: {e}")
            raise

    def format_job_text(self, job):
        """
        Formats job description into a structured text for comparison
        """
        return f"""
        Title: {job['title']}
        Department: {job['department']}
        Level: {job['level']}
        Summary: {job['summary']}
        Required Skills: {', '.join(job['required_skills'])}
        Experience: {job['experience']}
        Education: {job['education']}
        Responsibilities: {', '.join(job['responsibilities'])}
        Preferred: {', '.join(job['preferred'])}
        """

    def create_job_result(self, job, score):
        """
        Creates a standardized job result dictionary
        """
        return {
            'title': job['title'],
            'department': job['department'],
            'required_skills': ', '.join(job['required_skills']),
            'experience': job['experience'],
            'responsibilities': job['responsibilities'][:3],
            'score': score
        }

    def calculate_similarity_score(self, resume_text, job_text):
        try:
            resume_embedding = self.model.encode([resume_text])
            job_embedding = self.model.encode([job_text])
            similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
            return round(similarity * 100)
        except Exception as e:
            self.logger.error(f"Error calculating similarity score: {e}")
            raise

    def extract_name_from_resume(self, resume_text):
        """
        Extracts candidate name from resume text
        """
        try:
            # Simple extraction - first line or first words
            first_line = resume_text.split('\n')[0]
            return first_line.strip()
        except Exception as e:
            self.logger.error(f"Error extracting name from resume: {e}")
            return "Candidate"

    def analyze_resume(self, resume_text):
        try:
            matches = []
            unmatched = []
            
            for job_id, job in self.job_descriptions.items():
                job_text = self.format_job_text(job)
                score = self.calculate_similarity_score(resume_text, job_text, job)
                
                # Extract matched skills
                required_skills = self.extract_detailed_skills(job)
                matched_skills = [skill for skill in required_skills if skill.lower() in resume_text.lower()]
                
                job_result = {
                    'title': job['title'],
                    'company_name': job.get('company_name', 'Not specified'),
                    'summary': job.get('summary', ''),
                    'score': score,
                    'required_skills': self.format_skills(job.get('required_skills', {})),
                    'matched_skills': matched_skills,
                    'experience': job.get('experience', 'Not specified'),
                    'responsibilities': job.get('responsibilities', [])[:3]
                }
                
                if score >= 50:
                    matches.append(job_result)
                else:
                    unmatched.append(job_result)
            
            return {
                'matches': sorted(matches, key=lambda x: x['score'], reverse=True),
                'unmatched': sorted(unmatched, key=lambda x: x['score'], reverse=True)
            }
        except Exception as e:
            self.logger.error(f"Error analyzing resume: {e}")
            raise
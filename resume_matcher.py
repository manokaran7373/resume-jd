import docx
import textract
import re
from logger import Logger
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from db_connector import JobDescriptionDB


class ResumeJDMatcher:
    def __init__(self):
        self.logger = Logger("matcher")
        try:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.db = JobDescriptionDB()
            self.job_descriptions = self.load_job_descriptions()
        except Exception as e:
            self.logger.error(f"Initialization error: {e}")
            raise

    def load_job_descriptions(self):
        try:
            all_jds = self.db.get_all_job_descriptions()
            print(f"Retrieved {len(all_jds)} job descriptions from database")
            # print(all_jds)
            formatted_jds = {}

            for key, jd in all_jds.items():
                if key not in formatted_jds:
                    formatted_jds[key] = []  #
                formatted_jds[key] = {
                    "title": jd["job_title"],
                    "company_name": jd["company_name"],
                    "department": jd["department"],
                    "level": jd["job_level"],
                    "summary": jd["job_summary"],
                    "responsibilities": jd["key_responsibilities"],
                    "required_skills": [
                        *jd["required_skills"]["programming_languages"],
                        *jd["required_skills"]["frameworks"],
                        jd["required_skills"]["database"],
                    ],
                    "education": jd["education_requirements"],
                    "experience": f"{jd['experience_requirements']['minimum_years']} years in application development",
                    "preferred": jd["preferred_qualifications"],
                }
            return formatted_jds
        except Exception as e:
            self.logger.error(f"Error loading job descriptions: {e}")
            raise

    def extract_resume_text(self, file_path):
        try:
            file_extension = file_path.lower().split(".")[-1]

            if file_extension == "pdf":
                with open(file_path, "rb") as file:
                    reader = PdfReader(file)
                    text = " ".join(page.extract_text() for page in reader.pages)

            elif file_extension == "docx":
                doc = docx.Document(file_path)
                text = " ".join(paragraph.text for paragraph in doc.paragraphs)

            elif file_extension == "txt":
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()

            else:
                # For other formats like RTF, DOC, etc.
                text = textract.process(file_path).decode("utf-8")

            return text.strip()
        except Exception as e:
            self.logger.error(f"Error extracting text from {file_path}: {e}")
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
            "title": job["title"],
            "department": job["department"],
            "required_skills": ", ".join(job["required_skills"]),
            "experience": job["experience"],
            "responsibilities": job["responsibilities"][:3],
            "score": score,
        }

    def calculate_similarity_score(self, resume_text, job_text, job):
        try:
            # 1. Skills Check (60% weight) - High Priority
            required_skills = job["required_skills"]
            skills_found = [
                skill
                for skill in required_skills
                if skill.lower() in resume_text.lower()
            ]
            skills_score = (len(skills_found) / len(required_skills)) * 60

            # 2. Experience Check (15% weight)
            experience_text = job["experience"]
            exp_years_match = re.search(r"(\d+)", experience_text)
            required_years = int(exp_years_match.group(1)) if exp_years_match else 0

            exp_pattern = re.compile(r"(\d+)\s*(?:years?|yrs?)")
            resume_exp_matches = exp_pattern.findall(resume_text.lower())
            exp_years = max([int(year) for year in resume_exp_matches] or [0])
            exp_score = (
                min((exp_years / required_years) * 15, 15) if required_years > 0 else 15
            )

            # 3. Basic Content Match (25% weight)
            resume_embedding = self.model.encode([resume_text], show_progress_bar=False)
            job_embedding = self.model.encode([job_text], show_progress_bar=False)
            content_similarity = (
                cosine_similarity(resume_embedding, job_embedding)[0][0] * 25
            )
            # print(content_similarity)

            # Calculate final score
            final_score = skills_score + exp_score + content_similarity

            # Generate matching analysis
            analysis = {
                "total_score": round(final_score),
                "skills_match": {
                    "matched": skills_found,
                    "missing": [
                        skill for skill in required_skills if skill not in skills_found
                    ],
                    "score": round(skills_score, 2),
                },
                "experience_match": {
                    "required": required_years,
                    "found": exp_years,
                    "score": round(exp_score, 2),
                },
                "content_match_score": round(content_similarity, 2),
            }

            return round(final_score), analysis

        except Exception as e:
            self.logger.error(f"Error calculating similarity score: {e}")
            raise

    def extract_name_from_resume(self, resume_text):
        """
        Extracts candidate name from resume text
        """
        try:
            # Simple extraction - first line or first words
            first_line = resume_text.split("\n")[0]
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
                score, analysis = self.calculate_similarity_score(
                    resume_text, job_text, job
                )

                job_result = {
                    "title": job["title"],
                    "company_name": job.get("company_name", "Not specified"),
                    "summary": job.get("summary", ""),
                    "score": score,
                    "analysis": analysis,
                    "required_skills": ", ".join(job["required_skills"]),
                    "experience": job["experience"],
                    "responsibilities": job["responsibilities"][:3],
                }

                # Lower the threshold to 30% for better visibility
                if score >= 30:
                    matches.append(job_result)
                else:
                    unmatched.append(job_result)

            results = {
                "matches": sorted(matches, key=lambda x: x["score"], reverse=True),
                "unmatched": sorted(unmatched, key=lambda x: x["score"], reverse=True),
            }
            return results

        except Exception as e:
            self.logger.error(f"Error analyzing resume: {e}")
            raise

# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np
# from datetime import datetime
# import PyPDF2
# import re

# class ResumeJDMatcher:
#     def __init__(self):
#         self.model = SentenceTransformer('all-MiniLM-L6-v2')
#         self.job_descriptions = {
#     # 🔹 Software Engineering & Backend
#     'python_dev': {
#         'title': 'Senior Python Developer',
#         'skills': 'Python, Django, REST APIs, MySQL',
#         'experience': '3-5 years',
#         'matching_factors': 'Strong backend experience, API design knowledge'
#     },
#     'backend_dev': {
#         'title': 'Backend Developer',
#         'skills': 'Python, FastAPI, PostgreSQL, Redis',
#         'experience': '2-3 years',
#         'matching_factors': 'Backend architecture experience'
#     },

#     # 🔹 Machine Learning & AI
#     'ml_engineer': {
#         'title': 'ML Engineer',
#         'skills': 'Python, TensorFlow, PyTorch, SQL',
#         'experience': '2-4 years',
#         'matching_factors': 'Machine Learning experience, model deployment skills'
#     },
#     'ai_researcher': {
#         'title': 'AI Research Scientist',
#         'skills': 'Deep Learning, NLP, Generative AI, PyTorch',
#         'experience': '3-5 years',
#         'matching_factors': 'Research experience in AI/ML, working with LLMs'
#     },

#     # 🔹 Data Science & Engineering
#     'data_engineer': {
#         'title': 'Data Engineer',
#         'skills': 'Python, SQL, ETL, Hadoop',
#         'experience': '2-3 years',
#         'matching_factors': 'Data pipeline development, ETL processes'
#     },
#     'data_scientist': {
#         'title': 'Data Scientist',
#         'skills': 'Python, R, Machine Learning, Data Visualization',
#         'experience': '3-5 years',
#         'matching_factors': 'Experience with big data, statistical modeling'
#     },

#     # 🔹 Cloud & DevOps
#     'devops_engineer': {
#         'title': 'DevOps Engineer',
#         'skills': 'AWS, Docker, Kubernetes, CI/CD',
#         'experience': '3+ years',
#         'matching_factors': 'Experience in cloud infrastructure automation'
#     },
#     'cloud_architect': {
#         'title': 'Cloud Solutions Architect',
#         'skills': 'AWS, Azure, GCP, Terraform',
#         'experience': '5+ years',
#         'matching_factors': 'Architecting scalable cloud solutions'
#     },

#     # 🔹 Security & Cybersecurity
#     'cybersecurity_analyst': {
#         'title': 'Cybersecurity Analyst',
#         'skills': 'Penetration Testing, Security Audits, SIEM',
#         'experience': '2-5 years',
#         'matching_factors': 'Experience in network security & threat analysis'
#     },

#     # 🔹 Frontend Development & UI/UX
#     'frontend_dev': {
#         'title': 'Frontend Developer',
#         'skills': 'React, JavaScript, CSS, Next.js',
#         'experience': '2-4 years',
#         'matching_factors': 'Strong UI development, responsive design knowledge'
#     },
#     'ui_ux_designer': {
#         'title': 'UI/UX Designer',
#         'skills': 'Figma, Sketch, User Research, Wireframing',
#         'experience': '3+ years',
#         'matching_factors': 'Experience in UX research and interface design'
#     },

#     # 🔹 Product Management & Business Roles
#     'product_manager': {
#         'title': 'Product Manager',
#         'skills': 'Agile, Roadmap Planning, Market Research',
#         'experience': '3-6 years',
#         'matching_factors': 'Experience in leading cross-functional teams'
#     },
#     'business_analyst': {
#         'title': 'Business Analyst',
#         'skills': 'SQL, Data Analytics, Excel, Tableau',
#         'experience': '2-5 years',
#         'matching_factors': 'Strong analytical skills and business insights'
#     },

#     # 🔹 Blockchain & Web3
#     'blockchain_dev': {
#         'title': 'Blockchain Developer',
#         'skills': 'Solidity, Ethereum, Smart Contracts',
#         'experience': '2-4 years',
#         'matching_factors': 'Experience in blockchain application development'
#     },

#     # 🔹 Game Development
#     'game_dev': {
#         'title': 'Game Developer',
#         'skills': 'Unity, C#, Unreal Engine, Game Physics',
#         'experience': '3+ years',
#         'matching_factors': 'Game design and development experience'
#     }
# }

#     def extract_resume_text(self, pdf_path):
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = " ".join(page.extract_text() for page in reader.pages)
#         return text.strip()

#     def extract_name_from_resume(self, resume_text):
#         # Simple name extraction - first line or first capitalized words
#         first_line = resume_text.split('\n')[0]
#         return first_line.strip()

#     def calculate_similarity_score(self, resume_text, job_description):
#         resume_embedding = self.model.encode([resume_text])
#         job_embedding = self.model.encode([job_description])
#         similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
#         return round(similarity * 100)

#     def analyze_resume(self, resume_text):
#         matches = []
#         unmatched = []

#         candidate_name = self.extract_name_from_resume(resume_text)

#         for job_id, job in self.job_descriptions.items():
#             job_text = f"{job['title']} {job['skills']} {job['experience']} {job['matching_factors']}"
#             score = self.calculate_similarity_score(resume_text, job_text)

#             job_result = {
#                 'title': job['title'],
#                 'skills': job['skills'],
#                 'experience': job['experience'],
#                 'matching_factors': job['matching_factors'],
#                 'score': score
#             }

#             if score >= 50:
#                 matches.append(job_result)
#             else:
#                 unmatched.append(job_result)

#         return {
#             'candidate_name': candidate_name,
#             'matches': sorted(matches, key=lambda x: x['score'], reverse=True),
#             'unmatched': sorted(unmatched, key=lambda x: x['score'], reverse=True)
#         }

# def display_results(results):
#     print("\n📌 Resume Matching Report")
#     print(f"\nCandidate Name: {results['candidate_name']}")
#     print(f"Date: {datetime.now().strftime('%d-%m-%Y')}")

#     if results['matches']:
#         print("\n🔹 Matched Job Positions (Score ≥ 50%)\n")
#         for index, match in enumerate(results['matches'], 1):
#             print(f"{index}️⃣ {match['title']}\n")
#             print(f"🔢 Match Score: {match['score']}%\n")
#             print(f"✅ Required Skills: {match['skills']}")
#             print(f"✅ Experience: {match['experience']}")
#             print(f"✔ Key Matching Factors: {match['matching_factors']}")
#             print("\n" + "-"*80 + "\n")

#     if results['unmatched']:
#         print("\n❌ Unmatched Job Positions (Below 50%)")
#         for job in results['unmatched']:
#             print(f"• {job['title']} (Match: {job['score']}%)")

# def main():
#     print("\n" + "="*80)
#     print("🚀 Welcome to Smart Resume-JD Matcher!")
#     print("=" * 80 + "\n")

#     matcher = ResumeJDMatcher()
#     resume_path = "C:/Users/USER/Downloads/KM_resume(2024).pdf"  # Update with actual path

#     print("📄 Processing resume...")
#     resume_text = matcher.extract_resume_text(resume_path)

#     print("🔍 Analyzing matches...")
#     results = matcher.analyze_resume(resume_text)

#     display_results(results)
#     print("\n✨ Analysis Complete! ✨")
#     print("=" * 80 + "\n")

# if __name__ == "__main__":
#     main()


from resume_matcher import ResumeJDMatcher
from display_results import display_results
from logger import Logger


def main():
    logger = Logger("main")
    try:
        print("\n" + "=" * 80)
        print("🚀 Welcome to Smart Resume-JD Matcher!")
        print("=" * 80 + "\n")

        matcher = ResumeJDMatcher()
        # resume_path = "path/to/your/resume.pdf"
        resume_path = "C:/Users/USER/Downloads/Thiru_CV (1).docx"

        print("📄 Processing resume...")
        resume_text = matcher.extract_resume_text(resume_path)

        print("🔍 Analyzing matches...")
        results = matcher.analyze_resume(resume_text)

        display_results(results)

    except Exception as e:
        logger.error(f"Main execution error: {e}")
        print(f"\n❌ An error occurred: {e}")
    finally:
        print("\n✨ Process completed ✨")


if __name__ == "__main__":
    main()

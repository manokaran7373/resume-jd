# Smart Resume-JD Matcher 🚀

A powerful resume matching system that uses advanced NLP and ML techniques to analyze resumes against job descriptions, providing detailed matching scores and analysis.

## Features ✨

- **Multi-Format Support**: Handles PDF, DOCX, TXT, and RTF resume formats
- **Smart Scoring System**: 
  - Skills Match (60%)
  - Experience Match (15%)
  - Content Match (25%)
- **Detailed Analysis**: Provides comprehensive matching insights
- **Database Integration**: MySQL backend for job descriptions
- **Professional Reporting**: Clear, well-formatted match results

## Installation 🛠️

```bash
git clone https://github.com/manokaran7373/resume-jd.git
cd resume-jd

python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

pip install -r requirements.txt
```

## Dependencies 📚

- sentence-transformers
- PyPDF2
- python-docx
- textract
- mysql-connector-python
- scikit-learn

## Configuration ⚙️

1. Set up MySQL database:
```sql
CREATE DATABASE job_desc;
USE job_desc;
```

2. Configure database connection in `db_connector.py`:
```python
host="localhost"
user="your_username"
password="your_password"
database="job_desc"
```

## Usage 💻

```python
from resume_matcher import ResumeJDMatcher
from display_results import display_results

matcher = ResumeJDMatcher()
resume_path = "path/to/your/resume.pdf"
results = matcher.analyze_resume(matcher.extract_resume_text(resume_path))
display_results(results)
```

## Run the application
```bash
python main.py
```

## Output Format 📋

```
📌 Resume Matching Report
Date: 14-03-2024

🔹 High Priority Matches (Skills Match ≥ 60%)

1️⃣ Python Developer
🔢 Overall Match Score: 94%
💻 Skills Match: 60.0%
⏳ Experience Match: 15.0%
🎯 Content Match: 19.0%

[Detailed JD Content]
```

## Project Structure 📁

```
resume-matcher/
├── resume_matcher.py
├── db_connector.py
├── display_results.py
├── logger.py
├── main.py
├── requirements.txt
└── README.md
```

## Features in Detail 🔍

1. **Skills Analysis**
   - Priority-based skill matching
   - Technical skill verification
   - Framework compatibility check

2. **Experience Matching**
   - Years of experience validation
   - Role relevance scoring
   - Industry alignment check

3. **Content Analysis**
   - Semantic similarity scoring
   - Key responsibility matching
   - Job requirement alignment

## Contributing 🤝

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📄

MIT License - see LICENSE.md

## Contact 📧

Manokaran kumar - manokarank1916@gmail.com
Project Link: https://github.com/manokaran7373/resume-jd.git
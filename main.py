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
        resume_path = "path/to/your/resume.pdf"

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

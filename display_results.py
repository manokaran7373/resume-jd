from datetime import datetime

# def display_results(results):
#     print("\n📌 Resume Matching Report")
#     print(f"\nDate: {datetime.now().strftime('%d-%m-%Y')}")
    
#     if results['matches']:
#         print("\n🔹 Matched Job Positions (Score ≥ 50%)\n")
#         for index, match in enumerate(results['matches'], 1):
#             print(f"{index}️⃣ {match['title']}")
#             print(f"🔢 Match Score: {match['score']}%")
#             print(f"🏢 Company: {match.get('company_name', 'Not specified')}")
#             print(f"📝 Job Summary: {match.get('summary', 'Not specified')}")
#             print("\n✅ Required Skills:")
#             print(f"  • {match['required_skills']}")
#             print("\n✅ Experience Required:")
#             print(f"  • {match['experience']}")
#             print("\n✔ Key Responsibilities:")
#             for resp in match['responsibilities']:
#                 print(f"  • {resp}")
#             print("\n" + "-" * 80 + "\n")
    
#     if results['unmatched']:
#         print("\n❌ Unmatched Job Positions (Below 50%)")
#         for job in results['unmatched']:
#             print(f"• {job['title']} (Match: {job['score']}%)")
    
#     print("\n✨ Analysis Complete! ✨")
#     print("=" * 80 + "\n")



def display_results(results):
    print("\n📌 Resume Matching Report")
    print(f"\nDate: {datetime.now().strftime('%d-%m-%Y')}")
    
    if results['matches']:
        print("\n🔹 High Priority Matches (Skills Match ≥ 60%)\n")
        for index, match in enumerate(results['matches'], 1):
            print(f"{index}️⃣ {match['title']}")
            print(f"🔢 Overall Match Score: {match['score']}%")
            print(f"💻 Skills Match: {match['analysis']['skills_match']['score']}%")
            print(f"⏳ Experience Match: {match['analysis']['experience_match']['score']}%")
            print(f"🎯 Content Match: {match['analysis']['content_match_score']}%")
            
            # Detailed JD Content for high-priority matches
            print(f"\n🏢 Company: {match['company_name']}")
            print(f"\n📝 Job Summary:")
            print(f"{match['summary']}")
            
            print("\n📋 Matched Skills:")
            print(f"  ✓ {', '.join(match['analysis']['skills_match']['matched'])}")
            
            print("\n❌ Missing Skills:")
            print(f"  • {', '.join(match['analysis']['skills_match']['missing'])}")
            
            print("\n💼 Experience Required:")
            print(f"  • {match['experience']}")
            
            print("\n🎯 Key Responsibilities:")
            for resp in match['responsibilities']:
                print(f"  • {resp}")
            
            print("\n" + "-" * 80 + "\n")
    
    if results['unmatched']:
        print("\n📉 Lower Priority Matches\n")
        for job in results['unmatched']:
            print(f"• {job['title']} (Match: {job['score']}%)")
    
    print("\n✨ Analysis Complete! ✨")
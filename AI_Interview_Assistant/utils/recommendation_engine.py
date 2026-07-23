# utils/recommendation_engine.py
"""
Recommendation Engine.
Maps identified skill gaps (missing skills) to online courses,
professional certifications, learning platforms, and career trajectories.
"""

class RecommendationEngine:
    def __init__(self):
        # Database of courses, platforms, and certifications for target skills
        self.catalog = {
            "python": {
                "courses": [
                    {"title": "Python for Everybody Specialization", "platform": "Coursera / University of Michigan"},
                    {"title": "Complete Python Bootcamp From Zero to Hero", "platform": "Udemy"}
                ],
                "certifications": ["PCPP1 – Certified Professional in Python Programming"],
                "career_path": "Software Engineer, Backend Developer, Data Scientist"
            },
            "java": {
                "courses": [
                    {"title": "Java Programming and Software Engineering Fundamentals", "platform": "Coursera / Duke University"},
                    {"title": "Java In-Depth: Become a Complete Java Engineer", "platform": "Udemy"}
                ],
                "certifications": ["Oracle Certified Professional: Java SE Developer"],
                "career_path": "Enterprise Software Engineer, Android Developer"
            },
            "sql": {
                "courses": [
                    {"title": "SQL for Data Science", "platform": "Coursera / UC Davis"},
                    {"title": "The Complete SQL Bootcamp", "platform": "Udemy"}
                ],
                "certifications": ["Microsoft Certified: Azure Data Fundaments (DP-900)"],
                "career_path": "Database Administrator, Data Analyst, BI Developer"
            },
            "excel": {
                "courses": [
                    {"title": "Everyday Excel Specialization", "platform": "Coursera / University of Colorado"},
                    {"title": "Microsoft Excel - Excel from Beginner to Advanced", "platform": "Udemy"}
                ],
                "certifications": ["Microsoft Office Specialist (MOS): Excel Associate"],
                "career_path": "Financial Analyst, Business Operations Specialist"
            },
            "power bi": {
                "courses": [
                    {"title": "Microsoft Power BI Data Analyst Professional Certificate", "platform": "Coursera"},
                    {"title": "Power BI A-Z: Hands-On Power BI Training", "platform": "Udemy"}
                ],
                "certifications": ["Microsoft Certified: Power BI Data Analyst Associate (PL-300)"],
                "career_path": "BI Analyst, Data Reporting Specialist"
            },
            "tableau": {
                "courses": [
                    {"title": "Data Visualization with Tableau Specialization", "platform": "Coursera / UC Davis"},
                    {"title": "Tableau 2024 A-Z: Hands-On Tableau Training for Data Science", "platform": "Udemy"}
                ],
                "certifications": ["Tableau Desktop Certified Associate"],
                "career_path": "Data Visualization Engineer, Business Analyst"
            },
            "machine learning": {
                "courses": [
                    {"title": "Machine Learning Specialization", "platform": "Coursera / Stanford (DeepLearning.AI)"},
                    {"title": "Introduction to Machine Learning Course", "platform": "Kaggle Learning"}
                ],
                "certifications": ["AWS Certified Machine Learning – Specialty"],
                "career_path": "Machine Learning Engineer, Data Scientist"
            },
            "deep learning": {
                "courses": [
                    {"title": "Deep Learning Specialization", "platform": "Coursera / DeepLearning.AI"},
                    {"title": "Practical Deep Learning for Coders", "platform": "Fast.ai"}
                ],
                "certifications": ["Google Cloud Professional Machine Learning Engineer"],
                "career_path": "Deep Learning Researcher, Computer Vision Engineer"
            },
            "nlp": {
                "courses": [
                    {"title": "Natural Language Processing Specialization", "platform": "Coursera / DeepLearning.AI"},
                    {"title": "Hugging Face NLP Course", "platform": "Hugging Face (Free)"}
                ],
                "certifications": ["TensorFlow Developer Certificate"],
                "career_path": "NLP Engineer, Conversational AI Designer"
            },
            "react": {
                "courses": [
                    {"title": "Front-End Web Development with React", "platform": "Coursera / HKUST"},
                    {"title": "React - The Complete Guide (incl Hooks, React Router, Redux)", "platform": "Udemy"}
                ],
                "certifications": ["Meta Front-End Developer Professional Certificate"],
                "career_path": "Frontend Engineer, UI/UX Developer"
            },
            "node.js": {
                "courses": [
                    {"title": "HTML, CSS, and Javascript for Web Developers", "platform": "Coursera / Johns Hopkins"},
                    {"title": "The Complete Node.js Developer Course", "platform": "Udemy"}
                ],
                "certifications": ["OpenJS Node.js Application Developer (LFW211)"],
                "career_path": "Backend Developer, Full Stack Engineer"
            },
            "git": {
                "courses": [
                    {"title": "Version Control with Git", "platform": "Coursera / Atlassian"},
                    {"title": "Git Complete: The definitive, step-by-step guide to Git", "platform": "Udemy"}
                ],
                "certifications": ["GitHub Actions Certification"],
                "career_path": "DevOps Engineer, Software Developer"
            },
            "github": {
                "courses": [
                    {"title": "GitHub Foundations", "platform": "GitHub Skills (Free)"}
                ],
                "certifications": ["GitHub Foundations Certification"],
                "career_path": "DevOps Architect"
            }
        }
        
        # General career advice/certifications when no skills are missing
        self.default_recommendations = {
            "courses": [
                {"title": "Software Design and Architecture Specialization", "platform": "Coursera / University of Alberta"},
                {"title": "System Design Interview Prep", "platform": "ByteByteGo"}
            ],
            "certifications": [
                "AWS Certified Solutions Architect – Associate",
                "Certified ScrumMaster (CSM)"
            ],
            "career_path": "Senior Software Architect, Technical Lead, engineering Manager"
        }

    def get_recommendations(self, missing_skills: list) -> dict:
        """
        Maps a list of missing skills to courses and certifications.
        """
        recommended_courses = []
        recommended_certs = []
        target_roles = set()
        
        for skill in missing_skills:
            skill_key = skill.lower().strip()
            # If we have catalog recommendations for this skill
            if skill_key in self.catalog:
                item = self.catalog[skill_key]
                # Extend courses
                for course in item["courses"]:
                    if course not in recommended_courses:
                        recommended_courses.append(course)
                # Extend certs
                for cert in item["certifications"]:
                    if cert not in recommended_certs:
                        recommended_certs.append(cert)
                # Map role
                target_roles.add(item["career_path"])
                
        # If no recommendations matched, return default advanced learning paths
        if not recommended_courses:
            recommended_courses = self.default_recommendations["courses"]
            recommended_certs = self.default_recommendations["certifications"]
            target_roles.add(self.default_recommendations["career_path"])
            
        return {
            "courses": recommended_courses[:6], # Limit to top 6 courses
            "certifications": recommended_certs[:4], # Limit to top 4 certs
            "career_paths": ", ".join(list(target_roles)[:2]) # Limit to top 2 paths
        }

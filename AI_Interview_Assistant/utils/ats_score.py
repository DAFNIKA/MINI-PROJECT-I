# utils/ats_score.py
"""
ATS Resume Scorer.
Computes a hybrid match score based on TF-IDF cosine similarity,
skill coverage ratio, and structural resume check.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ATSScorer:
    @staticmethod
    def calculate_text_similarity(resume_text: str, jd_text: str) -> float:
        """
        Calculates cosine similarity using TF-IDF representation of the texts.
        Returns a float between 0 and 100.
        """
        if not resume_text or not jd_text:
            return 0.0
            
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf = vectorizer.fit_transform([resume_text, jd_text])
            similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            return float(similarity * 100)
        except Exception as e:
            print(f"Error computing text similarity: {e}")
            return 0.0

    @staticmethod
    def calculate_score(resume_text: str, jd_text: str, matched_skills: list, missing_skills: list, 
                        contact_info: dict, education: list, experience: list) -> dict:
        """
        Computes a composite ATS score from multiple sub-scores:
        1. Text Similarity (30% weight)
        2. Skill Coverage (60% weight)
        3. Structure Check (10% weight)
        """
        # 1. Text Similarity Score
        text_sim = ATSScorer.calculate_text_similarity(resume_text, jd_text)
        
        # 2. Skill Coverage Score
        total_jd_skills = len(matched_skills) + len(missing_skills)
        skill_score = 100.0
        if total_jd_skills > 0:
            skill_score = (len(matched_skills) / total_jd_skills) * 100
            
        # 3. Structure Completeness Score
        struct_score = 0.0
        if contact_info.get("email") != "Not Found":
            struct_score += 25
        if contact_info.get("phone") != "Not Found":
            struct_score += 25
        if education:
            struct_score += 25
        if experience:
            struct_score += 25

        # Weighted calculation
        overall_score = (text_sim * 0.3) + (skill_score * 0.6) + (struct_score * 0.1)
        overall_score = min(max(overall_score, 0.0), 100.0) # clamp between 0 and 100

        # Generate constructive suggestions
        suggestions = []
        if contact_info.get("email") == "Not Found":
            suggestions.append("⚠️ Add a professional email address to the header.")
        if contact_info.get("phone") == "Not Found":
            suggestions.append("⚠️ Add a phone number for contact reachability.")
        if not education:
            suggestions.append("⚠️ Add an Education section listing your degrees and college/university.")
        if not experience:
            suggestions.append("⚠️ Detail your work history or academic projects under an Experience/Projects section.")
            
        if missing_skills:
            top_missing = missing_skills[:5]
            skills_str = ", ".join(top_missing)
            suggestions.append(f"💡 Incorporate these high-demand keywords and skills: {skills_str}.")
        
        if text_sim < 40:
            suggestions.append("✍️ Rewrite your summary and experience bullet points to more closely mirror the action verbs and terminology of the Job Description.")

        if not suggestions:
            suggestions.append("🌟 Excellent alignment! Your resume matches the job requirements very well.")

        return {
            "overall_score": round(overall_score, 1),
            "text_similarity": round(text_sim, 1),
            "skill_score": round(skill_score, 1),
            "structure_score": round(struct_score, 1),
            "suggestions": suggestions
        }

# utils/jd_matcher.py
"""
Job Description Matcher.
Identifies skill matches and gaps between a candidate's resume and a Job Description.
"""

from utils.skill_extractor import SkillExtractor

class JDMatcher:
    def __init__(self):
        self.extractor = SkillExtractor()

    def analyze_jd(self, jd_text: str) -> dict:
        """
        Parses a Job Description and extracts target skills.
        """
        return self.extractor.extract_skills(jd_text)

    def match_skills(self, resume_skills_dict: dict, jd_skills_dict: dict) -> dict:
        """
        Matches resume skills against job description skills.
        Returns matched, missing, and recommended skills.
        """
        resume_set = set()
        for skills in resume_skills_dict.values():
            resume_set.update(skills)

        jd_set = set()
        for skills in jd_skills_dict.values():
            jd_set.update(skills)

        # Convert to lowercase for comparison
        resume_set_lower = {s.lower(): s for s in resume_set}
        jd_set_lower = {s.lower(): s for s in jd_set}

        matched_lower = set(resume_set_lower.keys()).intersection(set(jd_set_lower.keys()))
        missing_lower = set(jd_set_lower.keys()).difference(set(resume_set_lower.keys()))

        # Map back to original case
        matched_skills = [jd_set_lower[s] for s in matched_lower]
        missing_skills = [jd_set_lower[s] for s in missing_lower]

        # Recommend skills: top missing skills that are in the JD
        recommended_skills = missing_skills.copy()

        return {
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(missing_skills),
            "recommended_skills": sorted(recommended_skills)
        }

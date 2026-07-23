# utils/skill_extractor.py
"""
Skill Extractor Utility.
Uses tokenization, regular expressions, and semantic lookup to identify and categorize technical skills.
"""

import re
import spacy
from spacy.matcher import PhraseMatcher

class SkillExtractor:
    def __init__(self):
        # Define detailed taxonomy of skills to extract
        self.skill_categories = {
            "Languages": [
                "Python", "Java", "JavaScript", "TypeScript", "HTML", "CSS", "C", "C++", 
                "C#", "Ruby", "PHP", "Go", "Rust", "R", "SQL", "Swift", "Kotlin", "Scala"
            ],
            "Libraries & Frameworks": [
                "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "React", 
                "Node.js", "Express", "Angular", "Vue", "Keras", "NLTK", "spaCy", "Scipy",
                "HuggingFace", "Django", "Flask", "FastAPI", "Tailwind", "Bootstrap", "Spring Boot"
            ],
            "Tools & Databases": [
                "Git", "GitHub", "Tableau", "Power BI", "Excel", "MySQL", "SQLite", 
                "PostgreSQL", "MongoDB", "Redis", "Docker", "Kubernetes", "AWS", "GCP", 
                "Azure", "Jira", "Linux", "Heroku"
            ],
            "Concepts & Methodologies": [
                "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
                "Computer Vision", "Data Science", "Web Development", "DevOps", 
                "Object-Oriented Programming", "OOP", "Agile", "Scrum", "Cloud Computing"
            ]
        }
        
        # Mapping of alternative/abbreviated spellings to canonical names
        self.synonyms = {
            "js": "JavaScript",
            "ts": "TypeScript",
            "reactjs": "React",
            "react.js": "React",
            "nodejs": "Node.js",
            "node": "Node.js",
            "sklearn": "Scikit-learn",
            "tensorflow": "TensorFlow",
            "pytorch": "PyTorch",
            "git/github": ["Git", "GitHub"],
            "powerbi": "Power BI",
            "scikit learn": "Scikit-learn",
            "natural language processing": "NLP",
            "oop": "Object-Oriented Programming"
        }
        
        # Load small English spaCy model. Fail-safe to download if missing.
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model 'en_core_web_sm' not found. Installing via command-line...")
            try:
                import subprocess
                import sys
                subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
                self.nlp = spacy.load("en_core_web_sm")
            except Exception as ex:
                print(f"Failed to install spaCy model programmatically: {ex}")
                self.nlp = None

    def extract_skills(self, text: str) -> dict:
        """
        Extracts skills from text and groups them by category.
        """
        extracted = {
            "Languages": [],
            "Libraries & Frameworks": [],
            "Tools & Databases": [],
            "Concepts & Methodologies": []
        }
        
        text_lower = text.lower()
        
        # 1. Regex & Boundary-based extraction (highly reliable for special chars like C++, C#, Node.js)
        # Flatten all skill definitions for pattern checking
        all_skills = []
        for cat, items in self.skill_categories.items():
            for item in items:
                all_skills.append((item, cat))
                
        matched_skills = set()
        
        # Match canonical names
        for skill_name, category in all_skills:
            # Escape skill name for regex safety, handle special character boundaries
            escaped_name = re.escape(skill_name)
            
            # Boundary conditions: if it ends with special characters like ++, #, .js, adjust boundaries
            if skill_name.endswith("++") or skill_name.endswith("#"):
                pattern = r'\b' + escaped_name + r'(?:\s|$|\b)'
            elif skill_name.endswith(".js"):
                pattern = r'\b' + escaped_name + r'(?:\b|$|\s)'
            else:
                pattern = r'\b' + escaped_name + r'\b'
                
            if re.search(pattern, text_lower):
                matched_skills.add((skill_name, category))
                
        # Match synonyms/abbreviations
        for syn, canonical in self.synonyms.items():
            escaped_syn = re.escape(syn)
            pattern = r'\b' + escaped_syn + r'\b'
            if re.search(pattern, text_lower):
                if isinstance(canonical, list):
                    for c_name in canonical:
                        cat = self._get_skill_category(c_name)
                        matched_skills.add((c_name, cat))
                else:
                    cat = self._get_skill_category(canonical)
                    matched_skills.add((canonical, cat))
                    
        # 2. Match using spaCy PhraseMatcher (adds semantic boundary matching)
        if self.nlp:
            try:
                doc = self.nlp(text)
                matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
                
                # Add phrases to match
                for skill_name, category in all_skills:
                    patterns = [self.nlp.make_doc(skill_name)]
                    matcher.add(skill_name, patterns)
                    
                matches = matcher(doc)
                for match_id, start, end in matches:
                    matched_string = self.nlp.vocab.strings[match_id]
                    cat = self._get_skill_category(matched_string)
                    matched_skills.add((matched_string, cat))
            except Exception as e:
                print(f"Error in spaCy matching: {e}")
                
        # Group the matched items
        for skill_name, category in matched_skills:
            if category in extracted and skill_name not in extracted[category]:
                extracted[category].append(skill_name)
                
        return extracted

    def _get_skill_category(self, skill_name: str) -> str:
        """
        Helper to look up category of a skill name from taxonomy.
        """
        for category, list_of_skills in self.skill_categories.items():
            if skill_name in list_of_skills:
                return category
        return "Concepts & Methodologies" # Fallback

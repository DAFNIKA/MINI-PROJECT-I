# utils/report_generator.py
"""
PDF Report Generator.
Compiles resume profiles, ATS scores, interview Q&As, and recommendations
into a professionally styled, printable PDF document using fpdf2.
"""

import os
from fpdf import FPDF

def clean_txt(text: str) -> str:
    """
    Cleans Unicode text by substituting common non-ASCII characters
    with standard ASCII equivalents to prevent FPDF latin-1 encoding errors.
    """
    if not text:
        return ""
    replacements = {
        "\u201c": '"', "\u201d": '"', "\u2018": "'", "\u2019": "'",
        "\u2013": "-", "\u2014": "-", "\u2022": "*", "\u2010": "-",
        "\u2265": ">=", "\u2264": "<=", "\u20a8": "Rs.", "\u20b9": "Rs."
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    return text.encode('latin-1', 'replace').decode('latin-1')

class PDFReport(FPDF):
    def header(self):
        # Draw header on all pages except title page (if needed)
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, clean_txt("AI-Powered Interview Prep Assistant | Performance Report"), new_x="LMARGIN", new_y="NEXT", align="R")
            self.line(10, 18, 200, 18)
            self.ln(5)

    def footer(self):
        # Page numbers
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="C")

class ReportGenerator:
    @staticmethod
    def generate_pdf(user_info: dict, resume_info: dict, ats_info: dict, 
                     interview_answers: list, recommendations: dict, output_path: str) -> str:
        """
        Builds a comprehensive interview preparation summary PDF.
        """
        pdf = PDFReport()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # --- TITLE PAGE / HEADER ---
        pdf.set_fill_color(99, 102, 241) # Indigo accent color
        pdf.rect(0, 0, 210, 40, "F")
        
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(255, 255, 255)
        pdf.set_y(12)
        pdf.cell(0, 10, clean_txt("AI-POWERED INTERVIEW PREPARATION REPORT"), new_x="LMARGIN", new_y="NEXT", align="C")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, clean_txt("Candidate Performance Review and Actionable Skills Gap Analysis"), new_x="LMARGIN", new_y="NEXT", align="C")
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_y(45)
        
        # --- SECTION 1: PROFILE SUMMARY ---
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, clean_txt("1. Candidate Profile Summary"), new_x="LMARGIN", new_y="NEXT")
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(100, 6, clean_txt(f"Name: {user_info.get('full_name', 'N/A')}"))
        pdf.cell(90, 6, clean_txt(f"Username: {user_info.get('username', 'N/A')}"), new_x="LMARGIN", new_y="NEXT")
        pdf.cell(100, 6, clean_txt(f"Email: {user_info.get('email', 'N/A')}"))
        pdf.cell(90, 6, clean_txt(f"Phone: {resume_info.get('parsed_details', {}).get('contact', {}).get('phone', 'N/A')}"), new_x="LMARGIN", new_y="NEXT")
        
        if resume_info:
            pdf.cell(0, 6, clean_txt(f"Active Resume Filename: {resume_info.get('filename')}"), new_x="LMARGIN", new_y="NEXT")
            
            # Print parsed skills list
            skills_data = resume_info.get("parsed_details", {}).get("skills", {})
            flat_skills = []
            for items in skills_data.values():
                flat_skills.extend(items)
            
            if flat_skills:
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, clean_txt("Extracted Core Technical Skills:"), new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 5, clean_txt(", ".join(flat_skills)), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        # --- SECTION 2: ATS SCORE CARD ---
        if ats_info:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, clean_txt(f"2. ATS Score Evaluation: {ats_info.get('job_title', 'Target Role')}"), new_x="LMARGIN", new_y="NEXT")
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)
            
            metrics = ats_info.get("score_metrics", {})
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(50, 6, clean_txt(f"Overall ATS Score: {metrics.get('overall_score')}%"))
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(50, 6, clean_txt(f"Text Similarity: {metrics.get('text_similarity')}%"))
            pdf.cell(50, 6, clean_txt(f"Skill Score: {metrics.get('skill_score')}%"))
            pdf.cell(40, 6, clean_txt(f"Structure Score: {metrics.get('structure_score')}%"), new_x="LMARGIN", new_y="NEXT")
            
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(0, 6, clean_txt("ATS Recommendations for improvement:"), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "I", 9)
            for sug in metrics.get("suggestions", []):
                pdf.multi_cell(0, 5, clean_txt(f"- {sug}"), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)

        # --- SECTION 3: RECOMMENDATIONS ---
        if recommendations:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, clean_txt("3. Skill-Gap Training Recommendations"), new_x="LMARGIN", new_y="NEXT")
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)
            
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, clean_txt(f"Recommended Career Trajectory: {recommendations.get('career_paths') or 'Full Stack Software Engineer'}"), new_x="LMARGIN", new_y="NEXT")
            
            pdf.ln(2)
            pdf.cell(100, 6, clean_txt("Suggested Online Courses:"))
            pdf.cell(90, 6, clean_txt("Recommended Certifications:"), new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("Helvetica", "", 9)
            courses = recommendations.get("courses", [])
            certs = recommendations.get("certifications", [])
            
            max_lines = max(len(courses), len(certs))
            for i in range(max_lines):
                c_text = ""
                cr_text = ""
                if i < len(courses):
                    item = courses[i]
                    c_text = f"* {item['title']} ({item['platform']})"
                if i < len(certs):
                    cr_text = f"* {certs[i]}"
                
                pdf.cell(100, 5, clean_txt(c_text))
                pdf.cell(90, 5, clean_txt(cr_text), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(8)

        # --- SECTION 4: INTERVIEW DETAILS ---
        if interview_answers:
            # We start this section on a new page to keep it clean
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, clean_txt("4. Mock Interview Session Transcripts"), new_x="LMARGIN", new_y="NEXT")
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)
            
            for idx, ans in enumerate(interview_answers):
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, clean_txt(f"Question {idx+1}: {ans['question_text']}"), new_x="LMARGIN", new_y="NEXT")
                
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(0, 5, clean_txt(f"Your Response: {ans['answer_text']}"), new_x="LMARGIN", new_y="NEXT")
                
                pdf.set_text_color(99, 102, 241) # Highlight ideal response
                pdf.multi_cell(0, 5, clean_txt(f"Ideal Concept Answer: {ans['ideal_answer']}"), new_x="LMARGIN", new_y="NEXT")
                
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Helvetica", "B", 9)
                scores_str = f"Scores -> Semantic Fit: {ans['similarity_score']}% | Grammar: {ans['grammar_score']}% | Communication: {ans['communication_score']}% | Confidence: {ans['confidence_score']}%"
                pdf.cell(0, 6, clean_txt(scores_str), new_x="LMARGIN", new_y="NEXT")
                
                pdf.set_font("Helvetica", "I", 9)
                pdf.multi_cell(0, 5, clean_txt(f"Feedback: {ans['feedback']}"), new_x="LMARGIN", new_y="NEXT")
                if ans['missing_concepts']:
                    pdf.set_font("Helvetica", "", 9)
                    pdf.cell(0, 5, clean_txt(f"Missing terms: {ans['missing_concepts']}"), new_x="LMARGIN", new_y="NEXT")
                
                pdf.ln(5)
                # Draw small line separator
                pdf.line(15, pdf.get_y(), 195, pdf.get_y())
                pdf.ln(4)
                
        # Make directory for saving report if missing
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        pdf.output(output_path)
        return output_path

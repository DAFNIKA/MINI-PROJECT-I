# generate_samples.py
"""
Script to programmatically generate a sample PDF resume and a sample Job Description.
This provides ready-to-use testing materials for the AI Interview Prep Assistant.
"""

import os
from fpdf import FPDF

def create_sample_resume_pdf(output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "John Doe", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Email: john.doe@example.com | Phone: 123-456-7890 | GitHub: github.com/johndoe", ln=True, align="C")
    pdf.ln(5)
    
    # Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Professional Summary", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, "Motivated Software Engineer and Data Scientist with 2+ years of experience building machine learning models and web applications. Skilled in Python, SQL, and database management. Proven ability to analyze datasets and build predictive models using Scikit-learn and Pandas.")
    pdf.ln(5)
    
    # Skills
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Core Technical Skills", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "Languages: Python, Java, SQL, HTML, CSS, JavaScript", ln=True)
    pdf.cell(0, 6, "Libraries & Frameworks: Pandas, NumPy, Scikit-learn, React", ln=True)
    pdf.cell(0, 6, "Tools & Databases: Git, GitHub, MySQL, Excel, Docker", ln=True)
    pdf.cell(0, 6, "Concepts: Machine Learning, Web Development, Object-Oriented Programming (OOP)", ln=True)
    pdf.ln(5)
    
    # Education
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Education", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Bachelor of Technology in Computer Science", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "XYZ University | Graduated: May 2024", ln=True)
    pdf.ln(5)
    
    # Experience
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Work Experience & Projects", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Junior Software Engineer - TechCorp Solutions (June 2024 - Present)", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, "- Designed and maintained backend REST APIs using Python, Flask, and PostgreSQL database.\n- Collaborated with front-end teams to integrate React components with backend services.\n- Streamlined code deployments using Git and GitHub actions CI/CD pipelines.")
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Data Science Project: Customer Churn Predictor", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, "- Built a classification model using Scikit-learn, Pandas, and NumPy to predict customer churn with 88% accuracy.\n- Extracted and cleaned customer transactions from MySQL databases using SQL aggregation queries.")
    
    pdf.output(output_path)
    print(f"Sample Resume PDF created at: {output_path}")

def create_sample_jd_txt(output_path):
    jd_content = """Job Title: Associate Data Scientist & Machine Learning Engineer

Company: AI Frontiers Inc.
Location: Remote / Hybrid

About the Role:
We are seeking an Associate Data Scientist with strong coding skills in Python and database management. In this role, you will help design, build, and deploy machine learning models and data pipelines to power our automated analytics platforms.

Requirements & Qualifications:
- 1-3 years of experience writing clean, professional code in Python.
- Proficient in SQL database querying, JOINs, and database normalization.
- Practical experience with Machine Learning modeling using Scikit-learn, Pandas, and NumPy.
- Strong understanding of version control using Git and GitHub.
- Experience with Deep Learning (TensorFlow or PyTorch) and Natural Language Processing (NLP) is a plus.
- Excellent communication and problem-solving skills.
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(jd_content.strip())
    print(f"Sample JD text created at: {output_path}")

if __name__ == "__main__":
    create_sample_resume_pdf("sample_resume.pdf")
    create_sample_jd_txt("sample_job_description.txt")

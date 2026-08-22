AI Based Interview Preparation Asssistant using ML and NLP:

AI-Powered Interview Preparation Assistant:
An advanced, self-contained AI web application designed to automate candidate profile alignment and mock interview practice. This system brings together resume parsing, Applicant Tracking System (ATS) scoring, dynamic skill-based question generation, and deep semantic answer grading into a single Streamlit dashboard.
Built using Python, Streamlit, SQLite 3, spaCy NER, NLTK, and Sentence-Transformers (SBERT).

 Key Features:
*   Secure Authentication: Stateful registration and login sessions powered by `bcrypt` password hashing.
*   Resume Parsing & Skill Extraction: Extracts text and contact details from uploaded PDF and Word (`.docx`) files, mapping technical credentials to a taxonomy of 500+ skills using spaCy NER.
*   ATS Compatibility Scoring: Computes resume-JD alignment ratings (0-100%) using TF-IDF document vectorization and Cosine Similarity.
*   Mock Interview Simulator: Dynamically pulls mock questions based on the candidate's parsed resume skills and selected difficulty (Easy, Medium, Hard).
*   Semantic Answer Evaluation: Uses Sentence-Transformers (SBERT: `all-MiniLM-L6-v2`) to measure candidate responses against ideal answers, layered with NLTK heuristics checking grammar and filler-word density.
*   Analytics Dashboard: Generates interactive Plotly charts illustrating historical score progression and scoring brackets.
*   PDF Report Generator: Compiles candidate profiles, ATS ratings, full mock transcripts, and targeted course recommendations into a downloadable PDF report using `fpdf2`.
  
  Technology Stack:
*   Frontend UI: Streamlit, Vanilla CSS (Glassmorphism theme)
*   Machine Learning / NLP:
    *   Sentence-Transformers (SBERT) - Dense vector cosine embeddings
    *   spaCy - Named Entity Recognition (`en_core_web_sm` CNN model)
    *   NLTK - Word/sentence tokenization & filler heuristics
    *   Scikit-learn - TF-IDF document similarity matrices
*   Database: SQLite 3 (Standard SQL driver)
*   Document Engines: `pdfplumber` (PDF), `python-docx` (Word), `fpdf2` (PDF compiler)

    ️ Installation & Setup
1. Clone the Repository:
   
   git clone https://github.com/your-username/AI-Interview-Assistant.git
   cd AI-Interview-Assistant
Install Dependencies: Ensure you have Python 3.10+ installed, then run:

pip install -r requirements.txt
Download NLP Models: Download the spaCy language model:

python -m spacy download en_core_web_sm
Launch the Application: Run the local Streamlit dev server:

streamlit run app.py

👤 Author
D. Dafnika
Department of Master of Computer Applications (PG-MCA)
PSG College of Arts & Science, Coimbatore, India
7:13 PM


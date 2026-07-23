# AI-Powered Interview Preparation Assistant

An advanced, production-ready web application built using **Python, Streamlit, SQLite, spaCy NLP, NLTK, and Sentence-Transformers (SBERT)**. It helps students and job seekers prepare for interviews through personalized AI-driven mocks, resume parsing, ATS scoring, and training recommendations.

---

## 🌟 Key Features

1. **Secure User Authentication**: Encrypted credentials using `bcrypt` and active session state management.
2. **Resume Parser**: Raw text extraction from PDF and Word documents, using regular expressions and Named Entity Recognition (NER) to isolate contact info, education history, and experience items.
3. **Skill Extractor**: Automatic detection of core technical competencies from a predefined taxonomy of 500+ skills (Languages, Libraries, Frameworks, Databases, Tools).
4. **ATS Resume Matcher**: TF-IDF & Cosine Similarity score mapping against target Job Descriptions, highlighting keyword matches, gap analyses, and structural suggestions.
5. **Interview Question Generator**: Dynamic selection of Technical, HR, Behavioral, and Scenario questions matched to candidate skills and difficulty profiles (Easy, Medium, Hard).
6. **Sentence-Transformers Answer Evaluator**: Real-time evaluation of answers comparing semantic embeddings against ideal responses using `all-MiniLM-L6-v2`. Includes NLP indicators for grammar correctness, communication readability, and filler word confidence assessments.
7. **Interactive Dashboard**: progress tracker charts, score distribution rings, and historical session logs generated dynamically with `Plotly`.
8. **Recommendation System**: Rule-based engine mapping skill deficits to specific online courses, platform resources, and career trajectories.
9. **PDF Report Compiler**: Full summary reports capturing profile details, ATS results, full interview transcripts, and recommendations, compiled into a downloadable PDF format.

---

## 📂 Project Structure

```
AI_Interview_Assistant/
├── app.py                         # Main landing portal and entrypoint
├── requirements.txt               # Required packages and dependencies
├── README.md                      # Setup and usage guide
├── database.db                    # SQLite Database file (Auto-generated)
├── assets/
│   └── style.css                  # Custom CSS styling overrides
├── database/
│   ├── database.py                # Connection manager and seeding
│   ├── models.py                  # SQL schemas & DDL definition
│   └── seed_data.py               # Seed bank of 300+ interview Q&As
├── pages/
│   ├── Home.py                    # Introduction and roadmap manual
│   ├── Login.py                   # User sign-in
│   ├── Register.py                # User registration
│   ├── Resume_Analysis.py         # Parsing and ATS Match score calculations
│   ├── Interview.py               # Interactive interview simulator
│   ├── Dashboard.py               # Performance charts and analytics
│   ├── Reports.py                 # Report downloads and recommendations
│   └── Profile.py                 # Account metadata and history lookup
├── utils/
│   ├── authentication.py          # Hashing and sign-in handlers
│   ├── resume_parser.py           # text extraction from PDF/docx
│   ├── skill_extractor.py         # spaCy/NLTK skill parsing
│   ├── jd_matcher.py              # Skill match alignments
│   ├── ats_score.py               # Hybrid ATS compatibility scorer
│   ├── ai_evaluator.py            # SBERT similarity and NLP metrics
│   ├── recommendation_engine.py   # Skill-gap course mapper
│   └── report_generator.py        # PDF report generator using fpdf2
├── resumes/                       # Temporary store for uploaded resumes (Auto-created)
└── reports/                       # Temporary store for generated PDFs (Auto-created)
```

---

## 🛠️ Setup & Installation Instructions

Follow these steps to run the application locally on your system:

### 1. Prerequisite Checks
Ensure you have **Python 3.12+** installed. Check your version with:
```bash
python --version
```

### 2. Download code and Navigate
Navigate to the directory containing the project:
```bash
cd AI_Interview_Assistant
```

### 3. Install Dependencies
Install all package requirements listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Setup Natural Language Processing Models
Download the small English spaCy model required for parsing (this will also auto-download on the first application parse if skipped):
```bash
python -m spacy download en_core_web_sm
```

### 5. Launch the Application
Start the Streamlit development server:
```bash
streamlit run app.py
```

Streamlit will boot up and host the app locally. It will automatically open in your default browser at `http://localhost:8501`.

---

## 🧠 Behind the Scenes: NLP & Machine Learning

* **ATS Scoring (TF-IDF & Cosine Similarity)**: We fit a `TfidfVectorizer` on the resume and job description texts to compute their term vectors. The cosine angle between these vectors represents text relevance.
* **Semantic Evaluation (SBERT)**: A lightweight `SentenceTransformer` model (`all-MiniLM-L6-v2`) encodes the candidate's answer and the ideal answer into 384-dimensional vectors. Cosine similarity calculates how closely the semantic meaning aligns.
* **Confidence Metrics**: We run word tokenizations to identify filler expressions (like *like*, *um*, *basically*, *literally*, *you know*). High ratios of filler occurrences deduct from the overall confidence rating.
* **Communication Richness**: We check the Type-Token Ratio (TTR - number of unique words divided by total words) to measure vocabulary variety, combined with sentence length ratios to determine clarity.

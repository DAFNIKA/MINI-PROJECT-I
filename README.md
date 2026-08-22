# 🤖 AI-Powered Interview Preparation Assistant

An AI-powered web application designed to help candidates prepare for interviews by analyzing resumes, matching profiles with job descriptions, generating skill-based interview questions, evaluating answers semantically, and providing personalized performance insights.

The application combines **Resume Parsing, ATS Scoring, NLP, Machine Learning, and Mock Interview Simulation** into a single interactive Streamlit dashboard.

---

## 🚀 Key Features

### 🔐 Secure Authentication

* User registration and login
* Secure password storage using **bcrypt hashing**
* Stateful user sessions

### 📄 Resume Parsing & Skill Extraction

* Supports **PDF and DOCX resumes**
* Extracts resume text and contact information
* Identifies technical skills from the candidate's profile
* Uses **spaCy NER** for skill extraction
* Supports a taxonomy containing **500+ technical skills**

### 🎯 ATS Compatibility Scoring

* Compares a candidate's resume with a given job description
* Uses **TF-IDF Vectorization**
* Calculates similarity using **Cosine Similarity**
* Generates an ATS compatibility score from **0 to 100%**

### 🎤 Mock Interview Simulator

* Generates interview questions based on extracted resume skills
* Supports multiple difficulty levels:

  * Easy
  * Medium
  * Hard
* Provides a realistic interview practice environment

### 🧠 Semantic Answer Evaluation

* Evaluates candidate answers against ideal answers
* Uses **Sentence-Transformers (SBERT)**
* Uses `all-MiniLM-L6-v2` for semantic similarity
* Includes NLTK-based analysis for:

  * Grammar-related heuristics
  * Filler-word detection
  * Response quality

### 📊 Analytics Dashboard

* Displays interview performance history
* Provides interactive charts using **Plotly**
* Tracks score progression
* Displays performance scoring brackets

### 📑 PDF Report Generation

Generates a downloadable interview report containing:

* Candidate profile
* Extracted skills
* ATS compatibility score
* Interview questions
* Candidate responses
* Evaluation scores
* Performance analysis
* Course recommendations

Reports are generated using **fpdf2**.

---

## 🛠️ Technology Stack

| Category             | Technologies                  |
| -------------------- | ----------------------------- |
| Frontend             | Streamlit, HTML, CSS          |
| Programming Language | Python                        |
| Database             | SQLite 3                      |
| NLP                  | spaCy, NLTK                   |
| Machine Learning     | Scikit-learn                  |
| Semantic Analysis    | Sentence-Transformers (SBERT) |
| Visualization        | Plotly                        |
| PDF Processing       | pdfplumber                    |
| Word Processing      | python-docx                   |
| PDF Generation       | fpdf2                         |
| Authentication       | bcrypt                        |

---

## 🧠 AI & NLP Components

### spaCy

Used for Natural Language Processing and Named Entity Recognition to identify relevant information from resumes.

### NLTK

Used for text processing, tokenization, and filler-word analysis.

### Sentence-Transformers

The application uses:

```text
all-MiniLM-L6-v2
```

to generate semantic embeddings and compare candidate answers with expected answers.

### Scikit-learn

Used for:

```text
TF-IDF Vectorization
Cosine Similarity
```

These techniques are used to calculate the ATS compatibility between a resume and job description.

---

## 📂 Project Structure

```text
AI-Interview-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── database.db
│
├── models/
│   └── ...
│
├── utils/
│   └── ...
│
├── assets/
│   └── ...
│
└── reports/
    └── ...
```

> The exact project structure may vary depending on the implementation.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Interview-Assistant.git
```

```bash
cd AI-Interview-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Download NLTK Resources

If required by the application:

```python
import nltk

nltk.download('punkt')
nltk.download('stopwords')
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔄 Application Workflow

```text
             ┌──────────────────┐
             │      Register    │
             │      / Login     │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │  Upload Resume   │
             │   PDF / DOCX     │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Resume Parsing   │
             │ & Skill Extract. │
             └────────┬─────────┘
                      │
             ┌────────┴─────────┐
             ▼                  ▼
    ┌─────────────────┐  ┌──────────────────┐
    │  ATS Scoring    │  │ Mock Interview   │
    │ Resume vs. JD   │  │ Question Gen.    │
    └────────┬────────┘  └────────┬─────────┘
             │                    │
             │                    ▼
             │           ┌──────────────────┐
             │           │ Answer Evaluation│
             │           │     SBERT + NLTK │
             │           └────────┬─────────┘
             │                    │
             └──────────┬─────────┘
                        ▼
               ┌──────────────────┐
               │ Analytics & PDF  │
               │     Report       │
               └──────────────────┘
```

---

## 📊 Main Modules

### Resume Analyzer

Analyzes uploaded resumes and extracts relevant candidate information and technical skills.

### ATS Analyzer

Measures how closely the candidate's resume matches a target job description.

### Interview Simulator

Creates personalized interview questions based on the candidate's skills and selected difficulty.

### Answer Evaluator

Compares candidate responses with expected answers using semantic similarity and linguistic heuristics.

### Analytics Dashboard

Provides visual insights into interview performance and score progression.

### Report Generator

Creates a structured PDF containing the candidate's interview preparation results.

---

## 🔮 Future Enhancements

* Voice-based mock interviews
* Speech-to-text answer evaluation
* Facial expression and confidence analysis
* Large Language Model-based question generation
* Personalized learning paths
* Job recommendation based on resume skills
* LinkedIn profile integration
* Real-time interview feedback
* Advanced ATS keyword analysis
* Cloud-based deployment
* Multi-language interview support

---

## 🎓 Project Information

**Project:** AI-Powered Interview Preparation Assistant

**Program:** Master of Computer Applications (MCA)

**Institution:** PSG College of Arts & Science, Coimbatore, India

**Author:** D. Dafnika

---

## 📜 License

This project is developed for **academic and educational purposes**.

---

## ⭐ Acknowledgement

This project demonstrates the application of **Artificial Intelligence, Natural Language Processing, Machine Learning, and Web Technologies** to improve the interview preparation process for job seekers.

# Resume Shortlister AI

## 0.1 Problem Statement
Build a Streamlit-based AI system where:
- HR inputs a Job Description and skills
- HR uploads multiple resumes
- System parses resumes
- System ranks candidates
- System explains *why* candidates are shortlisted

## 0.2 Architectural Philosophy
### Rule 1: Deterministic core
- Parsing, matching, scoring = pure Python + NLP
- Same input → same output every time
- No LLM involved in decisions

### Rule 2: AI is a narrator, not a judge
- Gemini explains results
- Gemini never changes scores
- Gemini never adds facts

### Rule 3: Streamlit constraints are law
- Limited RAM
- Cold starts
- No background workers
- No persistent local storage

## 0.5 Tech Stack
- **App**: Streamlit
- **Parsing**: pdfplumber, PyMuPDF, python-docx
- **NLP**: spaCy, sentence-transformers
- **AI**: Gemini 1.5 Flash
- **Core**: Python, NumPy, pandas

## Folder Contract
- `app.py`: Streamlit UI only
- `parsing/`: Text extraction & structuring
- `matching/`: Intelligence (scoring, skill matching)
- `explanation/`: Gemini explanation only
- `utils/`: Helpers

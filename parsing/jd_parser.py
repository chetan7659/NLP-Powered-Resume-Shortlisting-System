import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Explicitly warn or handle the missing model
    print("Warning: en_core_web_sm model not found. Run 'python -m spacy download en_core_web_sm'")
    # We might want to try to download it here or just fail graciously,
    # but strictly following the user code, I'll assume they might handle it or I'll just load it.
    # For robust code, I'll re-raise or let it fail if not found as per strict instructions.
    raise


def extract_experience(jd_text: str) -> int:
    match = re.search(r'(\d+)\s*\+?\s*years?', jd_text.lower())
    return int(match.group(1)) if match else 0


def extract_skills(jd_text: str) -> list:
    doc = nlp(jd_text.lower())
    skills = set()

    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 4:
            skills.add(chunk.text.strip())

    return list(skills)


def parse_jd(jd_text: str) -> dict:
    return {
        "required_skills": extract_skills(jd_text),
        "preferred_skills": [],
        "min_experience": extract_experience(jd_text)
    }

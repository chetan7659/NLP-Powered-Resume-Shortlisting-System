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
    """
    Extract years of experience from text.
    Handles multiple patterns:
    - Explicit: "3+ years", "5 years"
    - Date ranges: "2018-2023", "2020 - 2024"
    - Present/Current: "2020-present", "2019 - current"
    """
    from datetime import datetime
    
    # Try explicit "X years" pattern first
    match = re.search(r'(\d+)\s*\+?\s*years?', jd_text.lower())
    if match:
        return int(match.group(1))
    
    # Try date range pattern (YYYY-YYYY or YYYY - YYYY)
    date_ranges = re.findall(r'(\d{4})\s*[-–—]\s*(\d{4})', jd_text)
    if date_ranges:
        total_years = sum(int(end) - int(start) for start, end in date_ranges)
        return max(total_years, 0)  # Ensure non-negative
    
    # Try "present" or "current" pattern
    current_match = re.search(r'(\d{4})\s*[-–—]\s*(present|current|now)', jd_text.lower())
    if current_match:
        start_year = int(current_match.group(1))
        current_year = datetime.now().year
        return max(current_year - start_year, 0)
    
    return 0


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

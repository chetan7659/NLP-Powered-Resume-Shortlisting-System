import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
# Priority: Streamlit Secrets > Environment Variable (.env)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError):
    api_key = os.getenv("GEMINI_API_KEY")

try:
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in secrets or environment.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    # Handle cases where secrets are missing
    model = None
    print(f"Warning: Gemini configuration failed. Details: {e}")


def generate_explanation(match_data: dict) -> str:
    """
    Generates a natural language explanation for the candidate's score.
    Uses Gemini 1.5 Flash with a strict prompt to avoid hallucination.
    Falls back to structured explanation if Gemini is unavailable.
    """
    if not model:
        # Fallback: Generate structured explanation without Gemini
        return _generate_fallback_explanation(match_data)

    prompt = f"""
You are an HR assistant.

Explain why this candidate was shortlisted using ONLY the data below.
Do not assume or add information.
Be concise and professional.

Candidate evaluation data:
{match_data}

Explanation:
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # If Gemini fails, use fallback
        error_msg = str(e)
        if "suspended" in error_msg.lower() or "403" in error_msg:
            print(f"Warning: Gemini API key suspended. Using fallback explanation.")
        else:
            print(f"Warning: Gemini API error: {e}. Using fallback explanation.")
        return _generate_fallback_explanation(match_data)


def _generate_fallback_explanation(match_data: dict) -> str:
    """
    Generate structured explanation without Gemini.
    Used when API is unavailable or suspended.
    """
    final_score = match_data.get("final_score", 0)
    skill_match = match_data.get("skill_match", "0/0")
    experience_match = match_data.get("experience_match", "N/A")
    matched_skills = match_data.get("matched_skills", [])
    missing_skills = match_data.get("missing_skills", [])
    
    explanation = f"""**Candidate Score: {final_score}/100**

**Skills Match:** {skill_match}
- ✅ Matched: {', '.join(matched_skills) if matched_skills else 'None'}
- ⚠️ Missing: {', '.join(missing_skills) if missing_skills else 'None'}

**Experience:** {experience_match}

**Note:** AI explanation unavailable (API key issue). This is a structured summary of the scoring data.
"""
    return explanation

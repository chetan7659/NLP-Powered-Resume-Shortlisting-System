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
    """
    if not model:
        return "Error: Gemini API key not configured."

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
        return f"Error generating explanation: {str(e)}"

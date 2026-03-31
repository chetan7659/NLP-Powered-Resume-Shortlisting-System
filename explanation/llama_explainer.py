import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Model configuration - Using smaller model for Vercel compatibility
MODEL_NAME = "distilgpt2"  # Smaller GPT-2 model, better for serverless deployment

# Global variables for model and tokenizer
model = None
tokenizer = None
model_loaded = False

def load_model():
    """Load the model and tokenizer."""
    global model, tokenizer, model_loaded
    if not model_loaded:
        try:
            # Check for Hugging Face token
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            if not hf_token:
                print("Warning: HUGGINGFACE_TOKEN not found. Using fallback explanation.")
                return False

            print("Loading DistilGPT-2 model...")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=hf_token)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token

            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                token=hf_token,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                low_cpu_mem_usage=True
            )
            model_loaded = True
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Warning: Failed to load model. Details: {e}")
            model_loaded = False
            return False

# Don't load model on import - load only when needed

def generate_explanation(match_data: dict) -> str:
    """
    Generates a natural language explanation for the candidate's score.
    Uses Hugging Face model with a strict prompt to avoid hallucination.
    Falls back to structured explanation if model is unavailable.
    """
    # Try to load model if not loaded
    if not model_loaded:
        if not load_model():
            return _generate_fallback_explanation(match_data)

    if model is None or tokenizer is None:
        # Fallback: Generate structured explanation without model
        return _generate_fallback_explanation(match_data)

    prompt = f"""You are an HR assistant.

Explain why this candidate was shortlisted using ONLY the data below.
Do not assume or add information.
Be concise and professional.

Candidate evaluation data:
{match_data}

Explanation:"""

    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,  # Reduced for smaller model
                temperature=0.7,  # Slightly higher temperature for variety
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=3  # Prevent repetition
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the explanation part (after "Explanation:")
        explanation_start = response.find("Explanation:")
        if explanation_start != -1:
            explanation = response[explanation_start + len("Explanation:"):].strip()
        else:
            explanation = response[len(prompt):].strip()
        return explanation
    except Exception as e:
        print(f"Warning: Llama model error: {e}. Using fallback explanation.")
        return _generate_fallback_explanation(match_data)


def _generate_fallback_explanation(match_data: dict) -> str:
    """
    Generate structured explanation without Llama.
    Used when model is unavailable.
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

**Note:** AI explanation unavailable (model loading issue). This is a structured summary of the scoring data.
"""
    return explanation
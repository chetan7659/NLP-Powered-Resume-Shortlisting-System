from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st

import streamlit as st

# Load the model directly. In a real cold-start scenario, this might take a moment.
# Caching appropriately in Streamlit app.py will be important later.
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


def match_skills(resume_skills: list, jd_skills: list, threshold: float = 0.7) -> dict:
    if not resume_skills or not jd_skills:
        return {"matched": [], "missing": jd_skills, "match_ratio": 0.0}

    resume_emb = model.encode(resume_skills)
    jd_emb = model.encode(jd_skills)

    matched = []
    missing = []

    for i, jd_skill in enumerate(jd_skills):
        # We need to reshape jd_emb[i] to be (1, embedding_dim)
        similarities = cosine_similarity(
            [jd_emb[i]], resume_emb
        )[0]

        if max(similarities) >= threshold:
            matched.append(jd_skill)
        else:
            missing.append(jd_skill)

    match_ratio = len(matched) / len(jd_skills)

    return {
        "matched": matched,
        "missing": missing,
        "match_ratio": round(match_ratio, 2)
    }

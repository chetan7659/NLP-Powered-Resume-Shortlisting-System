# Improvement Roadmap

## 1. Critical Deployment Fixes (Implemented)
- **Problem**: `en_core_web_sm` model missing on Streamlit Cloud.
- **Fix**: Added direct URL dependency to `requirements.txt`.

## 2. Performance & Robustness (Recommended)
- **Model Caching**: The `sentence-transformers` model loads on every script rerun.
  - *Fix*: Wrap model loading with `@st.cache_resource` in `skill_matcher.py` or `app.py`.
- **Error Handling**: Currently, if one resume fails slightly, it might be caught, but detailed logs are missing.
  - *Fix*: Add a structured logger.

## 3. Logic Enhancements (Phase 1.5)
- **Project Scoring**: Currently hardcoded to `0.5`.
  - *Fix*: Implement a regex counter for words like "Led", "Created", "Managed", "Built" to give a proxy score for "Doer" vs "Watcher".
- **Skill Extraction**: Currently misses skills > 3 words (e.g., "Google Cloud Platform").
  - *Fix*: Increase noun chunk limit or use a predefined skill database (JSON) for exact lookup.
- **Experience Extraction**: Naive regex (`\d+ years`).
  - *Fix*: Handle "Jan 2020 - Present" date math parsing for higher accuracy.

## 4. UI/UX
- **Resume Preview**: PDF viewer is not implemented.
- **Score Explanation**: Display the distribution of scores (charts).

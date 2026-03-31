from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os
import tempfile
import shutil
from typing import List
import pandas as pd

# Import your existing modules
try:
    from parsing import resume_parser, jd_parser
    from matching import skill_matcher, scorer
    from explanation import llama_explainer
    from utils import logger, skill_taxonomy
    MODULES_LOADED = True
except ImportError as e:
    print(f"Warning: Some modules failed to import: {e}")
    MODULES_LOADED = False

app = FastAPI(title="AI Resume Shortlister API")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/evaluate")
async def evaluate_candidates(
    jd_text: str = Form(...),
    skills_text: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not MODULES_LOADED:
        raise HTTPException(status_code=500, detail="Required modules not loaded. Check dependencies.")

    try:
        # Validate inputs
        if not jd_text:
            raise HTTPException(status_code=400, detail="Job Description is required")
        if not skills_text:
            raise HTTPException(status_code=400, detail="Skills are required")
        if not files:
            raise HTTPException(status_code=400, detail="At least one resume file is required")

        if len(jd_text) > 10000:
            raise HTTPException(status_code=400, detail="Job Description too long (max 10,000 characters)")

        # Parse job description
        jd_skills = jd_parser.extract_skills_from_jd(jd_text)
        manual_skills = [skill.strip() for skill in skills_text.split(",") if skill.strip()]
        required_skills = list(set(jd_skills + manual_skills))

        results = []

        # Process each resume
        for file in files:
            if not file.filename.lower().endswith(('.pdf', '.docx')):
                continue

            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
                shutil.copyfileobj(file.file, temp_file)
                temp_path = temp_file.name

            try:
                # Parse resume
                resume_data = resume_parser.parse_resume(temp_path)

                # Match skills
                skill_matches = skill_matcher.match_skills(resume_data['skills'], required_skills)

                # Calculate score
                score_data = scorer.calculate_score(
                    resume_data,
                    required_skills,
                    jd_text,
                    skill_matches
                )

                # Generate explanation
                explanation = llama_explainer.generate_explanation(score_data)

                results.append({
                    "name": file.filename,
                    "score": score_data["final_score"],
                    "match_ratio": score_data["skill_match"],
                    "experience": score_data["experience_match"],
                    "explanation": explanation
                })

            finally:
                # Clean up temp file
                os.unlink(temp_path)

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)

        return {"results": results}

    except Exception as e:
        logger.log_error(f"Evaluation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
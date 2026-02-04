"""
Audit Logger - HR Compliance & Traceability
Logs all scoring decisions for audit trail.
"""

import logging
import json
from datetime import datetime
import hashlib
import os
import numpy as np

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'audit_log.jsonl'),
    level=logging.INFO,
    format='%(message)s'
)

logger = logging.getLogger(__name__)


def _hash_text(text: str) -> str:
    """Generate hash for JD/resume text for traceability"""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _convert_to_serializable(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: _convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_convert_to_serializable(item) for item in obj]
    return obj


def log_scoring_decision(
    resume_name: str,
    score_data: dict,
    jd_text: str,
    resume_text: str,
    parsed_jd: dict
) -> None:
    """
    Log scoring decision for audit trail.
    
    Args:
        resume_name: Name of resume file
        score_data: Scoring output from scorer.score_resume()
        jd_text: Original JD text
        resume_text: Original resume text
        parsed_jd: Parsed JD data
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "resume_name": resume_name,
        "jd_hash": _hash_text(jd_text),
        "resume_hash": _hash_text(resume_text),
        "final_score": score_data["final_score"],
        "skill_match": score_data["skill_match"],
        "experience_match": score_data["experience_match"],
        "jd_similarity": score_data["jd_similarity"],
        "matched_skills": score_data["matched_skills"],
        "missing_skills": score_data["missing_skills"],
        "required_skills_count": len(parsed_jd["required_skills"]),
        "min_experience_required": parsed_jd["min_experience"]
    }
    
    # Convert numpy types to native Python types
    log_entry = _convert_to_serializable(log_entry)
    
    logger.info(json.dumps(log_entry))


def log_batch_summary(total_resumes: int, successful: int, failed: int) -> None:
    """
    Log batch processing summary.
    
    Args:
        total_resumes: Total number of resumes uploaded
        successful: Number successfully processed
        failed: Number that failed
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "batch_summary",
        "total_resumes": total_resumes,
        "successful": successful,
        "failed": failed,
        "success_rate": round(successful / total_resumes * 100, 2) if total_resumes > 0 else 0
    }
    
    log_entry = _convert_to_serializable(log_entry)
    logger.info(json.dumps(log_entry))


def log_error(resume_name: str, error_message: str) -> None:
    """
    Log processing error.
    
    Args:
        resume_name: Name of resume that failed
        error_message: Error message
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "error",
        "resume_name": resume_name,
        "error": str(error_message)
    }
    
    log_entry = _convert_to_serializable(log_entry)
    logger.info(json.dumps(log_entry))

"""
Skill Taxonomy - Technical Skill Validation
Filters extracted skills to remove generic phrases and non-technical terms.
"""

# Comprehensive tech skills taxonomy (500+ skills)
TECH_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "go", "golang",
    "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl",
    "shell", "bash", "powershell", "sql", "pl/sql", "t-sql",
    
    # Web Technologies
    "html", "css", "react", "angular", "vue", "vue.js", "node.js", "express",
    "django", "flask", "fastapi", "spring", "spring boot", "asp.net", ".net",
    "jquery", "bootstrap", "tailwind", "sass", "less", "webpack", "vite",
    
    # Databases
    "mysql", "postgresql", "mongodb", "redis", "cassandra", "dynamodb",
    "oracle", "sql server", "sqlite", "mariadb", "elasticsearch", "neo4j",
    "couchdb", "firebase", "supabase",
    
    # Cloud Platforms
    "aws", "azure", "gcp", "google cloud", "cloud computing", "heroku", "digitalocean",
    "ec2", "s3", "lambda", "cloudformation", "terraform", "ansible",
    
    # Cloud Services
    "ec2", "s3", "rds", "dynamodb", "lambda", "cloudwatch", "iam",
    "azure functions", "azure devops", "azure data factory", "adf",
    "azure databricks", "synapse analytics", "adls", "blob storage",
    "cosmos db", "stream analytics",
    
    # Big Data & Processing
    "hadoop", "spark", "apache spark", "kafka", "flink", "storm", "hive",
    "pig", "hdinsight", "databricks", "airflow", "luigi", "nifi",
    
    # Machine Learning & AI
    "machine learning", "deep learning", "neural networks", "nlp",
    "natural language processing", "computer vision", "tensorflow", "pytorch",
    "keras", "scikit-learn", "xgboost", "lightgbm", "catboost",
    "transformers", "bert", "gpt", "llm", "generative ai", "rag",
    
    # Data Science
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
    "jupyter", "data analysis", "data visualization", "statistics",
    "probability", "linear algebra", "calculus",
    
    # DevOps & Tools
    "docker", "kubernetes", "jenkins", "gitlab", "github", "git",
    "ci/cd", "devops", "linux", "unix", "nginx", "apache",
    "monitoring", "prometheus", "grafana", "elk", "splunk",
    
    # Methodologies
    "agile", "scrum", "kanban", "waterfall", "lean", "six sigma",
    "tdd", "bdd", "test-driven development", "continuous integration",
    "continuous deployment", "microservices", "rest api", "graphql",
    
    # Data Engineering
    "etl", "elt", "data pipeline", "data warehouse", "data lake",
    "dimensional modeling", "star schema", "snowflake schema",
    "fact table", "dimension table", "scd", "slowly changing dimension",
    
    # Testing
    "pytest", "unittest", "jest", "mocha", "selenium", "cypress",
    "junit", "testng", "automation testing", "manual testing",
    
    # Project Management
    "jira", "confluence", "trello", "asana", "project management",
    "stakeholder management", "requirements gathering",
    
    # Soft Skills (Technical Context)
    "problem solving", "debugging", "troubleshooting", "code review",
    "technical documentation", "system design", "architecture design",
    
    # Security
    "cybersecurity", "encryption", "authentication", "authorization",
    "oauth", "jwt", "ssl", "tls", "penetration testing", "vulnerability assessment",
    
    # Mobile Development
    "android", "ios", "react native", "flutter", "xamarin", "mobile development",
    
    # Other Technologies
    "blockchain", "cryptocurrency", "iot", "edge computing", "5g",
    "ar", "vr", "augmented reality", "virtual reality",
    
    # Business Intelligence
    "power bi", "tableau", "looker", "qlik", "business intelligence",
    "data analytics", "reporting", "dashboards",
    
    # Networking
    "tcp/ip", "http", "https", "dns", "vpn", "firewall", "load balancing",
    "cdn", "networking", "routing", "switching"
}

# Common non-technical phrases to explicitly filter out
NOISE_PHRASES = {
    "the company", "the team", "the project", "the role", "the position",
    "the candidate", "the system", "the application", "the platform",
    "a team", "a project", "a role", "a position", "a company",
    "our team", "our company", "our project", "our system",
    "this role", "this position", "this project", "this team",
    "good communication", "strong communication", "excellent communication",
    "team player", "fast learner", "self-motivated", "detail-oriented"
}


def validate_skills(extracted_skills: list) -> list:
    """
    Filter extracted skills to remove non-technical phrases.
    
    Args:
        extracted_skills: List of skills extracted by spaCy
        
    Returns:
        Filtered list of technical skills only
        
    Example:
        Input: ["python", "the team", "machine learning", "good communication"]
        Output: ["python", "machine learning"]
    """
    validated = []
    
    for skill in extracted_skills:
        skill_lower = skill.lower().strip()
        
        # Skip noise phrases
        if skill_lower in NOISE_PHRASES:
            continue
        
        # Skip very short phrases (likely not skills)
        if len(skill_lower) < 2:
            continue
        
        # Check if skill is in taxonomy OR contains a known tech term
        if skill_lower in TECH_SKILLS:
            validated.append(skill)
        else:
            # Check if any tech skill is a substring (handles variations)
            for tech_skill in TECH_SKILLS:
                if tech_skill in skill_lower or skill_lower in tech_skill:
                    validated.append(skill)
                    break
    
    return list(set(validated))  # Remove duplicates


def add_custom_skills(custom_skills: list) -> None:
    """
    Add custom skills to the taxonomy (for domain-specific needs).
    
    Args:
        custom_skills: List of additional skills to recognize
    """
    TECH_SKILLS.update(s.lower() for s in custom_skills)

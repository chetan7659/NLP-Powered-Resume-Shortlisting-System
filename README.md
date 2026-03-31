# NLP-Powered Resume Shortlisting System

## 0.1 Problem Statement
Build a Streamlit-based AI system where:
- HR inputs a Job Description and skills
- HR uploads multiple resumes
- System parses resumes
- System ranks candidates
- System explains *why* candidates are shortlisted

## 0.2 Architectural Philosophy
### Rule 1: Deterministic core
- Parsing, matching, scoring = pure Python + NLP
- Same input → same output every time
- No LLM involved in decisions

### Rule 2: AI is a narrator, not a judge
- Hugging Face Llama explains results
- Llama never changes scores
- Llama never adds facts

### Rule 3: Streamlit constraints are law
- Limited RAM
- Cold starts
- No background workers
- No persistent local storage

## 0.5 Tech Stack
- **App**: FastAPI + HTML/CSS (Vercel-deployable)
- **Parsing**: pdfplumber, PyMuPDF, python-docx
- **NLP**: spaCy, sentence-transformers
- **AI**: Hugging Face DistilGPT-2 (Vercel-compatible)
- **Core**: Python, NumPy, pandas

## Folder Contract
- `api/index.py`: FastAPI serverless function (Vercel deployment)
- `templates/index.html`: Web frontend
- `static/`: Static assets
- `parsing/`: Text extraction & structuring
- `matching/`: Intelligence (scoring, skill matching)
- `explanation/`: DistilGPT-2 explanation only
- `utils/`: Helpers

## 🚀 Deployment to Vercel

### Prerequisites
1. **Hugging Face Account & Token**:
   - Sign up at [Hugging Face](https://huggingface.co/)
   - Go to Settings → Access Tokens
   - Create a token with "Read" permissions
   - Accept the terms for [Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)

2. **Vercel Account**: Sign up at [Vercel](https://vercel.com)

### Environment Variables
Create a `.env` file with:
```
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI locally
cd api
uvicorn index:app --reload

# Or run Streamlit version
streamlit run app.py
```

### Deploy to Vercel
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Vercel deployment support"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Configure project settings:
     - **Framework Preset**: Other
     - **Root Directory**: NLP-Powered-Resume-Shortlisting-System
     - **Build Command**: (leave empty)
     - **Output Directory**: (leave empty)

3. **Environment Variables**:
   - Add `HUGGINGFACE_TOKEN` in Vercel's project settings

4. **Deploy**: Click "Deploy"

### Quick Deploy (Windows)
Run the deployment script:
```cmd
deploy.bat
```

### Quick Deploy (Linux/Mac)
Run the deployment script:
```bash
chmod +x deploy.sh
./deploy.sh
```

### ⚠️ Important Limitations
- **Model Size**: Llama-2-7b-chat-hf is large (~14GB) and may exceed Vercel's limits
- **Memory**: Vercel serverless functions have memory limits
- **Cold Starts**: First request may be slow due to model loading
- **Timeout**: Vercel has a 30-second timeout limit

### Alternative: Use Lighter Model
For better Vercel performance, consider using a smaller model like:
- `microsoft/DialoGPT-small`
- `distilbert-base-uncased`
- Or stick with the fallback explanation

### Troubleshooting
- **Model Loading Issues**: Check if you accepted the model terms on Hugging Face
- **Memory Errors**: Consider using a smaller model or CPU-only inference
- **Timeout Errors**: The model loading might take too long - consider pre-loading or using a lighter model

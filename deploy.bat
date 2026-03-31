@echo off
echo 🚀 Deploying NLP Resume Shortlister to Vercel

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI not found. Install it with: npm install -g vercel
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist "vercel.json" (
    echo ❌ vercel.json not found. Are you in the project root?
    pause
    exit /b 1
)

REM Check for environment variables
if not exist ".env" (
    echo ⚠️  .env file not found. Make sure to create it with HUGGINGFACE_TOKEN
)

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🔍 Checking for required files...
set "required_files=api/index.py templates/index.html requirements.txt vercel.json"
for %%f in (%required_files%) do (
    if not exist "%%f" (
        echo ❌ Required file missing: %%f
        pause
        exit /b 1
    )
)

echo ✅ All required files present

echo 🌐 Deploying to Vercel...
vercel --prod

echo 🎉 Deployment complete!
echo 📋 Don't forget to:
echo    1. Set HUGGINGFACE_TOKEN in Vercel dashboard
echo    2. Test the deployment
echo    3. Monitor for memory/timeout issues

pause
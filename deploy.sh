#!/bin/bash

echo "🚀 Deploying NLP Resume Shortlister to Vercel"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Install it with: npm install -g vercel"
    exit 1
fi

# Check if in correct directory
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found. Are you in the project root?"
    exit 1
fi

# Check for environment variables
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Make sure to create it with HUGGINGFACE_TOKEN"
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔍 Checking for required files..."
required_files=("api/index.py" "templates/index.html" "requirements.txt" "vercel.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file missing: $file"
        exit 1
    fi
done

echo "✅ All required files present"

echo "🌐 Deploying to Vercel..."
vercel --prod

echo "🎉 Deployment complete!"
echo "📋 Don't forget to:"
echo "   1. Set HUGGINGFACE_TOKEN in Vercel dashboard"
echo "   2. Test the deployment"
echo "   3. Monitor for memory/timeout issues"
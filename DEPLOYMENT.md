# 🚀 Deployment Guide for AI QA Genesis

## Overview

This guide will help you deploy the AI QA Genesis application to free cloud platforms.

## 📋 Prerequisites

1. **Google Gemini API Key** - Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **GitHub Account** - Your code should be pushed to GitHub
3. **Free hosting accounts** (we'll create these below)

---

## 🎯 Deployment Architecture

- **Backend (FastAPI)**: Deploy to **Render.com** (Free)
- **Frontend (Streamlit)**: Deploy to **Streamlit Community Cloud** (Free)

---

## Part 1: Deploy Backend to Render.com

### Step 1: Sign Up for Render

1. Go to [render.com](https://render.com/)
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"

### Step 2: Configure Backend Service

1. **Connect Repository**: Select your `Autonomous-QA-Agent` repository
2. **Configure Settings**:
   - **Name**: `qa-agent-backend` (or your choice)
   - **Region**: Select nearest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**:
   - Click "Add Environment Variable"
   - Key: `GOOGLE_API_KEY`
   - Value: Your Google Gemini API key
   
4. **Plan**: Select "Free"

5. Click **"Create Web Service"**

### Step 3: Get Backend URL

Once deployment completes (5-10 minutes), you'll get a URL like:
```
https://qa-agent-backend.onrender.com
```

**⚠️ Important**: Copy this URL, you'll need it for the frontend!

---

## Part 2: Deploy Frontend to Streamlit Cloud

### Step 1: Sign Up for Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"

### Step 2: Configure Streamlit App

1. **Repository**: Select `Autonomous-QA-Agent`
2. **Branch**: `main`
3. **Main file path**: `app/ui.py`
4. **Advanced settings** → **Python version**: `3.11`

### Step 3: Set Environment Variables

Click "Advanced settings" → "Secrets" and add:

```toml
GOOGLE_API_KEY = "your_google_api_key_here"
BACKEND_URL = "https://qa-agent-backend.onrender.com"
```

Replace the `BACKEND_URL` with your actual Render backend URL from Part 1, Step 3.

### Step 4: Deploy

1. Click **"Deploy!"**
2. Wait 3-5 minutes for deployment

Your app will be live at:
```
https://your-app-name.streamlit.app
```

---

## 🎉 You're Live!

Your AI QA Genesis application is now deployed! Test it by:

1. Open your Streamlit app URL
2. Upload documents in the "Knowledge Ingestion" tab
3. Generate test cases
4. Generate Selenium scripts

---

## 🔧 Alternative Free Platforms

### Backend Alternatives

**Railway.app**
- Free tier: $5 credit/month
- Deployment: Connect GitHub → Select repo → Deploy
- Add `GOOGLE_API_KEY` environment variable

**Fly.io**
- Free tier available
- Command: `fly launch` (requires Fly CLI)

### Frontend Alternatives

**Hugging Face Spaces**
- Free for public apps
- Create Space → Select Streamlit → Connect GitHub

---

## ⚠️ Important Notes

### ChromaDB Storage

- **Current Setup**: In-memory storage (data is lost on restart)
- **Why**: Free cloud platforms don't provide persistent disk storage
- **Solution**: Users need to re-upload documents after each deployment/restart
- **Future**: Consider upgrading to a paid tier or using a cloud vector database

### Free Tier Limitations

**Render.com**:
- Spins down after 15 minutes of inactivity
- First request after sleep takes ~30 seconds

**Streamlit Cloud**:
- Public apps only (private apps need paid plan)
- Limited resources

### Keeping Backend Alive

To prevent Render backend from sleeping, you can:
1. Use a service like [UptimeRobot](https://uptimerobot.com/) to ping your backend every 10 minutes
2. Or accept the ~30 second cold start on first request

---

## 🐛 Troubleshooting

### Backend not responding?
- Check Render logs: Dashboard → Your service → Logs
- Verify `GOOGLE_API_KEY` is set correctly
- Ensure `Procfile` exists in your repo

### Frontend can't connect to backend?
- Verify `BACKEND_URL` in Streamlit secrets matches your Render URL
- Check backend is actually running (visit backend URL directly)

### API Quota errors?
- You're hitting Google Gemini API rate limits
- Wait a few minutes or upgrade your Google Cloud quota

---

## 📞 Support

For issues:
1. Check the logs in Render/Streamlit dashboards
2. Verify environment variables are set correctly
3. Ensure your Google API key is valid and has quota remaining

---

Happy Deploying! 🚀

# 💸 Free Deployment Guide (Google Gemini + Render)

Yes, you can deploy this completely for **FREE**! To do this, we switch from expensive/local models to Google's generous free tier and free hosting.

---

## Part 1: Get the Brains (Google Gemini) - Costs $0/mo

Google offers a free tier for Gemini Pro (60 queries/minute), which is plenty for this app.

1.  Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
2.  Log in with your Google Account.
3.  Click **Create API Key**.
4.  Copy the key.
5.  Open your `.env` file locally (or environment variables on cloud):
    *   Set `USE_GEMINI=True`
    *   Set `GEMINI_API_KEY=your_copied_key_here`
    *   Ensure `USE_AWS_BEDROCK=False`.

---

## Part 2: Get the Hosting (Render) - Costs $0/mo

Render offers a "Web Service" free tier that can run Python apps.

### 1. Push Code to GitHub
*   Create a repository on GitHub (e.g., `my-rag-app`).
*   Push your project code there.

### 2. Create Web Service on Render
1.  Go to **[Render.com](https://render.com/)** and sign up.
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  **Settings**:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables** (Add these in the Render Dashboard):
    *   `USE_GEMINI`: `True`
    *   `GEMINI_API_KEY`: *(Paste your Google Key)*
    *   `PYTHON_VERSION`: `3.10.0` (Optional but good practice)
6.  Click **Deploy Web Service**.

### 🔍 Important Limitation
*   **Ephemeral Files**: On the free tier, Render wipes the hard drive every time the app restarts (which happens often).
*   **Impact**: Your uploaded documents (Knowledge Base) will be **deleted** when the server sleeps. You will need to re-upload them each time you open the app after a break.
*   **Solution**: Since this is for a demo/portfolio, this is usually acceptable!

---

## Summary
*   **Intelligence**: Google Gemini (Free Tier)
*   **Hosting**: Render (Free Tier)
*   **Total Cost**: **$0.00** 

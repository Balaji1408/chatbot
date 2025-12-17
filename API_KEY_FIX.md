# 🚨 CRITICAL: Your API Key Was Leaked

The error message `403 PERMISSION_DENIED: Your API key was reported as leaked` means Google detected your API Key in a public place (like your GitHub repository history) and **automatically disabled it** to protect you.

This is a standard security feature. The key you are using on Render is now **dead**.

## ⚡ How to Fix (3 Steps)

### 1. Get a New Key
1.  Go back to **[Google AI Studio](https://aistudio.google.com/app/apikey)**.
2.  Click **Create API Key** (or delete the old one and create a new one).
3.  **COPY** the new key.

### 2. Update Render (Production)
1.  Go to your **[Render Dashboard](https://dashboard.render.com/)**.
2.  Click on your **"Chat Bot"** (cortex-rag) service.
3.  Click **Environment** (left sidebar).
4.  Find `GEMINI_API_KEY`.
5.  Click **Edit** and paste the **NEW** key.
6.  Click **Save Changes**.
    *   *Render will automatically restart your app.*

### 3. Update Local (Development)
1.  Open your local `.env` file.
2.  Paste the new key: `GEMINI_API_KEY=AIzaSy...`
3.  **IMPORTANT**: Do **NOT** run `git add .env` or try to push this file. 
    *   We already added it to `.gitignore`, but please be careful.
    *   Secrets should **never** go to GitHub.

---

### Verify
Once Render restarts (usually 1-2 minutes), try the chat again. It will work immediately.

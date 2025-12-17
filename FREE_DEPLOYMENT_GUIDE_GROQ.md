# 🦙 Free Deployment Guide (Llama 3 via Groq + Render)

Yes, you can deploy this completely for **FREE** using Llama 3! We use **Groq**, which provides incredibly fast and currently free API access to Llama models.

---

## Part 1: Get the Brains (Groq) - Costs $0/mo

Groq offers a generous free tier for Llama 3 models.

1.  Go to **[Groq Console](https://console.groq.com/keys)**.
2.  Log in (likely with Google/GitHub).
3.  Click **Create API Key**.
4.  Name it (e.g., `render-bot`).
5.  Copy the key (starts with `gsk_...`).

---

## Part 2: Configure Your App

### Local Development
1.  Open your `.env` file.
2.  Set `USE_GROQ=True`.
3.  Set `GROQ_API_KEY=your_copied_key_here`.
4.  Ensure `USE_AWS_BEDROCK=False` and `USE_GEMINI=False`.

### Render Deployment (Cloud)

1.  Go to your **Generic Web Service** on Render.
2.  Go to **Environment**.
3.  Add/Update these Environment Variables:

| Variable | Value |
| :--- | :--- |
| `USE_GROQ` | `True` |
| `GROQ_API_KEY` | *(Paste your gsk_... key)* |
| `GROQ_MODEL` | `llama-3.1-8b-instant` (or `llama-3.3-70b-versatile`) |
| `USE_AWS_BEDROCK` | `False` |
| `USE_GEMINI` | `False` |

4.  **Save Changes**. Render will redeploy automatically.

---

## ⚡ Why Groq?
*   **Speed**: It is the fastest inference engine for Llama models.
*   **Cost**: Currently offers specific models for free.
*   **Quality**: You get Llama 3 8B or 70B, which are state-of-the-art open models.

---

## Troubleshooting
*   **Rate Limits**: If the bot stops responding with an error about limits, wait a minute or switch to valid paid credits if you scale up. For personal portfolios, the free tier is huge.

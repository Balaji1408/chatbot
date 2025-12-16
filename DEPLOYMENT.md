# 🚀 Deployment Guide

This project is currently designed to run **locally** using `Ollama` for the LLM and Embeddings. Deploying it to the cloud requires choosing between maintaining the local LLM (expensive) or switching to a Cloud API (cheap/efficient).

---

## Option 1: Deploy with Ollama (Current Code - GPU Required)

Since the project runs the AI models locally, you need a server with a powerful **GPU** and heavily resources (RAM).

### Recommended Platforms
1.  **AWS EC2 (G4/G5 Instances)**
    *   **Instance Type**: `g4dn.xlarge` (Minimum recommended).
    *   **Cost**: ~$0.50 - $1.00+ per hour (approx. $300-$700/month).
    *   **Setup**: Install Docker, Nvidia Drivers, pull Ollama models, and run the FastAPI app.
2.  **GPU Clouds (Lambda Labs, RunPod, Railway GPU)** 
    *   Often cheaper than AWS for raw GPU power.
    *   **Railway**: Supports deploying Dockerfiles but GPU tiers are paid.

**Why this is hard**: "Free" tiers (like Vercel, Heroku free, AWS t2.micro) **cannot** run Ollama/LLMs. They lack the memory and GPU power.

---

## Option 2: Switch to AWS Bedrock (Serverless - Cheaper/Free Tier Friendly)

To deploy on standard "Free Tier" infrastructure (like AWS App Runner, ECS, or Vercel), you must **remove Ollama** and use a Cloud API like AWS Bedrock.

### How to Refactor for Bedrock:
1.  **Embeddings**: Switch `HuggingFaceEmbeddings` (local) to `BedrockEmbeddings`.
2.  **LLM**: Switch `ChatOllama` to `ChatBedrock`.
3.  **Deploy**: Once changed, the app is just a lightweight Python API.
    *   **AWS App Runner**: Easy container deployment.
    *   **Render / Railway**: Supports simple Python apps.

### Is AWS Bedrock Free?
**Not exactly.** Unlike EC2's "12-months free", Bedrock is **Pay-Per-Token**.
*   **Pricing**: You pay for every word you send/receive (~$0.0004/1k tokens for Llama 3).
*   **Free Tier Experimentation**:
    *   **PartyRock**: AWS offers a playground called PartyRock.aws which is free for experimentation.
    *   **Credits**: New AWS accounts sometimes get credits ($300) which can be used for Bedrock.
    *   **On-Demand**: There is no "forever free" tier for the Bedrock API calls themselves, but they are very cheap for low volume.

---

## ☁️ Deployment Steps (General)

### 1. Dockerize the Application
Create a `Dockerfile` in the root:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# If using Option 1 (Ollama), you need complex setup here to run Ollama inside OR connect to external Ollama URL.
# If using Option 2 (Bedrock), just run the app:
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Build & Push
*   Build the image: `docker build -t cortex-rag .`
*   Push to AWS ECR or Docker Hub.

### 3. Run
*   Point your cloud service (App Runner/Render) to the Docker image.
*   Set Environment Variables (API Keys, AWS Credentials).

# ☁️ How to Get AWS Access Keys (and Is it Free?)

To use the "Cloud Mode" of this application, you need AWS credentials. Here represents the steps to get them.

## 1. Is it Free?
**The Short Answer:** No, but it's very cheap.

*   **AWS Free Tier**: When you create a *new* AWS account, you get 12 months of free usage for many services (EC2 micro instances, S3 storage, etc.).
*   **Bedrock (AI Models)**: This service is **NOT** part of the "Always Free" tier.
    *   **Price**: You pay per word (token).
    *   **Example Cost**: Processing 1,000 queries might cost you ~$0.10 - $0.50 depending on the model.
    *   **New Account Credits**: Sometimes new accounts get $300 in credits. If you have these, then yes, it is "free" until credits run out.

---

## 2. How to Get Access Keys (Step-by-Step)

You need an **IAM User** (Identity and Access Management) with permissions to use Bedrock.

### Step A: Create an AWS Account
1.  Go to [aws.amazon.com](https://aws.amazon.com/).
2.  Click **Create an AWS Account** and follow the signup process (requires credit card).

### Step B: Enable Bedrock Models
*(Important! Models are disabled by default)*
1.  Log in to the **AWS Console**.
2.  Search for **"Bedrock"** in the top search bar.
3.  In the left sidebar, click **Model access**.
4.  Click **Manage model access** (Top right orange button).
5.  Check the boxes for:
    *   **Amazon**: Titan Embeddings G1 - Text
    *   **Meta**: Llama 3 (8B Instruct or 70B Instruct)
    *   *Note: You might need to submit a use-case form for some models.*
6.  Click **Save changes**.

### Step C: Create IAM User & Keys
1.  Search for **"IAM"** in the top search bar.
2.  Click **Users** -> **Create user**.
3.  **Name**: Give it a name like `cortex-rag-user`. Click **Next**.
4.  **Permissions**:
    *   Select **Attach policies directly**.
    *   Search for `AmazonBedrockFullAccess` and check the box.
    *   Click **Next** -> **Create user**.
5.  **Get Keys**:
    *   Click on the newly created user name.
    *   Go to the **Security credentials** tab.
    *   Scroll down to **Access keys**.
    *   Click **Create access key**.
    *   Select **Local code** -> Check the "I understand..." box -> **Next**.
    *   Click **Create access key**.

### Step D: Copy to Project
1.  You will see `Access key ID` and `Secret access key`.
2.  **COPY THEM NOW**. You cannot see the secret key again later.
3.  Paste them into your `.env` file:
    ```env
    AWS_ACCESS_KEY_ID=AKIA......
    AWS_SECRET_ACCESS_KEY=wJalr......
    ```

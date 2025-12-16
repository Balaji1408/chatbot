from langchain_community.chat_models import ChatOllama
from app.core.config import settings
import asyncio

async def test():
    print(f"Connecting to Ollama at {settings.OLLAMA_BASE_URL} with model {settings.LLM_MODEL}")
    llm = ChatOllama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.LLM_MODEL,
        temperature=0.0
    )
    
    try:
        response = await llm.ainvoke("Why is the sky blue?")
        print("Success!")
        print(response.content)
    except Exception as e:
        print("Failed!")
        print(e)

if __name__ == "__main__":
    asyncio.run(test())

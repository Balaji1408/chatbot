from typing import List, AsyncIterable
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.core.prompts import QA_SYSTEM_PROMPT

class LLMService:
    def __init__(self):
        if settings.USE_AWS_BEDROCK:
            from langchain_aws import ChatBedrock
            import boto3
            
            boto3_session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            self.llm = ChatBedrock(
                client=boto3_session.client("bedrock-runtime"),
                model_id=settings.BEDROCK_MODEL_ID,
                model_kwargs={"temperature": 0.3}
            )
        elif settings.USE_GEMINI:
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            # Fallback to hardcoded 'gemini-pro' if env var is stuck/broken
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.3
            )
        else:
            self.llm = ChatOllama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.LLM_MODEL,
                temperature=0.3  # Slight creativity for general Qs
            )

    async def generate_answer_stream(self, question: str, context_docs: List[object]):
        # Format context
        formatted_context = "\n\n".join([f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}" for doc in context_docs])
        
        # Use the central system prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", QA_SYSTEM_PROMPT),
            ("human", "{question}"),
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            async for chunk in chain.astream({
                "context": formatted_context,
                "question": question
            }):
                yield chunk
        except Exception as e:
            yield f"\n\n[System Error: {str(e)}]"

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()

def get_generator_model():
    return ChatOpenAI(
        model=os.getenv("GEN_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        openai_api_key=os.getenv("GROQ_API_KEY"),
        base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
        timeout=30
    )


def get_judge_model():
    return ChatOpenAI(
        model=os.getenv("JUDGE_MODEL", "deepseek-chat"),
        temperature=0,
        openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        timeout=30
    )
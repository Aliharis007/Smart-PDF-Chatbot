# app/groq_setup.py

import os
from langchain_groq import ChatGroq

def get_groq_llm():
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )

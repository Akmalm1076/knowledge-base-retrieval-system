import google.generativeai as genai
from app.exceptions import GeminiException
from app.core.config import settings
from app.core.logging_config import logger
# Handles Gemini API configuration and response generation.
# Loads API keys securely from environment variables and connects the RAG system with Gemini.
# This module is responsible for generating final AI answers using retrieved document context.

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_response(query, context):

    prompt = f"""
    You are an AI assistant for a knowledge base retrieval system.

    Answer the question ONLY using the provided context.
    If the answer exists in the context, provide a clear and direct response.
    Do not be overly cautious or mention missing attribution unless necessary.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    try:
        logger.info("Generating response using Gemini")
        response = model.generate_content(prompt)
        logger.info("Successfully generated Gemini response")
        return response.text
    
    except Exception as e:
        raise GeminiException(
            f"Failed to generate AI response: {str(e)}"
        )
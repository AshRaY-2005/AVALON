from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_ai_client():
    """
    Centralized factory to initialize and return the Groq client.
    Uses the GROQ_API_KEY from environment variables.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
        
    return Groq(api_key=api_key)

# Singleton instance for the application
client = get_ai_client()

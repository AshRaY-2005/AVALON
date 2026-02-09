from groq import Groq
import os
import sys

print(f"Python version: {sys.version}")
try:
    client = Groq(api_key="test")
    print("Groq client initialized successfully")
except TypeError as e:
    print(f"Initialization failed with TypeError: {e}")
except Exception as e:
    print(f"Initialization failed with {type(e).__name__}: {e}")

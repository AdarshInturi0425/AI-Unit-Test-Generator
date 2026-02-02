from google import genai
from google.genai import types
import os
import time

class AITestEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found!")
        
        # Configure the client with automatic retries for 503/429 errors
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(
                    attempts=3,           # Try up to 3 times
                    initial_delay=2.0,    # Wait 2 seconds before first retry
                    max_delay=10.0,       # Wait at most 10 seconds
                    http_status_codes=[503, 429] # Retry on 'Overloaded' and 'Rate Limit'
                )
            )
        )
        self.model_id = 'gemini-3-flash-preview'

    def generate_test_code(self, source_code):
        prompt = f"""
        Generate a Python 'unittest' file for this code.
        
        RULES:
        1. Class must inherit from unittest.TestCase.
        2. Methods must start with 'test_'.
        3. Include 'import unittest' and 'from calculator import *'.
        4. Return ONLY the code. No markdown, no backticks.

        CODE:
        {source_code}
        """
        
        try:
            # Explicitly calling the Gemini 3 Flash model
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
            # Cleaning up any markdown if the AI includes it despite instructions
            return response.text.replace("```python", "").replace("```", "").strip()
        except Exception as e:
            # If even the retries fail, provide helpful feedback
            error_str = str(e)
            if "503" in error_str or "overloaded" in error_str.lower():
                return "# 🚧 AI is currently overloaded. Please wait 30 seconds and try again."
            elif "429" in error_str or "quota" in error_str.lower():
                return "# ⏱️ Rate limit reached. Please wait and try again."
            else:
                raise Exception(f"AI Generation failed: {error_str}")

    def heal_code(self, source_code, error_message):
        """Fix buggy code based on test failure messages"""
        prompt = f"""
        The following Python code has a bug that caused a unit test failure.
        
        ERROR MESSAGE:
        {error_message}
        
        ORIGINAL CODE:
        {source_code}
        
        Fix the code so the tests pass. 
        Return ONLY the corrected raw Python code. No explanation, no markdown.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text.replace("```python", "").replace("```", "").strip()
        except Exception as e:
            raise Exception(f"AI Healing failed: {str(e)}")

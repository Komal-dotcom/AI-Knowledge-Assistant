import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class LLMService:

    def __init__(self) -> None:

        genai.configure(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = genai.GenerativeModel(
       "gemini-2.5-flash"
        )

    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
You are a document assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:

"I could not find the answer in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.model.generate_content(
            prompt
        )

        return response.text
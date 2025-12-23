import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_test_suite(user_prompt: str) -> str:
    """
    Agent A (QA Architect): Generates a pytest suite based on a user prompt.
    It focuses on edge cases, boundary values, and happy paths.
    """
    
    system_prompt = """
    You are the QA Architect for a TDD (Test-Driven Development) system.
    Your GOAL is to break the code before it's written.
    
    RULES:
    1. specific output: Return ONLY raw Python code. No markdown formatting (like ```python), no explanations.
    2. Framework: Use 'pytest'.
    3. Coverage: Generate 5-10 test cases covering:
       - Happy Path (Standard inputs)
       - Edge Cases (Empty inputs, nulls, negative numbers, zeros) [cite: 9, 60]
       - Type Errors (if applicable)
    4. Naming: Name the test file `test_generated.py` contextually, but output the code directly.
    5. Do NOT write the implementation code (the function being tested). Assume the function to be tested is imported from `main`.
    
    Example:
    If the user asks for "A function to sum two numbers", your output should look like:
    
    from main import sum_numbers
    import pytest

    def test_sum_positive():
        assert sum_numbers(2, 3) == 5

    def test_sum_negative():
        assert sum_numbers(-1, -1) == -2
        
    def test_sum_zero():
        assert sum_numbers(0, 0) == 0
    """

    user_message = f"User Request: {user_prompt}"

    response = client.chat.completions.create(
        model="gpt-4o",  # Or "gpt-3.5-turbo" for testing cost-effectively
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2 # Low temperature for more deterministic/strict code generation
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    # Quick sanity check
    prompt = "Write a function that reverses a string."
    print(generate_test_suite(prompt))
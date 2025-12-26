import os
from openai import OpenAI

# Connect to local Ollama instance
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama", 
)

def generate_test_suite(user_prompt: str) -> str:
    """
    Agent A (QA Architect): Generates a pytest suite.
    """
    system_prompt = """
    You are the QA Architect for a TDD system.
    GOAL: Break the code before it's written.
    
    RULES:
    1. Output ONLY raw Python code. No markdown (```python), no chatter.
    2. Use 'pytest'.
    3. Generate 5 test cases: Happy Path, Edge Cases (0, negative, null), and Type Errors.
    4. Assume the function to be tested is imported from `main`.
    """

    user_message = f"User Request: {user_prompt}"

    try:
        response = client.chat.completions.create(
            model="qwen2.5-coder:32b", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"# Error generating tests: {str(e)}"
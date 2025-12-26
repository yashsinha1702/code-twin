import os
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

def generate_solution(user_prompt: str, test_code: str, error_log: str = None) -> str:
    """
    Agent B (The Developer): Writes code to satisfy tests.
    """
    system_prompt = """
    You are a Python Developer in a TDD workflow.
    
    RULES:
    1. Output ONLY valid Python code. No markdown, no explanations.
    2. Do NOT write the test code again. Only the implementation.
    3. If error logs are provided, fix the code based on the specific error.
    """

    user_message = f"""
    User Request: {user_prompt}
    
    The Test Suite you need to pass:
    {test_code}
    """

    if error_log:
        user_message += f"\n\nPREVIOUS ATTEMPT FAILED. FIX THIS ERROR:\n{error_log}"

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
        return f"# Error generating solution: {str(e)}"
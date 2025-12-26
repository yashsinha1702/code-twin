import os
from src.agents.qa_agent import generate_test_suite
from src.agents.dev_agent import generate_solution
from src.utils.executor import run_tests

def clean_code(code_str):
    # Removes markdown fences if the model accidentally adds them
    return code_str.replace("```python", "").replace("```", "").strip()

def main():
    print("🚀 Code-Twin: Autonomous TDD Agent (32B Model Loaded)")
    
    user_prompt = input("\nEnter your coding request: ")
    
    print("\n1. 🕵️  QA Architect is designing tests...")
    raw_test_code = generate_test_suite(user_prompt)
    test_code = clean_code(raw_test_code)
    # print(f"DEBUG: Tests Generated:\n{test_code}\n")
    
    print("2. 👨‍💻 Developer is building the first draft...")
    raw_sol_code = generate_solution(user_prompt, test_code)
    solution_code = clean_code(raw_sol_code)
    
    max_retries = 3
    for attempt in range(max_retries):
        print(f"\n3. ⚖️  Running Trial {attempt + 1}...")
        
        result = run_tests(test_code, solution_code)
        
        if result["success"]:
            print(f"\n✅ SUCCESS on attempt {attempt + 1}!")
            print("-" * 40)
            print("FINAL CODE:\n")
            print(solution_code)
            
            # Clean up
            if os.path.exists("main.py"): os.remove("main.py")
            if os.path.exists("test_generated.py"): os.remove("test_generated.py")
            break
        else:
            print(f"❌ Failed. Error snippet:\n{result['output'][:300]}...")
            
            if attempt < max_retries - 1:
                print("🔄 Dev Agent is analyzing the error and refactoring...")
                raw_sol_code = generate_solution(user_prompt, test_code, error_log=result["output"])
                solution_code = clean_code(raw_sol_code)
            else:
                print("\n💀 Maximum retries reached.")

if __name__ == "__main__":
    main()
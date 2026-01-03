import subprocess
import os

def run_tests(test_code: str, solution_code: str) -> dict:
    # 1. Write to temp files
    with open("main.py", "w") as f:
        f.write(solution_code)
        
    with open("test_generated.py", "w") as f:
        f.write(test_code)

    # 2. Run pytest
    try:
        result = subprocess.run(
            ["pytest", "test_generated.py"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout + result.stderr
        }

    except subprocess.TimeoutExpired:
        return {"success": False, "output": "Timeout: Infinite Loop Detected"}
    except Exception as e:
        return {"success": False, "output": str(e)}
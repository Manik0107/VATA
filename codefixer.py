import subprocess
import os
import time
from agno.agent import Agent
from agno.models.google import Gemini
from agno.utils.log import logger
from agno.tools.duckduckgo import DuckDuckGoTools

# =============================================================
# CONFIG
# =============================================================
# Path to your Manim Python file
MANIM_FILE_PATH = "generated_animation_dspy.py"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# =============================================================
# 1. MANIM TEST RUNNER
# =============================================================
class ManimRunner:
    def run(self, file_path):
        """Runs the specified Python file and captures stdout/stderr."""
        try:
            result = subprocess.run(
                ["manim", "-pql", file_path],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode == 0:
                logger.info("✅ Manim script ran successfully.")
                return {"success": True, "logs": result.stdout}
            else:
                logger.error("❌ Error during execution.")
                return {"success": False, "logs": result.stderr}
        except subprocess.TimeoutExpired:
            return {"success": False, "logs": "Execution timed out."}
        except Exception as e:
            return {"success": False, "logs": str(e)}

# =============================================================
# 2. FIX AGENT
# =============================================================
class FixAgent:
    def __init__(self):
        self.agent = Agent(
            name="FixAgent",
            role="Code Debugging Agent",
            model=Gemini(id="gemini-2.5-flash"),
            tools=[DuckDuckGoTools()],
        )

    def fix_code(self, original_code, error_logs, max_retries=3):
        """
        Ask Gemini to fix only the specific lines causing the error.
        Retries automatically if Gemini is overloaded (HTTP 503).
        """
        prompt = f"""
You are a precise Python code fixer.
You are given:
1. A Manim Python file (full code)
2. The error logs from executing it.

Your job:
- Identify the **exact line(s)** causing the error and all the line that will cause the same error.
- Correct **only those lines**, and keep every other part of the code 100% identical.
- Do NOT change structure, imports, or formatting elsewhere.
- Return the **entire corrected Python file** (ready to run).
- Do NOT explain your changes, only output the corrected code.
- Never add code fences like ```python or ```.

Error Logs:
{error_logs}

Original Code:
```
{original_code}
Return ONLY the corrected Python code below:
"""
        for attempt in range(max_retries):
            try:
                result = self.agent.run(prompt)
                return result.content
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    wait_time = (attempt + 1) * 5
                    logger.warning(
                        f"⚠️ Gemini overloaded (503). Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    raise e
        raise RuntimeError("Gemini failed after multiple retries.")

# =============================================================
# 3. COORDINATOR
# =============================================================
class CodeFixCoordinator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.runner = ManimRunner()
        self.fixer = FixAgent()

    def start(self):
        iteration = 1
        while True:
            print(f"\n🧩 Iteration {iteration} ----------------------------")
            # Read current version of the file
            with open(self.file_path, "r") as f:
                code = f.read()

            # Run the file and get logs
            result = self.runner.run(self.file_path)

            if result["success"]:
                print("✅ All errors fixed. File is ready.")
                break

            print("🔧 Fixing detected error...")
            corrected_code = self.fixer.fix_code(code, result["logs"])

            # Overwrite same file with corrected version
            with open(self.file_path, "w") as f:
                f.write(corrected_code)

            print(f"💾 Updated {self.file_path} with corrections.")
            iteration += 1

# =============================================================
# MAIN
# =============================================================
if __name__ == "__main__":
    coordinator = CodeFixCoordinator(MANIM_FILE_PATH)
    coordinator.start()

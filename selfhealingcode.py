import io
import os
import traceback
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from manim import config, tempconfig

load_dotenv()

import subprocess

def run_code_and_get_logs(code_file: str):
    """Run code as a subprocess to capture full runtime errors including Manim."""
    try:
        result = subprocess.run(
            ["python", code_file],
            capture_output=True,
            text=True,
            check=False  # Don't raise exception; we capture it manually
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "errors": result.stderr  # Manim errors show up in stderr
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "errors": str(e)
        }

def clean_code(raw_code: str) -> str:
    """Remove unwanted ``` fences if LLM adds them"""
    return (
        raw_code.replace("```python", "")
        .replace("```", "")
        .strip()
    )

# ✅ Gemini 2.5 Flash with LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=os.getenv("GEMINI_API_KEY"),
)

# Correction Prompt tailored for Manim
correction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior Manim + Python developer.
Your task: fix Manim animation code when it fails.

Rules:
- Always return the FULL corrected Manim code.
- Keep the original logic and animations.
- Ensure the corrected code runs without errors.
- If mobjects are empty, guard against FadeOut/FadeIn errors by checking `if self.mobjects:`.
- ❌ Do NOT include ```python or ``` fences.
- ❌ Do NOT include explanations or extra text. Only the code.

Here is the code and the runtime logs:"""),
    ("user", "Code:\n\n{code}\n\nLogs:\n{logs}")
])

correction_chain = correction_prompt | llm

CODE_FILE = "generated_manim_code.py"

def load_code():
    return Path(CODE_FILE).read_text()

def save_code(new_code: str):
    Path(CODE_FILE).write_text(new_code)

MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    code = load_code()
    logs = run_code_and_get_logs(code)

    if not logs["errors"]:  # ✅ Success
        print("✅ Code executed successfully with Manim render!")
        print("OUTPUT:\n", logs["stdout"])
        break

    print(f"❌ Errors found (attempt {attempt+1}):\n{logs['errors']}")

    # Ask Gemini to fix the code
    corrected = correction_chain.invoke({"code": code, "logs": logs})
    new_code = clean_code(corrected.content)  # ✅ clean out fences

    save_code(new_code)

else:
    print("⚠️ Code still failing after max retries.")
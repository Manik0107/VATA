import os
import sys
import subprocess
from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai import types

# Import our agents
from agno_agents import get_animator_agent, get_coder_agent

# Load environment variables
load_dotenv()


def extract_text_from_pdf(pdf_path: str) -> str:
    """Uses Agno agent with OpenRouter to extract full text from a PDF."""
    from agno_agents import get_pdf_extractor_agent
    import base64
    
    print(f"Reading PDF: {pdf_path}")
    
    try:
        # Read PDF as bytes
        pdf_bytes = Path(pdf_path).read_bytes()
        
        # Create PDF extractor agent (uses OpenRouter)
        extractor = get_pdf_extractor_agent()
        
        # Encode PDF to base64 for the agent
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # Create a message with the PDF content
        # Note: OpenRouter's Gemini supports multimodal input
        prompt = f"""Extract all text content from this PDF document.

PDF Content (base64):
{pdf_base64[:1000]}...

Please extract and return all the text content from this PDF, preserving logical structure."""
        
        response = extractor.run(prompt)
        
        return response.content
        
    except Exception as e:
        print(f"Failed to read PDF with Agno agent: {e}")
        print(f"Make sure your OPENROUTER_API_KEY has sufficient credits.")
        print(f"Visit https://openrouter.ai/settings/credits to add credits")
        sys.exit(1)



def validate_manim_code(code_file: str) -> tuple[bool, str]:
    """
    Validate generated Manim code by running dry_run with smart error filtering.
    
    Returns:
        (success: bool, error_message: str)
    """
    if not Path(code_file).exists():
        return False, f"File not found: {code_file}"
    
    try:
        print(f"Validating {code_file} with manim --dry_run...")
        result = subprocess.run(
            ["uv", "run", "manim", code_file, "GenScene", "--dry_run"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("Code validation passed!")
            return True, ""
        else:
            # Smart error filtering (inspired by selfhealingcode.py)
            stderr_text = result.stderr
            error_lines = []
            
            # Split into lines and filter out known warnings
            for line in stderr_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # Skip common warnings that aren't actual errors
                if any(warning in line for warning in [
                    "UserWarning: pkg_resources is deprecated",
                    "WARNING: All log messages before absl::InitializeLog()",
                    "ALTS creds ignored",
                    "import pkg_resources",
                    "manim_voiceover/__init__.py",
                    "INFO     Caching disabled",
                    "INFO     Animation",
                    "INFO     Automatically converted",
                    "Both GOOGLE_API_KEY and GEMINI_API_KEY are set"
                ]):
                    continue
                    
                # Only include lines that look like actual errors
                if any(error_indicator in line for error_indicator in [
                    "Error", "Exception", "Traceback", "File \"", 
                    "NameError", "TypeError", "ValueError", "ImportError",
                    "AttributeError", "SyntaxError", "IndentationError",
                    "KeyError", "IndexError", "RuntimeError"
                ]):
                    error_lines.append(line)
            
            errors = '\n'.join(error_lines)
            
            if not errors.strip():
                # If no errors found after filtering but return code != 0
                errors = stderr_text[-500:]  # Last 500 chars as fallback
            
            print(f"Validation failed with error:\n{errors[:500]}")
            return False, errors
            
    except subprocess.TimeoutExpired:
        return False, "Validation timed out after 60 seconds"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def main():
    # 1. Configuration
    input_pdf = "pdfs/linear_regression_notes.pdf" # Default for testing
    topic_prompt = "Explain Linear Regression deeply using the Pizza Price analogy."
    
    # Allow overriding via args (simple version)
    if len(sys.argv) > 1:
        topic_prompt = sys.argv[1]

    # Validate file
    if not Path(input_pdf).exists():
        print(f"Input file not found: {input_pdf}")
        return

    print("\n--- Phase 1: content Extraction ---")
    pdf_text = extract_text_from_pdf(input_pdf)
    print(f"Extracted {len(pdf_text)} characters.")

    print("\n--- Phase 2: Creative Direction (Animator Agent) ---")
    animator = get_animator_agent()
    
    animator_input = f"""
    SOURCE MATERIAL:
    {pdf_text[:30000]} # Limit context window if needed, though 2.5 flash is huge

    USER REQUEST:
    {topic_prompt}

    Create a storyboard that explains this perfectly to a beginner.
    """
    
    print("Animator is thinking...")
    storyboard_response = animator.run(animator_input)
    
    response_text = storyboard_response.content
    print(f"Raw response length: {len(response_text)} characters")
    
    try:
        from agno_agents import parse_storyboard
        storyboard = parse_storyboard(response_text)
    except Exception as e:
        print(f"Failed to parse storyboard JSON: {e}")
        print(f"Raw response: {response_text[:500]}...")
        sys.exit(1)
    
    print(f"Storyboard created: {len(storyboard.scenes)} scenes.")
    for i, scene in enumerate(storyboard.scenes):
        print(f"   {i+1}. {scene.title} ({scene.duration_seconds}s)")

    print("\n--- Phase 3: Production (Coder Agent) ---")
    coder = get_coder_agent()
    
    # Prepare initial input
    coder_input = f"""
    TOPIC: {storyboard.topic}
    SCENES_JSON:
    {storyboard.model_dump_json(indent=2)}

    Generate the Manim code for this sequence.
    """

    max_retries = 5
    output_filename = "generated_agno_manim.py"
    
    for attempt in range(max_retries):
        print(f"Coder is coding (attempt {attempt + 1}/{max_retries})...")
        code_response = coder.run(coder_input)
        
        response_text = code_response.content
        print(f"Raw coder response length: {len(response_text)} characters")
        
        try:
            from agno_agents import parse_manim_code
            manim_code_obj = parse_manim_code(response_text)
        except Exception as e:
            print(f"Failed to parse Manim code JSON: {e}")
            print(f"Raw response: {response_text[:500]}...")
            
            if attempt < max_retries - 1:
                print(f"Retrying with error feedback...")
                coder_input = f"""
                Your previous response had a JSON parsing error: {e}
                
                Please fix and regenerate ONLY valid JSON with this structure:
                {{
                  "filename": "...",
                  "code": "...",
                  "explanation": "..."
                }}
                
                Original request:
                {coder_input}
                """
                continue
            else:
                sys.exit(1)
        
        print(f"\nSaving generated code to {output_filename}...")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(manim_code_obj.code)
        
        # Validate with dry_run
        is_valid, error_msg = validate_manim_code(output_filename)
        
        if is_valid:
            print(f"Code generated successfully and passed validation!")
            print(f"Explanation: {manim_code_obj.explanation}")
            break
        else:
            print(f"Code has errors. Attempt {attempt + 1}/{max_retries}")
            
            if attempt < max_retries - 1:
                print(f"Sending error feedback to Coder Agent...")
                coder_input = f"""
                Your previous code had errors when tested with manim --dry_run.
                
                Here is the EXACT CODE you generated that failed:
                ```python
                {manim_code_obj.code}
                ```
                
                ERROR MESSAGE:
                {error_msg[:1000]}
                
                TASK: Fix ONLY the specific errors shown above.
                - Do NOT regenerate from scratch
                - Keep the working parts
                - Fix the specific line/method causing the error
                - Remember Manim v0.19+ API rules from your instructions
                
                Original storyboard context:
                TOPIC: {storyboard.topic}
                SCENES: {len(storyboard.scenes)} scenes
                
                Respond with corrected COMPLETE code as JSON:
                {{
                  "filename": "...",
                  "code": "... FIXED CODE ...",
                  "explanation": "What was wrong and how I fixed it"
                }}
                """
            else:
                print(f"Max retries ({max_retries}) exceeded. Code still has errors.")
                print(f"You may need to manually fix {output_filename}")
                break

if __name__ == "__main__":
    main()

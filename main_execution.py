from dspy_manim_workflow import DSPyManimWorkflow
import os
from dotenv import load_dotenv
import json
import sys
from pathlib import Path
import subprocess

def validate_environment():
    """Validate required environment variables."""
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment.\n"
            "Please set it in your .env file or export it:\n"
            "export GEMINI_API_KEY='your-api-key-here'"
        )
    
    return api_key

def validate_input_file(file_path):
    """Validate that the input document exists."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}\n"
            f"Searched at: {path.absolute()}"
        )
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    if path.suffix.lower() != '.pdf':
        print(f"Warning: Expected PDF file, got {path.suffix}")
    
    return str(path)

def save_report(report_data, output_path="report.json"):
    """Save workflow report with error handling."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        print(f"Report saved to {output_path}")
        return True
    except IOError as e:
        print(f"Warning: Failed to save report: {e}")
        return False

def run_code_fixer(generated_file):
    """Run codefixer.py with error handling."""
    if not Path(generated_file).exists():
        print(f"Warning: Generated file not found: {generated_file}")
        print("Skipping code fixing step.")
        return False
    
    try:
        print("\nRunning codefixer.py for error correction...")
        result = subprocess.run(
            ["uv", "run", "codefixer.py"],
            check=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        print("Code fixing completed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("Warning: Code fixer timed out after 5 minutes")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"Warning: Code fixer failed with exit code {e.returncode}")
        if e.stderr:
            print(f"Error output: {e.stderr[:500]}")
        return False
        
    except FileNotFoundError:
        print("Warning: 'uv' command not found. Please install uv or run codefixer.py manually:")
        print("python codefixer.py")
        return False

def main():
    """Main execution workflow with comprehensive error handling."""
    try:
        print("Validating environment...")
        api_key = validate_environment()
        print("API key found")
        
        document_path = "pdfs/linear_regression_notes.pdf"
        topic = "explain everything about linear regression so i can know everything about it"
        class_name = "LinearRegression"
        
        print(f"\nValidating input document: {document_path}")
        document_path = validate_input_file(document_path)
        print(f"Document found: {document_path}")
        
        print("\nInitializing DSPy Manim workflow...")
        try:
            workflow = DSPyManimWorkflow(api_key)
            print("Workflow initialized")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize workflow: {e}")
        
        print(f"\nExecuting workflow for topic: '{topic[:60]}...'")
        try:
            results = workflow(
                document_path=document_path,
                topic=topic,
                class_name=class_name,
                enhanced_narration=True,
                detailed_storyboard=True
            )
            print("Workflow execution completed")
        except Exception as e:
            raise RuntimeError(f"Workflow execution failed: {e}")
        
        if not results:
            raise ValueError("Workflow returned empty results")
        
        output_file = "generated_animation_dspy.py"
        print(f"\nSaving generated code to {output_file}...")
        try:
            workflow.save_code(results, output_file)
            print(f"Code saved to {output_file}")
        except Exception as e:
            print(f"Warning: Failed to save code: {e}")
        
        print("\nGenerating workflow report...")
        report_data = {
            "inputs": {
                "document_path": document_path,
                "topic": topic,
                "class_name": class_name
            },
            "outputs": {
                "extracted_content": results.get("extracted_content"),
                "teaching_plan": results.get("teaching_plan"),
                "storyboard": results.get("storyboard"),
                "enhanced_narration": results.get("enhanced_narration"),
                "detailed_storyboard": results.get("detailed_storyboard"),
                "generated_code": results.get("generated_code")
            }
        }
        save_report(report_data)
        
        run_code_fixer(output_file)
        
        print("\nPipeline completed successfully!\n")
        return results
        
    except ValueError as e:
        print(f"\nConfiguration Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except FileNotFoundError as e:
        print(f"\nFile Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except RuntimeError as e:
        print(f"\nRuntime Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user", file=sys.stderr)
        sys.exit(130)
        
    except Exception as e:
        print(f"\nUnexpected Error: {type(e).__name__}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    results = main()
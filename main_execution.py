# main_execution.py
from dspy_manim_workflow import DSPyManipWorkflow
import os
from dotenv import load_dotenv
import json

def main():
    # Load environment
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Initialize workflow
    workflow = DSPyManipWorkflow(api_key)
    
    # INPUTS
    document_path = "pdfs/Microsoft PowerPoint - Lecture14-Development of surfaces-pkghosh [Compatibility Mode].pdf"  # Your document
    topic = "explain the formation of the truncated right cylinder"               # Specific topic
    class_name = "Formation"            # Optional class name

    # Execute workflow
    results = workflow(
        document_path=document_path,
        topic=topic,
        class_name=class_name,
        enhanced_narration=True,  # New parameter
        detailed_storyboard=True  # New parameter
    )
    
    # Save generated code
    output_file = "generated_animation_dspy.py"
    workflow.save_code(results, output_file)
    
    report_data = {
        "inputs": {
            "document_path": document_path,
            "topic": topic,
            "class_name": class_name
        },
        "outputs": {
        "extracted_content": results.get("extracted_content"),
        "teaching_plan": results.get("teaching_plan"),   # Save teaching plan (animation plan)
        "storyboard": results.get("storyboard"),         # Save animation storyboard
        "enhanced_narration": results.get("enhanced_narration"),
        "detailed_storyboard": results.get("detailed_storyboard"),
        "generated_code": results.get("generated_code")
        }
    }
    
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)
    
    print("Report saved to report.json")
    
    return results

if __name__ == "__main__":
    results = main()

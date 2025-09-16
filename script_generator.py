import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# --- Configuration Paths ---
JSON_METADATA_PATH = "output/linear_regression_notes.json"
MARKDOWN_PATH = "output/linear_regression_notes.md"
PROMPT_FILE_PATH = "prompts/prompt1.txt"
OUTPUT_SCRIPT_PATH = "output/generated_narrative_script.txt"

# --- Helper Functions ---
def load_text(path):
    """Loads text content from a specified file path."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_and_process_metadata(path):
    """
    Loads JSON metadata and enhances it with an image summary for the LLM.
    Handles file not found or invalid JSON gracefully.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        if "images" in metadata and isinstance(metadata["images"], list):
            image_summary_lines = []
            image_summary_lines.append(f"Document contains {len(metadata['images'])} image(s) and diagram(s):\n")
            for img in metadata["images"]:
                img_name = img.get("image_name", "UNKNOWN_NAME")
                context_type = img.get("context_type", "general")
                keywords = ", ".join(img.get("keywords", []))
                description = img.get("description", "No description provided.")
                image_summary_lines.append(f"- {img_name} ({context_type}): Keywords: [{keywords}], Description: '{description}'")
            metadata["image_summary_for_llm"] = "\n".join(image_summary_lines)
        else:
            metadata["image_summary_for_llm"] = "No image or diagram metadata available."

        return json.dumps(metadata, indent=2)
    except FileNotFoundError:
        print(f"Warning: Metadata file not found at {path}. Proceeding with empty metadata.")
        return json.dumps({"image_summary_for_llm": "No metadata file found."})
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in metadata file at {path}. Proceeding with empty metadata.")
        return json.dumps({"image_summary_for_llm": "Invalid JSON in metadata file."})
    except Exception as e:
        print(f"Warning: An unexpected error occurred loading metadata from {path}. Error: {e}. Proceeding with empty metadata.")
        return json.dumps({"image_summary_for_llm": f"Error processing metadata: {e}"})


def escape_braces(text):
    """
    Escapes curly braces in the text to prevent Python's .format() from misinterpreting them,
    while preserving actual placeholders for later formatting.
    """
    placeholders = ["query", "document_content", "metadata"] # Only actual placeholders
    pattern = re.compile(r"\{([a-zA-Z0-9_]+)\}")
    token_map = {}

    def replace_placeholder(m):
        key = m.group(1)
        if key in placeholders:
            token = f"@@PLACEHOLDER_{key.upper()}@@" # Create a unique token
            token_map[token] = m.group(0) # Store original placeholder
            return token
        return m.group(0) # Not a placeholder, return as is

    # First, replace actual placeholders with tokens
    text_with_tokens = pattern.sub(replace_placeholder, text)
    # Then, escape all remaining curly braces
    text_escaped = text_with_tokens.replace("{", "{{").replace("}", "}}")

    # Finally, restore the original placeholders from tokens
    for token, original_placeholder in token_map.items():
        text_escaped = text_escaped.replace(token, original_placeholder)

    return text_escaped


def main():
    # Initialize the Gen AI client
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Load inputs
    enhanced_metadata = load_and_process_metadata(JSON_METADATA_PATH)
    markdown_content = load_text(MARKDOWN_PATH)
    prompt_template = load_text(PROMPT_FILE_PATH)

    user_query = input("Enter the lesson topic/focus for the animation script: ").strip()
    if not user_query:
        print("Error: User query cannot be empty.")
        return

    # Prepare the prompt
    prompt_template_escaped = escape_braces(prompt_template)
    full_prompt = prompt_template_escaped.format(
        query=user_query,
        document_content=markdown_content,
        metadata=enhanced_metadata,
    )

    print("\n--- Generating Narrative Script ---")
    print(f"Query: {user_query}")
    print(f"Lesson Content: {len(markdown_content)} characters")
    print(f"Metadata: {len(enhanced_metadata)} characters")
    print("Sending request to LLM...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[{"role": "user", "parts": [{"text": full_prompt}]}],
            config=types.GenerateContentConfig(
                temperature=0.9,  # Moderate creativity
                max_output_tokens=8192,  # Sufficient for a 15-20 min script (approx 2000-2500 words)
                top_k=40,
                top_p=0.9,
            ),
        )

        generated_script = None
        # A safer way to access the generated text
        try:
            generated_script = response.text
        except ValueError:
            # If the model blocks the response for safety reasons, `response.text` will raise an error.
            print("❌ Script generation failed. The response may have been blocked.")
            print(f"Prompt Feedback: {response.prompt_feedback}")
            return

        if not generated_script:
            print("❌ No script generated by Gemini, or response was empty.")
            if hasattr(response, "prompt_feedback") and response.prompt_feedback:
                print(f"Prompt Feedback: {response.prompt_feedback}")
            return

        # Save the generated script
        with open(OUTPUT_SCRIPT_PATH, "w", encoding="utf-8") as f:
            f.write(generated_script)

        print(f"\n✅ Narrative script successfully generated and saved to {OUTPUT_SCRIPT_PATH}")
        print("\n--- Generated Script Preview ---")
        print(generated_script[:1000] + ("..." if len(generated_script) > 1000 else ""))  # Print first 1000 chars

    except Exception as e:
        print(f"❌ An error occurred during script generation: {e}")

if __name__ == "__main__":
    main()
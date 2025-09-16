# render_manim.py
import os
import subprocess
import sys
import re # Added for parsing Manim output more robustly

# --- Configuration ---
# Name of the generated Manim file.
GENERATED_MANIM_FILE = "generated_manim_code.py" 
# The main class name in your generated Manim code. Make sure this matches!
SCENE_NAME = "GeneratedEducationalScene" 
# Folder where the final video outputs will be stored.
OUTPUT_FOLDER = "output_videos"
# Path to your images folder, relative to where `manim` command is run.
# This is crucial for ImageMobject to find images.
IMAGES_FOLDER_PATH = "output/linear_regression_notes_images" 

# --- TTS Service Configuration (for Manim Voiceover) ---
# Uncomment and install the desired service if gTTS causes issues or for higher quality.
# For CoquiService: `pip install TTS manim-voiceover[coqui]`
# For AzureService: `pip install azure-cognitiveservices-speech manim-voiceover[azure]` (requires Azure API key)
# For OpenAI TTS: `pip install openai manim-voiceover[openai]` (requires OpenAI API key)
# from manim_voiceover.services.coqui import CoquiService
# from manim_voiceover.services.azure import AzureService
# from manim_voiceover.services.openai import OpenAIService

# --- Helper to find the generated video path ---
def get_output_video_path_from_stdout(stdout_output):
    """
    Parses Manim's stdout to find the exact path of the generated video.
    """
    # Look for lines like "File ready at: media/videos/..."
    match = re.search(r"File ready at: (.+\.mp4)", stdout_output)
    if match:
        return match.group(1)
    
    # Fallback if specific pattern not found (e.g., Manim version change)
    # Assumes default Manim output structure
    expected_path = os.path.join(
        OUTPUT_FOLDER, 
        "videos", 
        GENERATED_MANIM_FILE.replace(".py", ""), 
        SCENE_NAME + ".mp4"
    )
    if os.path.exists(expected_path):
        return expected_path
    
    return None

def render_manim_video():
    """
    Renders the Manim animation with voiceover, handling image paths and errors.
    """
    if not os.path.exists(GENERATED_MANIM_FILE):
        print(f"Error: Manim file '{GENERATED_MANIM_FILE}' not found. Please generate it first.")
        sys.exit(1)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Set environment variable for Manim to find the images folder
    # This is crucial if ImageMobject expects a relative path or if Manim needs a global hint.
    # Manim Voiceover also uses a specific folder for audio caching within media_dir
    os.environ['MANIM_VOICEOVER_ASSETS_DIR'] = os.path.join(OUTPUT_FOLDER, "voiceover_assets")
    os.makedirs(os.environ['MANIM_VOICEOVER_ASSETS_DIR'], exist_ok=True)


    print(f"Rendering Manim scene '{SCENE_NAME}' from '{GENERATED_MANIM_FILE}'...")
    print(f"Output videos will be saved to: {OUTPUT_FOLDER}")
    print(f"Voiceover assets will be cached in: {os.environ['MANIM_VOICEOVER_ASSETS_DIR']}")
    
    # Manim command to render the scene
    # -pql for preview, low quality (fast drafts). Change to -pqm for medium, -pqh for high, -p for play
    # --media_dir specifies where the overall output (videos, images, text) will go
    # --custom_folders ensures media_dir is respected and not overridden by internal Manim defaults
    command = [
        "manim",
        GENERATED_MANIM_FILE,
        SCENE_NAME,
        "-pql", # Preview, low quality for quick iteration. Can be changed for final render.
        "--media_dir", OUTPUT_FOLDER,
        "--custom_folders",
        # Uncomment if you want to force re-generation of voiceover audio every time
        # This is useful for debugging TTS issues or changing voice parameters.
        # "--force_voiceover_generation" 
    ]

    try:
        # Execute the manim command
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print("Manim rendering successful!")
        print("--- Manim STDOUT ---")
        print(result.stdout)
        print("--- End STDOUT ---")

        if result.stderr:
            print("--- Manim STDERR (Warnings/Errors) ---")
            print(result.stderr)
            print("--- End STDERR ---")

        video_path = get_output_video_path_from_stdout(result.stdout)

        if video_path and os.path.exists(video_path):
            print(f"✨ Final video available at: {video_path}")
        else:
            print(f"⚠️ Could not reliably determine output video path. Check '{OUTPUT_FOLDER}' for your video.")
            print("Expected path might be:", os.path.join(
                OUTPUT_FOLDER, 
                "videos", 
                GENERATED_MANIM_FILE.replace(".py", ""), 
                SCENE_NAME + ".mp4"
            ))

        # Clean up voiceover cache if desired (optional)
        # import shutil
        # voiceover_cache_dir = os.environ['MANIM_VOICEOVER_ASSETS_DIR']
        # if os.path.exists(voiceover_cache_dir):
        #     print(f"Cleaning up voiceover cache: {voiceover_cache_dir}")
        #     shutil.rmtree(voiceover_cache_dir)

    except subprocess.CalledProcessError as e:
        print(f"❌ Error during Manim rendering. Command failed with exit code {e.returncode}.")
        print("--- Manim STDOUT ---")
        print(e.stdout)
        print("--- End STDOUT ---")
        if e.stderr:
            print("--- Manim STDERR ---")
            print(e.stderr)
            print("--- End STDERR ---")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: 'manim' command not found. Please ensure Manim Community is installed")
        print("   and its executable is in your system's PATH. You can install it via pip:")
        print("   `pip install manim`")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    render_manim_video()
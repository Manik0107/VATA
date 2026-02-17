# render_manim.py
import os
import subprocess
import sys
import re

GENERATED_MANIM_FILE = "generated_manim_code.py" 
SCENE_NAME = "GeneratedEducationalScene" 
OUTPUT_FOLDER = "output_videos"
IMAGES_FOLDER_PATH = "output/linear_regression_notes_images" 


def get_output_video_path_from_stdout(stdout_output):
    """
    Parses Manim's stdout to find the exact path of the generated video.
    """
    match = re.search(r"File ready at: (.+\.mp4)", stdout_output)
    if match:
        return match.group(1)
    
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
    
    os.environ['MANIM_VOICEOVER_ASSETS_DIR'] = os.path.join(OUTPUT_FOLDER, "voiceover_assets")
    os.makedirs(os.environ['MANIM_VOICEOVER_ASSETS_DIR'], exist_ok=True)


    print(f"Rendering Manim scene '{SCENE_NAME}' from '{GENERATED_MANIM_FILE}'...")
    print(f"Output videos will be saved to: {OUTPUT_FOLDER}")
    print(f"Voiceover assets will be cached in: {os.environ['MANIM_VOICEOVER_ASSETS_DIR']}")
    
    command = [
        "manim",
        GENERATED_MANIM_FILE,
        SCENE_NAME,
        "-pql",
        "--media_dir", OUTPUT_FOLDER,
        "--custom_folders",
    ]

    try:
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
            print(f"Final video available at: {video_path}")
        else:
            print(f"Could not reliably determine output video path. Check '{OUTPUT_FOLDER}' for your video.")
            print("Expected path might be:", os.path.join(
                OUTPUT_FOLDER, 
                "videos", 
                GENERATED_MANIM_FILE.replace(".py", ""), 
                SCENE_NAME + ".mp4"
            ))

    except subprocess.CalledProcessError as e:
        print(f"Error during Manim rendering. Command failed with exit code {e.returncode}.")
        print("--- Manim STDOUT ---")
        print(e.stdout)
        print("--- End STDOUT ---")
        if e.stderr:
            print("--- Manim STDERR ---")
            print(e.stderr)
            print("--- End STDERR ---")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'manim' command not found. Please ensure Manim Community is installed")
        print("and its executable is in your system's PATH. You can install it via pip:")
        print("`pip install manim`")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    render_manim_video()
#!/usr/bin/env python3
"""
Manim Code Generator with Latest Google GenAI SDK
Compatible with Manim 0.19.0 and Google GenAI 1.19.0 (2025)
"""

import os
import re
import json
from typing import List, Dict, Optional

# NEW: Updated imports for Google GenAI SDK (replaces google-generativeai)
from google import genai
from google.genai import types

from narrative_parser import AdvancedNarrativeParser, AnimationSection


class ManimCodeGenerator:
    """
    Advanced Manim code generator using latest Google GenAI SDK
    """

    def __init__(self, api_key: str):
        # NEW: Updated client initialization for Google GenAI SDK
        self.client = genai.Client(api_key=api_key)
        self.parser = AdvancedNarrativeParser()

        # Template for the latest Manim 0.19.0 syntax
        self.base_template = '''from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np
import os
from pathlib import Path

class NarrativeEducationalAnimation(VoiceoverScene):
    def construct(self):
        # Initialize TTS service (compatible with Manim Voiceover 0.3.7)
        self.set_speech_service(GTTSService())
        
        # Execute narrative sections in sequence
{method_calls}
        
        self.wait(2)
{section_methods}
    
    def load_image_safe(self, image_path, scale=0.5, position=RIGHT*3):
        \"\"\"Safely load images with fallback for missing files\"\"\"
        try:
            # Handle both absolute and relative paths
            if not os.path.isabs(image_path):
                image_path = os.path.join(os.getcwd(), image_path)
            
            img = ImageMobject(image_path)
            img.scale(scale)
            img.move_to(position)
            return img
        except Exception as e:
            print(f\"Warning: Could not load image {{image_path}}. Error: {{e}}\")
            # Fallback placeholder
            placeholder = Rectangle(width=2, height=1.5, color=GREY_B)
            placeholder.move_to(position)
            text = Text(\"Image\\nUnavailable\", font_size=20, color=WHITE)
            text.move_to(position)
            return Group(placeholder, text)
    
    def create_title_animation(self, title_text, subtitle_text=\"\"):
        \"\"\"Create engaging title sequence\"\"\"
        title = Text(title_text, font_size=72, color=BLUE, weight=BOLD)
        title.move_to(UP * 0.5)
        
        if subtitle_text:
            subtitle = Text(subtitle_text, font_size=36, color=GREY_A)
            subtitle.move_to(DOWN * 0.5)
            title_group = VGroup(title, subtitle)
        else:
            title_group = VGroup(title)
        
        return title_group
    
    def create_equation_animation(self, equation_tex, build_step_by_step=True):
        \"\"\"Create mathematical equation animations\"\"\"
        equation = MathTex(equation_tex, font_size=48, color=WHITE)
        equation.move_to(ORIGIN)
        
        if build_step_by_step and len(equation) > 1:
            # Build equation part by part
            return [equation[i] for i in range(len(equation))]
        else:
            return [equation]
'''

    def generate_manim_code(self, narrative_script: str, images_folder: str = "",
                          metadata: Optional[Dict] = None) -> str:
        """
        Generate complete Manim code from narrative script
        """
        print("🚀 Starting Manim code generation with advanced parser...")
        
        # Parse narrative script
        parsed_data = self.parser.parse_narrative_script(narrative_script)
        sections = parsed_data['sections']
        
        print(f"📊 Processing {len(sections)} sections...")
        
        # Get available images
        available_images = self._get_available_images(images_folder)
        
        # Create optimized prompt for latest APIs
        prompt = self._create_advanced_prompt(sections, available_images, metadata)
        
        print("🤖 Generating code with Gemini 2.0...")
        
        generated_code = ""
        try:
            # Robust call to generate_content
            # Using contents as a list of dictionaries as per Google GenAI SDK 1.19.0 examples
            response = self.client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            config=types.GenerateContentConfig( # Use generation_config
                    temperature=0.1,  # Lower for more consistent code
                    max_output_tokens=8192,
                    top_k=40,
                    top_p=0.9,
                ),
            )
            
            if response.candidates:
                generated_code = response.candidates[0].content.parts[0].text
                print("✅ Successfully generated Manim code")
            else:
                print("⚠️ Gemini 2.0 returned no candidates. Falling back to template.")
                generated_code = self._generate_fallback_code(sections, available_images)
            
        except Exception as e:
            print(f"❌ Error generating code with Gemini 2.0: {e}")
            # Fallback to template-based generation
            generated_code = self._generate_fallback_code(sections, available_images)
            print("🔄 Used fallback code generation")
        
        # Extract and clean the code
        final_code = self._extract_clean_code(generated_code)
        
        # Validate and fix common issues
        final_code = self._validate_and_fix_code(final_code)
        
        return final_code

    def _create_advanced_prompt(self, sections: List[AnimationSection], available_images: List[str], metadata: Optional[Dict] = None) -> str:
        """Create advanced prompt for latest Manim and AI capabilities"""
        prompt = f"""# MANIM 0.19.0 EDUCATIONAL ANIMATION GENERATOR

# CRITICAL API SAFETY INSTRUCTION
# Never use attributes or methods that do not exist in the official Manim documentation or API.
# For example, do NOT use 'line.point_from_function' or similar non-existent attributes on Manim objects.
# Always use documented and supported Manim methods and properties, such as 'axes.c2p(x, y)', 'get_center()', 'get_start()', 'get_end()', etc.
# If you need a point on a line generated by a function, always calculate it using the function and axes, e.g. axes.c2p(x, f(x)).
# If unsure, refer to the official Manim documentation for the correct usage.
#
# CRITICAL INDEX SAFETY INSTRUCTION
# Never access an index of a MathTex, VGroup, or any list-like object unless you have checked its length and the index is valid.
# For example, before using equation[0][6], always check that equation[0] has at least 7 elements.
# If unsure, use len() to verify the size before accessing, and handle cases where the index may be out of range gracefully.

## MISSION
Generate complete, executable Python code using Manim 0.19.0 and Manim Voiceover 0.3.7 that creates a professional educational video from the parsed narrative structure.

## CRITICAL REQUIREMENTS - LATEST 2025 SYNTAX

### 1. Base Structure (MANDATORY)
```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np
import os
from pathlib import Path

class NarrativeEducationalAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        # Call section methods here
        # Example: self.introduction_section()
        self.wait(2)

    # Helper methods like load_image_safe, create_title_animation, create_equation_animation go here
```

### 2. Manim 0.19.0 API Updates (CRITICAL)
- Use `Text(...)` for text, specifying `font_size`, `color`, `weight`.
- Use `MathTex(r"...")` for mathematical content.
- Use `ImageMobject(path).scale(factor).move_to(position)` for images.
- Use `self.play(Create(obj), run_time=duration)` for animations.
- Use `Group(...)` for grouping objects.
- Colors: `BLUE`, `RED`, `GREEN`, `WHITE`, `GREY_A`, `GREY_B`, etc.

### 3. Perfect Voiceover Synchronization

```python
with self.voiceover(text="Narration text here") as tracker:
    animation = Create(circle)
    self.play(animation, run_time=tracker.duration)
# Crucially, if there's no animation or the animation is shorter than the voiceover,
# ensure a self.wait(tracker.duration - animation_run_time) to sync.
# Or, if animation is just a part of the voiceover, play it and let voiceover naturally progress.
```
Always synchronize animations to `tracker.duration`. If an animation completes before the voiceover, use `self.wait()` to fill the remaining time.

### 4. Section Implementation
Each narrative section MUST be implemented as a separate method within the `NarrativeEducationalAnimation` class. These methods should be called sequentially in the `construct` method.
"""

        # Add section-specific instructions
        for i, section in enumerate(sections, 1):
            prompt += f"""
**Section {i}: {section.title}**
- Method Name: `{section.method_name}`
- Estimated Duration: ~{section.estimated_duration:.1f} seconds
- Voiceover segments: {len(section.segments)}
- Images to consider: {', '.join([os.path.basename(img) for img in section.images]) if section.images else 'None'}
- Animation cues: {', '.join(section.animation_cues) if section.animation_cues else 'None'}
- Mathematical content: {', '.join(section.mathematical_content) if section.mathematical_content else 'None'}

Voiceover text for this section (first 3 segments as example):
"""
            for seg in section.segments[:3]:  # Show first 3 segments as example
                prompt += f'- "{seg.text}"\n'
            
            if len(section.segments) > 3:
                prompt += f"... and {len(section.segments) - 3} more segments\n"

        prompt += f"""

### 5. Image Integration
Available images (full paths): {', '.join(available_images) if available_images else 'None'}

**MANDATORY HELPER METHOD TO INCLUDE AND USE:**
```python
    def load_image_safe(self, image_path, scale=0.5, position=RIGHT*3):
        \"\"\"Safely load images with fallback for missing files\"\"\"
        try:
            if not os.path.isabs(image_path):
                # Ensure the path is absolute or relative to the script's execution directory
                # Manim typically runs from the project root where images might be stored.
                # Use Path to handle cross-OS paths more robustly.
                image_path = Path(os.getcwd()) / image_path
            
            img = ImageMobject(str(image_path)) # ImageMobject expects a string path
            img.scale(scale)
            img.move_to(position)
            return img
        except Exception as e:
            print(f\"Warning: Could not load image {{image_path}}. Error: {{e}}\")
            placeholder = Rectangle(width=2, height=1.5, color=GREY_B)
            placeholder.move_to(position)
            text = Text(\"Image\\nUnavailable\", font_size=20, color=WHITE)
            text.move_to(position)
            return Group(placeholder, text)
```

### 6. Educational Animation Patterns

**For Introduction Sections:**
- Create engaging title with `Text(..., font_size=72, color=BLUE)`
- Add subtitle if needed using `Text(..., font_size=36, color=GREY_A)`
- Use smooth `Write()` or `FadeIn()` animations.

**For Concept Sections:**
- Build content progressively using `Succession()` or `LaggedStart()`.
- Use `MathTex()` for equations, revealing parts sequentially.
- Introduce terms with `Text()` and `Create()`.

**For Mathematical Content:**
- Use `MathTex(r"Y = a + bx")` syntax for equations.
- Build equations piece by piece (`self.play(Write(eq[0]))`, `self.play(Transform(eq[0], eq[1]))`).
- Add visual annotations like `Arrow` or `SurroundingRectangle`.

**For Examples:**
- Create interactive demonstrations using `Animate()`.
- Use `Indicate()` or `Flash()` for emphasis.
- Show before/after comparisons with `Transform()`.

### 7. MANDATORY OUTPUT FORMAT
Generate ONLY the complete Python code. No explanations, no markdown blocks, just clean executable code that:
- Implements ALL sections as methods.
- Uses perfect voiceover synchronization for *every* voiceover block.
- Integrates available images safely using `load_image_safe`.
- Follows Manim 0.19.0 syntax exactly.
- Creates engaging educational animations.
- The main class name MUST be `NarrativeEducationalAnimation`.

### 8. Overlap and Clarity Best Practices
- For every new section or title in the same place as the previous object or animation, ALWAYS fade out or remove previous objects using self.play(FadeOut(*self.mobjects)).
- Explicitly position titles, subtitles, and key visuals with .to_edge, .move_to, .next_to to avoid overlap.
- Never stack multiple Write(Text(...)) animations for section headers at the same position.
- Always ensure only one main title is visible at a time.

The code must be immediately executable with: `manim your_file.py -pql --disable_caching`
```python
# Start your Python code here. DO NOT include ```python or ```
# Make sure to include the load_image_safe helper method within the class.
```
"""

        return prompt

    def _get_available_images(self, images_folder: str) -> List[str]:
        """Get list of available image files with their full paths"""
        if not images_folder or not os.path.exists(images_folder):
            print(f"Warning: Image folder '{images_folder}' not found or empty.")
            return []
        
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')
        images = []
        
        for file in os.listdir(images_folder):
            if file.lower().endswith(image_extensions):
                images.append(os.path.join(images_folder, file))
        
        return images

    def _extract_clean_code(self, generated_text: str) -> str:
        """
        Extract clean Python code from LLM response, robustly handling markdown fences.
        """
        # Look for a Python code block (```python ... ```)
        code_block_match = re.search(r'```python\n(.*?)```', generated_text, re.DOTALL)
        if code_block_match:
            return code_block_match.group(1).strip()
        
        # If no explicit code block, try to find the class definition
        # This is less ideal but better than nothing
        python_start = re.search(r'(from manim import|import manim|class\s+\w+\s*\(VoiceoverScene\):)', generated_text)
        if python_start:
            return generated_text[python_start.start():].strip()
        
        print("Warning: Could not find a clear Python code block. Returning raw text.")
        return generated_text.strip()

    def _validate_and_fix_code(self, code: str) -> str:
        """Validate and fix common code issues"""
        fixes_applied = []
        
        # Fix common import issues
        if 'from manim import *' not in code:
            code = 'from manim import *\n' + code
            fixes_applied.append('Added missing manim import')
        
        # Ensure VoiceoverScene import
        if 'from manim_voiceover import VoiceoverScene' not in code:
            code = code.replace(
                'from manim import *',
                'from manim import *\nfrom manim_voiceover import VoiceoverScene'
            )
            fixes_applied.append('Added VoiceoverScene import')
        
        # Fix GTTSService import if missing
        if 'GTTSService' in code and 'from manim_voiceover.services.gtts import GTTSService' not in code:
            code = code.replace(
                'from manim_voiceover import VoiceoverScene',
                'from manim_voiceover import VoiceoverScene\nfrom manim_voiceover.services.gtts import GTTSService'
            )
            fixes_applied.append('Added GTTSService import')
        
        # Ensure proper class inheritance for the main animation class
        # Only replace if it doesn't already inherit from VoiceoverScene
        class_definition_match = re.search(r'class\s+(\w+)\s*\((\w+)\):', code)
        if class_definition_match:
            class_name = class_definition_match.group(1)
            base_class = class_definition_match.group(2)
            if base_class != "VoiceoverScene":
                code = re.sub(r'class\s+' + re.escape(class_name) + r'\s*\(' + re.escape(base_class) + r'\):',
                              r'class ' + class_name + r'(VoiceoverScene):', code)
                fixes_applied.append(f'Fixed class {class_name} inheritance to VoiceoverScene')
        else: # If no class definition found, add a default one
            if "class NarrativeEducationalAnimation(VoiceoverScene):" not in code:
                # Attempt to insert it after imports
                insert_pos = code.find("import numpy as np") # A common import point
                if insert_pos == -1: insert_pos = code.find("from manim import *") # Fallback to first import
                if insert_pos != -1:
                    code = code[:insert_pos] + self.base_template.split('class NarrativeEducationalAnimation(VoiceoverScene):')[0] + \
                           'class NarrativeEducationalAnimation(VoiceoverScene):\n    ' + \
                           code[insert_pos:]
                    fixes_applied.append("Added default 'NarrativeEducationalAnimation' class definition.")


        # Add TTS service setup if missing within construct and not already present
        if 'def construct(self):' in code and 'self.set_speech_service' not in code:
            # Check if set_speech_service exists but might be commented out or elsewhere
            if not re.search(r'self\.set_speech_service\(GTTSService\(\)\)', code):
                code = code.replace(
                    'def construct(self):',
                    'def construct(self):\n        self.set_speech_service(GTTSService())'
                )
                fixes_applied.append('Added TTS service setup in construct method')
        
        # Ensure load_image_safe is present
        if 'def load_image_safe(self, image_path, scale=0.5, position=RIGHT*3):' not in code:
            # Extract load_image_safe from the base_template
            load_image_safe_method = re.search(r'(    def load_image_safe\(self,.*?)    def create_title_animation\(self,', self.base_template, re.DOTALL)
            if load_image_safe_method:
                # Find where to insert it within the class
                class_end_match = re.search(r'\n(    def [a-zA-Z_]+\(self,.*\):)', code, re.DOTALL) # Find first method to insert before
                if class_end_match:
                    insert_pos = class_end_match.start(1)
                    code = code[:insert_pos] + load_image_safe_method.group(1) + code[insert_pos:]
                    fixes_applied.append('Added missing load_image_safe helper method.')
                else: # Fallback: append at the end of the class
                    code += '\n' + load_image_safe_method.group(1)
                    fixes_applied.append('Appended missing load_image_safe helper method.')

        # Fix self.wait() after voiceovers in generated section methods (if fallback was used)
        # This is more complex to generalize for LLM output, but for fallback:
        # The prompt strongly suggests `run_time=tracker.duration` for `self.play`.
        # For pure voiceover blocks without animation or short animations, LLM should add self.wait().
        # This fix is more for the _fallback_code.
        
        if fixes_applied:
            print(f"🔧 Applied fixes: {', '.join(fixes_applied)}")
        
        return code

    def _generate_fallback_code(self, sections: List[AnimationSection], available_images: List[str]) -> str:
        """Generate robust fallback code if LLM fails"""
        method_calls = ""
        section_methods = ""
        
        for section in sections:
            method_calls += f"        self.{section.method_name}()\n"
            
            # Generate basic method implementation for fallback
            # Ensure proper voiceover sync for fallback as well
            section_methods += f"""
    def {section.method_name}(self):
        \"\"\"Animate: {section.title}\"\"\"
        # Clear previous objects
        self.play(FadeOut(*self.mobjects)) # Fade out everything visible
        
        section_title = Text("{section.title}", font_size=48, color=BLUE).to_edge(UP)
        self.play(Write(section_title))

        # Combine all segments for a single voiceover in fallback
        full_narration_text = " ".join([seg.text for seg in section.segments])
        if not full_narration_text:
            full_narration_text = f"Content for {section.title} section."

        with self.voiceover(text=full_narration_text) as tracker:
            # Display primary content
            content_objects = []
            
            # Add images if available
            if section.images:
                # Use the first image from the section for simplicity in fallback
                img_name = os.path.basename(section.images[0])
                # Check against available_images for actual path
                full_img_path = next((path for path in available_images if img_name in path), None)
                if full_img_path:
                    image_mobject = self.load_image_safe(full_img_path, scale=0.6, position=RIGHT*3)
                    content_objects.append(image_mobject)
                    self.play(FadeIn(image_mobject))

            # Add simple text for description
            description_text = Text(full_narration_text[:100] + "...", font_size=30).next_to(section_title, DOWN, buff=0.5).to_edge(LEFT)
            content_objects.append(description_text)
            self.play(Write(description_text), run_time=tracker.duration * 0.5) # Play animation for half duration
            
            # Ensure voiceover completes
            self.wait(tracker.duration * 0.5) # Wait for remaining half duration

        self.wait(1) # Short pause between sections
"""
        
        return self.base_template.format(
            method_calls=method_calls,
            section_methods=section_methods
        )


# Usage example and testing
if __name__ == "__main__":
    # Test the generator
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Please set GOOGLE_API_KEY environment variable")
        exit(1)
    
    # Use your real images folder
    images_folder = "output/linear_regression_notes_images"

    generator = ManimCodeGenerator(api_key)
    
    sample_script = """
## Introduction
Welcome to linear regression! [MEDIUM PAUSE] This powerful tool helps us understand relationships in data.

## Core Concepts  
Linear regression uses the equation Y = a + bx. [DISPLAY IMAGE: equation.png]
This equation is fundamental to understanding linear relationships.
"""
    
    code = generator.generate_manim_code(sample_script, images_folder=images_folder)
    print("\n" + "="*80)
    print("Generated code preview:")
    print("="*80)
    print(code)
    print("="*80)
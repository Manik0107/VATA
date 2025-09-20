#!/usr/bin/env python3
"""
Professional Manim Code Generator with Latest Google GenAI SDK
Compatible with Manim 0.19.0+ and Google GenAI 1.19.0 (2025)
Generates high-quality educational videos with synchronized narration
"""

import os
import re
import json
from typing import List, Dict, Optional
from pathlib import Path

# Updated imports for Google GenAI SDK
from google import genai
from google.genai import types

from narrative_parser import AdvancedNarrativeParser, AnimationSection


class ManimCodeGenerator:
    """
    Advanced Manim code generator for professional educational videos
    """

    def __init__(self, api_key: str):
        # Initialize Google GenAI client
        self.client = genai.Client(api_key=api_key)
        self.parser = AdvancedNarrativeParser()

        # Professional template for Manim 0.19.0+
        self.base_template = '''from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np
import os
from pathlib import Path
import uuid
import time

# Enhanced audio timing management to prevent overlapping
class TimingAwareGTTSService(GTTSService):
    def __init__(self, lang="en", tld="com"):
        super().__init__(lang=lang, tld=tld)
        self.segment_count = 0
        self.total_duration = 0.0

    def get_audio(self, text):
        # Add timing tracking
        words = len(text.split())
        estimated_duration = max(words * 0.4, 1.5)  # Estimate: ~2.5 words/second
        self.total_duration += estimated_duration
        self.segment_count += 1
        
        print(f"🎵 Generating audio segment {self.segment_count} (est. {estimated_duration:.1f}s)")
        return super().get_audio(text)

class {class_name}(VoiceoverScene):
    def construct(self):
        # Initialize enhanced TTS service with timing awareness
        self.set_speech_service(TimingAwareGTTSService())
        
        # Set scene background
        self.camera.background_color = "#0d1117"  # Dark background for professional look
        
        # Execute all sections with proper timing
{method_calls}
        
        # Final pause
        self.wait(2)

    def safe_clear_and_transition(self, transition_time=0.5):
        """Safe scene clearing with audio timing consideration"""
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=transition_time)
        self.wait(0.3)  # Buffer for audio cleanup
        self.clear()

    def create_professional_title(self, title_text, subtitle="", font_size=56):
        """Create professional 3Blue1Brown style titles"""
        title = Text(title_text, font_size=font_size, color="#58a6ff", weight=BOLD)
        title.move_to(UP * 1.2)
        
        elements = [title]
        if subtitle:
            sub = Text(subtitle, font_size=font_size//2, color="#7d8590")
            sub.move_to(DOWN * 0.3)
            elements.append(sub)
        
        underline = Line(LEFT * 3, RIGHT * 3, color="#58a6ff", stroke_width=4)
        underline.next_to(title, DOWN, buff=0.5)
        elements.append(underline)
        
        return VGroup(*elements)

{section_methods}

    def load_image_safe(self, image_path, scale=0.5, position=RIGHT*3):
        """Safely load images with fallback for missing files"""
        try:
            if not os.path.isabs(image_path):
                image_path = Path(os.getcwd()) / image_path
            
            img = ImageMobject(str(image_path))
            img.scale(scale)
            img.move_to(position)
            return img
        except Exception as e:
            print(f"Warning: Could not load image {{image_path}}. Error: {{e}}")
            placeholder = Rectangle(width=2.5, height=1.8, color=GREY_B, fill_opacity=0.3)
            placeholder.move_to(position)
            text = Text("Image\\nUnavailable", font_size=18, color=WHITE)
            text.move_to(position)
            return Group(placeholder, text)
    
    def create_title_sequence(self, title_text, subtitle_text=""):
        """Create professional title sequence"""
        # Main title
        title = Text(title_text, font_size=56, color="#58a6ff", weight=BOLD)
        title.move_to(UP * 1.2)
        
        # Subtitle if provided
        if subtitle_text:
            subtitle = Text(subtitle_text, font_size=32, color="#7d8590")
            subtitle.move_to(DOWN * 0.3)
            title_group = VGroup(title, subtitle)
        else:
            title_group = VGroup(title)
        
        # Decorative elements
        underline = Line(LEFT * 3, RIGHT * 3, color="#58a6ff", stroke_width=4)
        underline.next_to(title_group, DOWN, buff=0.5)
        
        return VGroup(title_group, underline)
    
    def create_section_header(self, text, color="#ffa657"):
        """Create consistent section headers"""
        header = Text(text, font_size=40, color=color, weight=BOLD)
        header.to_edge(UP, buff=1)
        
        separator = Line(LEFT * 6, RIGHT * 6, color=color, stroke_width=2)
        separator.next_to(header, DOWN, buff=0.3)
        
        return VGroup(header, separator)
    
    def create_formula_breakdown(self, formula_tex, explanations=None):
        """Create step-by-step formula explanation"""
        formula = MathTex(formula_tex, font_size=48, color=WHITE)
        formula.move_to(ORIGIN)
        
        if explanations:
            explanation_group = VGroup()
            for i, explanation in enumerate(explanations):
                exp_text = Text(explanation, font_size=24, color="#7d8590")
                exp_text.next_to(formula, DOWN, buff=0.5 + i * 0.4)
                explanation_group.add(exp_text)
            
            return VGroup(formula, explanation_group)
        
        return formula
    
    def create_graph_with_axes(self, x_range=[-5, 5], y_range=[-5, 5], 
                             x_length=8, y_length=6, axis_config=None):
        """Create professional-looking axes"""
        if axis_config is None:
            axis_config = {{"color": WHITE, "stroke_width": 2}}
        
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config=axis_config
        )
        
        # Add labels
        x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT, buff=0.3)
        y_label = axes.get_y_axis_label("y", edge=UP, direction=UP, buff=0.3)
        
        return VGroup(axes, x_label, y_label)
    
    def clear_scene_smart(self):
        """Clear scene while preserving important elements"""
        # Remove all mobjects except camera
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=0.5)
    
    def highlight_text_part(self, text_obj, part_indices, color="#ffa657"):
        """Highlight specific parts of text"""
        if hasattr(text_obj, '__getitem__') and len(text_obj) > max(part_indices):
            highlighted_parts = VGroup(*[text_obj[i] for i in part_indices])
            return Indicate(highlighted_parts, color=color)
        return FadeIn(text_obj)  # Fallback
'''

    def generate_manim_code(self, narrative_script: str, images_folder: str = "",
                          metadata: Optional[Dict] = None) -> str:
        """
        Generate complete professional Manim code from narrative script
        """
        print("🚀 Starting professional Manim code generation...")
        
        # Parse narrative script
        parsed_data = self.parser.parse_narrative_script(narrative_script)
        sections = parsed_data['sections']
        
        print(f"📊 Processing {len(sections)} sections...")
        
        # Get available images
        available_images = self._get_available_images(images_folder)
        
        # Determine topic and class name from first section
        topic = sections[0].title if sections else "Educational"
        class_name = self._generate_class_name(topic, metadata)
        
        # Create comprehensive prompt
        prompt = self._create_professional_prompt(sections, available_images, metadata, class_name)
        
        print("🤖 Generating code with Gemini 2.0 Flash...")
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
                config=types.GenerateContentConfig(
                    temperature=0.2,  # Lower for more consistent, professional code
                    max_output_tokens=8192,
                    top_k=40,
                    top_p=0.9,
                ),
            )
            
            if response.candidates and response.candidates[0].content.parts:
                generated_code = response.candidates[0].content.parts[0].text
                print("✅ Successfully generated professional Manim code")
            else:
                print("⚠️ Gemini returned no content. Using enhanced fallback.")
                generated_code = self._generate_enhanced_fallback(sections, available_images, class_name)
            
        except Exception as e:
            print(f"❌ Error with Gemini: {e}")
            generated_code = self._generate_enhanced_fallback(sections, available_images, class_name)
            print("🔄 Using enhanced fallback code generation")
        
        # Clean and validate the generated code
        final_code = self._extract_and_clean_code(generated_code)
        final_code = self._validate_and_enhance_code(final_code, class_name)
        
        print("✨ Professional Manim code generation complete!")
        return final_code

    def _generate_class_name(self, topic: str, metadata: Optional[Dict] = None) -> str:
        """Generate appropriate class name from topic"""
        # Clean topic for class name
        clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
        words = clean_topic.split()
        
        # Create CamelCase class name
        if words:
            class_name = ''.join(word.capitalize() for word in words[:3])  # Limit to 3 words
            class_name += "Animation"
        else:
            class_name = "EducationalAnimation"
        
        return class_name

    def _create_professional_prompt(self, sections: List[AnimationSection], 
                                  available_images: List[str], 
                                  metadata: Optional[Dict], 
                                  class_name: str) -> str:
        """Create comprehensive prompt for professional educational video generation"""
        
        prompt = f"""# PROFESSIONAL EDUCATIONAL VIDEO GENERATOR - MANIM 0.19.0+

## MISSION
Generate a complete, executable, professional-quality educational video using Manim 0.19.0+ that:
- Creates visually stunning, child-friendly explanations
- Uses perfect voiceover synchronization
- Adapts dynamically to any educational topic
- Maintains professional visual standards
- Provides in-depth, step-by-step explanations

## CRITICAL REQUIREMENTS

### 1. PROFESSIONAL VISUAL STANDARDS
- **No overlapping objects**: Always clear previous content with `self.clear_scene_smart()`
- **Proper spacing**: Use consistent positioning with `to_edge()`, `move_to()`, `next_to()`
- **Color scheme**: Use professional colors (#58a6ff for titles, #ffa657 for highlights, #7d8590 for subtitles)
- **Smooth animations**: Use FadeIn, FadeOut, Write, Transform, Create with appropriate timing
- **Clean layout**: Center important content, align text properly

### 2. MANDATORY CLASS STRUCTURE & IMPORTS
**CRITICAL IMPORT RESTRICTIONS:**
- NEVER use `from manim.utils.file_system import find_file`
- NEVER use `from manim.utils.file_ops import find_file` 
- NEVER use any `manim.utils.file_system` imports
- NEVER use any from manim.utils.file_writing import open_file as open_media_file
- Use ONLY standard Python file operations: `os.path`, `pathlib.Path`


### 3. IN-DEPTH EXPLANATIONS
- **Formula breakdowns**: Show each variable separately with explanations
- **Step-by-step reveals**: Build complex concepts progressively
- **Visual annotations**: Use arrows, highlights, and callouts
- **Interactive elements**: Zoom, focus, and emphasize important parts

### 4. PERFECT SYNCHRONIZATION (CRITICAL - NO OVERLAPPING)
```python
with self.voiceover(text="Your narration text here") as tracker:
    # ALWAYS use fallback duration to prevent None errors
    run_time_val = tracker.duration if tracker.duration is not None else 2.0
    
    # Animation that matches the narration
    self.play(Create(object), run_time=run_time_val)
    
    # NEVER add self.wait() inside voiceover context!
    # This causes audio overlapping!

# Add buffer OUTSIDE voiceover context
self.wait(0.3)  # Short pause before next segment
```

### 5. TIMING RULES (ABSOLUTELY CRITICAL)
- **NEVER** use `self.wait()` inside `with self.voiceover()` context
- **ALWAYS** add buffers between segments outside voiceover context
- **ALWAYS** use fallback duration: `tracker.duration if tracker.duration is not None else 2.0`
- **ALWAYS** call `self.safe_clear_and_transition()` between sections

### 6. MANDATORY CLASS STRUCTURE
```python
class {class_name}(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#0d1117"
        
        # Call all section methods in order
        self.animate_introduction()
        # ... other sections
        
        self.wait(2)
    
    # All helper methods (provided in template)
    # All section methods (implement based on narrative)
```

## CONTENT TO IMPLEMENT

### Available Images:
{', '.join([os.path.basename(img) for img in available_images]) if available_images else 'None available'}

### Sections to implement:
"""

        # Add detailed section information
        for i, section in enumerate(sections, 1):
            prompt += f"""
**Section {i}: {section.title}**
- Method: `{section.method_name}()`  
- Duration: ~{section.estimated_duration:.1f}s
- Segments: {len(section.segments)}
- Key visual elements: {', '.join(section.animation_cues) if section.animation_cues else 'None'}
- Math content: {', '.join(section.mathematical_content) if section.mathematical_content else 'None'}
- Images: {', '.join([os.path.basename(img) for img in section.images]) if section.images else 'None'}

Key narration points:
"""
            # Show first few segments as examples
            for j, segment in enumerate(section.segments[:3]):
                prompt += f"  • \"{segment.text[:100]}...\"\n"
            
            if len(section.segments) > 3:
                prompt += f"  • ... and {len(section.segments) - 3} more segments\n"

        prompt += f"""

## IMPLEMENTATION GUIDELINES

### Visual Hierarchy:
1. **Title sequences**: Use `create_title_sequence()` with professional styling
2. **Section headers**: Use `create_section_header()` for consistency  
3. **Main content**: Center stage with proper spacing
4. **Supporting visuals**: Side panels or overlays

### Mathematical Content:
- Use `MathTex(r"...")` for all equations
- Break down formulas step by step
- Highlight variables as they're explained
- Show practical applications

### Graph/Chart Requirements:
- Use `create_graph_with_axes()` for consistency
- Animate data points appearing
- Draw trend lines dynamically
- Add proper labels and legends

### Code Quality Requirements:
- Every section MUST be a separate method
- Use helper methods consistently
- Handle edge cases (missing images, etc.)
- Include proper error handling
- Maintain professional naming conventions

### Example Implementation Pattern:
```python
def animate_core_concepts(self):
    \"\"\"Explain core concepts with visuals\"\"\"
    self.clear_scene_smart()
    
    # Section header
    header = self.create_section_header("Core Concepts")
    self.play(Write(header))
    
    # Main explanation with synchronized voiceover
    with self.voiceover(text="First concept explanation...") as tracker:
        concept_visual = Text("Key Concept", font_size=36)
        self.play(FadeIn(concept_visual), run_time=tracker.duration)
    
    # Continue with more concepts...
```

## OUTPUT REQUIREMENTS

Generate ONLY the complete Python code that:
✅ Implements ALL sections from the narrative
✅ Uses perfect voiceover synchronization  
✅ Follows Manim 0.19.0+ syntax exactly
✅ Creates professional, engaging visuals
✅ Adapts to the specific topic content
✅ Includes all helper methods
✅ Handles mathematical formulas properly
✅ Manages scene transitions smoothly

Class name: `{class_name}`

**CRITICAL**: The code must be immediately executable with:
`manim your_file.py {class_name} -pql --disable_caching`

Start your code with the imports. Do NOT use markdown code blocks.
"""

        return prompt

    def _get_available_images(self, images_folder: str) -> List[str]:
        """Get list of available image files with full paths"""
        if not images_folder or not os.path.exists(images_folder):
            return []
        
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')
        images = []
        
        try:
            for file in os.listdir(images_folder):
                if file.lower().endswith(image_extensions):
                    images.append(os.path.join(images_folder, file))
        except Exception as e:
            print(f"Warning: Error reading images folder: {e}")
        
        return images

    def _extract_and_clean_code(self, generated_text: str) -> str:
        """Extract clean Python code from LLM response"""
        # Remove markdown code blocks if present
        code_block_pattern = r'```(?:python)?\s*(.*?)```'
        code_match = re.search(code_block_pattern, generated_text, re.DOTALL)
        
        if code_match:
            return code_match.group(1).strip()
        
        # Look for class definition start
        class_start = re.search(r'(from manim import|class\s+\w+.*VoiceoverScene)', generated_text)
        if class_start:
            return generated_text[class_start.start():].strip()
        
        # Return as-is if no clear structure found
        return generated_text.strip()

    def _validate_and_enhance_code(self, code: str, class_name: str) -> str:
        """Validate and enhance the generated code"""
        enhancements = []
        
        # Ensure proper imports
        required_imports = [
            'from manim import *',
            'from manim_voiceover import VoiceoverScene',
            'from manim_voiceover.services.gtts import GTTSService',
            'import numpy as np',
            'import os',
            'from pathlib import Path'
        ]
        
        for imp in required_imports:
            if imp not in code:
                code = imp + '\n' + code
                enhancements.append(f'Added missing import: {imp}')
        
        # Ensure proper class definition
        if f'class {class_name}(VoiceoverScene):' not in code:
            class_pattern = r'class\s+(\w+)\s*\([^)]*\):'
            code = re.sub(class_pattern, f'class {class_name}(VoiceoverScene):', code)
            enhancements.append(f'Fixed class name to {class_name}')
        
        # Ensure TTS service setup
        if 'self.set_speech_service(GTTSService())' not in code:
            construct_pattern = r'def construct\(self\):\s*'
            replacement = 'def construct(self):\n        self.set_speech_service(GTTSService())\n        '
            code = re.sub(construct_pattern, replacement, code)
            enhancements.append('Added TTS service setup')
        
        # Ensure background color
        if 'self.camera.background_color' not in code:
            service_line = 'self.set_speech_service(GTTSService())'
            if service_line in code:
                code = code.replace(
                    service_line,
                    service_line + '\n        self.camera.background_color = "#0d1117"'
                )
                enhancements.append('Added professional background color')
        
        # Add helper methods if missing
        if 'def load_image_safe(' not in code:
            # Insert all helper methods before the last closing of the class
            helper_methods = self._get_helper_methods()
            # Find the last method and insert before the class ends
            last_method = re.findall(r'\n    def \w+\([^)]*\):.*?(?=\n    def |\n\n|\Z)', code, re.DOTALL)
            if last_method:
                code += '\n' + helper_methods
                enhancements.append('Added missing helper methods')
        
        if enhancements:
            print(f"🔧 Code enhancements applied: {', '.join(enhancements)}")
        
        return code

    def _get_helper_methods(self) -> str:
        """Get all helper methods as a string"""
        return '''
    def load_image_safe(self, image_path, scale=0.5, position=RIGHT*3):
        """Safely load images with fallback for missing files"""
        try:
            if not os.path.isabs(image_path):
                image_path = Path(os.getcwd()) / image_path
            
            img = ImageMobject(str(image_path))
            img.scale(scale)
            img.move_to(position)
            return img
        except Exception as e:
            print(f"Warning: Could not load image {image_path}. Error: {e}")
            placeholder = Rectangle(width=2.5, height=1.8, color=GREY_B, fill_opacity=0.3)
            placeholder.move_to(position)
            text = Text("Image\\nUnavailable", font_size=18, color=WHITE)
            text.move_to(position)
            return Group(placeholder, text)
    
    def create_title_sequence(self, title_text, subtitle_text=""):
        """Create professional title sequence"""
        title = Text(title_text, font_size=56, color="#58a6ff", weight=BOLD)
        title.move_to(UP * 1.2)
        
        if subtitle_text:
            subtitle = Text(subtitle_text, font_size=32, color="#7d8590")
            subtitle.move_to(DOWN * 0.3)
            title_group = VGroup(title, subtitle)
        else:
            title_group = VGroup(title)
        
        underline = Line(LEFT * 3, RIGHT * 3, color="#58a6ff", stroke_width=4)
        underline.next_to(title_group, DOWN, buff=0.5)
        
        return VGroup(title_group, underline)
    
    def create_section_header(self, text, color="#ffa657"):
        """Create consistent section headers"""
        header = Text(text, font_size=40, color=color, weight=BOLD)
        header.to_edge(UP, buff=1)
        
        separator = Line(LEFT * 6, RIGHT * 6, color=color, stroke_width=2)
        separator.next_to(header, DOWN, buff=0.3)
        
        return VGroup(header, separator)
    
    def clear_scene_smart(self):
        """Clear scene while preserving important elements"""
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=0.5)
'''

    def _generate_enhanced_fallback(self, sections: List[AnimationSection], 
                                  available_images: List[str], 
                                  class_name: str) -> str:
        """Generate enhanced fallback code with professional quality"""
        
        method_calls = ""
        section_methods = ""
        
        for section in sections:
            method_calls += f"        self.{section.method_name}()\n"
            
            # Generate professional section method
            section_methods += f'''
    def {section.method_name}(self):
        """Animate: {section.title}"""
        self.clear_scene_smart()
        
        # Create section header
        header = self.create_section_header("{section.title}")
        self.play(Write(header), run_time=1)
        self.wait(0.5)
        
        # Process narration segments with synchronized visuals
'''
            
            # Add synchronized voiceover for each segment
            for i, segment in enumerate(section.segments):
                section_methods += f'''
        # Segment {i + 1} - Enhanced timing to prevent overlapping
        with self.voiceover(text="{segment.text}") as tracker:
            content = Text(
                "{segment.text[:50]}..." if len("{segment.text}") > 50 else "{segment.text}",
                font_size=28,
                color=WHITE
            ).move_to(ORIGIN)
            
            # CRITICAL: Use proper timing without extra waits
            run_time_val = tracker.duration if tracker.duration is not None else 2.0
            if run_time_val > 2:
                self.play(Write(content), run_time=min(2.0, run_time_val * 0.7))
                # Calculate remaining time and use it for content display
                remaining = max(0, run_time_val - 2.0)
                if remaining > 0:
                    self.wait(remaining)  # Only wait for remaining voiceover time
            else:
                self.play(FadeIn(content), run_time=run_time_val)
            # NO additional wait() here - it causes overlapping!
        
        # Buffer OUTSIDE voiceover context to prevent overlapping
        self.wait(0.3)  # Short buffer between segments
        self.play(FadeOut(content), run_time=0.5)
        self.wait(0.2)  # Additional cleanup time
'''
            
            # Add images if available
            if section.images and available_images:
                section_methods += '''
        # Add relevant image if available
        if True:  # Placeholder for image logic
            image = self.load_image_safe("''' + available_images[0] + '''", scale=0.6)
            self.play(FadeIn(image), run_time=1)
            self.wait(1)
            self.play(FadeOut(image), run_time=0.5)
'''
            
            section_methods += '''
        # Section transition with proper timing
        self.safe_clear_and_transition(0.5)
'''

        # Format the complete code
        return self.base_template.format(
            class_name=class_name,
            method_calls=method_calls,
            section_methods=section_methods
        )


# Test and validation
if __name__ == "__main__":
    # Test with sample data
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
        exit(1)
    
    generator = ManimCodeGenerator(api_key)
    
    sample_narrative = '''
## Introduction
Welcome to our lesson on linear regression! This powerful statistical method helps us understand relationships between variables.

## Mathematical Foundation  
Linear regression uses the equation y = mx + b, where y is the dependent variable, x is independent, m is slope, and b is the y-intercept.

## Practical Application
Let's see how we can use this to predict house prices based on size.
'''
    
    print("🧪 Testing code generation...")
    generated_code = generator.generate_manim_code(
        narrative_script=sample_narrative,
        images_folder="images"
    )
    
    print("\n" + "="*80)
    print("📝 GENERATED CODE PREVIEW:")
    print("="*80)
    print(generated_code[:1500] + "\n... (truncated)")
    print("="*80)
    print("✅ Test completed successfully!")
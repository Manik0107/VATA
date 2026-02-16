#!/usr/bin/env python3
"""
Comprehensive Educational Video Generation System
Inspired by 3Blue1Brown's visual style and educational approach

This system combines:
- Advanced narrative generation
- Sophisticated Manim code generation with self-healing
- Perfect audio-visual synchronization
- Professional animations and subtitles
- Robust error handling and correction
"""

import os
import sys
import json
import re
import subprocess
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from contextlib import redirect_stdout, redirect_stderr
import time

# Import dependencies
from dotenv import load_dotenv
from google import genai
from google.genai import types
from manim import config

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION AND DATACLASSES
# ============================================================================

@dataclass
class VoiceoverSegment:
    """Enhanced voiceover segment with precise timing"""
    text: str
    start_time: float = 0.0
    duration: float = 0.0
    pause_after: float = 0.5
    visual_cues: List[str] = None
    emphasis: str = "normal"  # normal, slow, fast, emphasis
    
    def __post_init__(self):
        if self.visual_cues is None:
            self.visual_cues = []

@dataclass
class AnimationSection:
    """Enhanced section data for professional animations"""
    title: str
    method_name: str
    segments: List[VoiceoverSegment]
    images: List[str]
    diagrams: List[str]
    animation_cues: List[str]
    estimated_duration: float
    mathematical_content: List[str]
    visual_style: str = "professional"  # professional, playful, formal
    complexity_level: str = "medium"    # beginner, medium, advanced
    
    def __post_init__(self):
        if not self.segments:
            self.segments = []
        if not self.images:
            self.images = []
        if not self.diagrams:
            self.diagrams = []
        if not self.animation_cues:
            self.animation_cues = []
        if not self.mathematical_content:
            self.mathematical_content = []

# ============================================================================
# ENHANCED NARRATIVE PARSER
# ============================================================================

class AdvancedNarrativeParser:
    """Advanced parser optimized for educational content"""
    
    def __init__(self):
        self.timing_mappings = {
            'SHORT PAUSE': 1.0,
            'MEDIUM PAUSE': 2.5,
            'LONG PAUSE': 4.0,
            'BRIEF PAUSE': 0.5,
            'EXTENDED PAUSE': 5.0
        }
        
        self.visual_cue_patterns = {
            r'\[DISPLAY IMAGE:\s*([^\]]+)\]': 'image',
            r'\[DISPLAY DIAGRAM:\s*([^\]]+)\]': 'diagram',
            r'\[DISPLAY GRAPH:\s*([^\]]+)\]': 'graph',
            r'\[SHOW EQUATION:\s*([^\]]+)\]': 'equation',
            r'\[ANIMATE:\s*([^\]]+)\]': 'animation',
            r'\[HIGHLIGHT:\s*([^\]]+)\]': 'highlight',
            r'\[ZOOM:\s*([^\]]+)\]': 'zoom'
        }
        
        self.speech_patterns = {
            r'\[SLOW\]': 'slow',
            r'\[FAST\]': 'fast',
            r'\[EMPHASIS\]': 'emphasis',
            r'\[WHISPER\]': 'whisper'
        }
    
    def parse_narrative_script(self, script_content: str) -> Dict:
        """Enhanced parsing for better educational flow"""
        print("🔍 Starting enhanced narrative parsing...")
        
        sections = self._extract_sections(script_content)
        processed_sections = []
        
        total_duration = 0.0
        
        for section_data in sections:
            processed = self._process_section_enhanced(section_data)
            processed_sections.append(processed)
            total_duration += processed.estimated_duration
        
        result = {
            'sections': processed_sections,
            'metadata': {
                'total_sections': len(processed_sections),
                'total_duration': total_duration,
                'complexity_score': self._calculate_complexity_score(processed_sections),
                'educational_level': self._determine_educational_level(processed_sections)
            }
        }
        
        print(f"✅ Parsed {len(processed_sections)} sections")
        print(f"📊 Total duration: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
        
        return result
    
    def _extract_sections(self, script: str) -> List[Dict]:
        """Enhanced section extraction"""
        script = script.encode('utf-8').decode('utf-8-sig').strip()
        parts = re.split(r'^## (.+)$', script, flags=re.MULTILINE)
        
        if parts and not parts[0].strip():
            parts = parts[1:]
        
        sections = []
        for i in range(0, len(parts), 2):
            if i + 1 < len(parts):
                title = parts[i].strip()
                content = parts[i + 1].strip()
                
                if title and content:
                    sections.append({
                        'title': title,
                        'content': content,
                        'position': i // 2
                    })
        
        return sections
    
    def _process_section_enhanced(self, section_data: Dict) -> AnimationSection:
        """Enhanced section processing with better timing"""
        title = section_data['title']
        content = section_data['content']
        
        # Extract enhanced voiceover segments
        segments = self._extract_enhanced_voiceover_segments(content)
        
        # Extract visual elements
        images = self._extract_visual_elements(content, 'image')
        diagrams = self._extract_visual_elements(content, 'diagram')
        
        # Analyze for advanced animation cues
        animation_cues = self._analyze_content_for_enhanced_animations(content, title)
        
        # Extract mathematical content with context
        math_content = self._extract_mathematical_content_enhanced(content)
        
        # Calculate precise duration
        duration = self._calculate_precise_duration(segments, content)
        
        # Determine visual style and complexity
        visual_style = self._determine_visual_style(content, title)
        complexity_level = self._determine_complexity_level(content)
        
        return AnimationSection(
            title=title,
            method_name=self._generate_method_name(title),
            segments=segments,
            images=images,
            diagrams=diagrams,
            animation_cues=animation_cues,
            estimated_duration=duration,
            mathematical_content=math_content,
            visual_style=visual_style,
            complexity_level=complexity_level
        )
    
    def _extract_enhanced_voiceover_segments(self, content: str) -> List[VoiceoverSegment]:
        """Extract segments with precise timing and emphasis"""
        clean_content = re.sub(r'\[[^\]]+\]', '', content)
        clean_content = re.sub(r'\([^)]*\)', '', clean_content)
        
        sentences = re.split(r'(?<=[.!?])\s+', clean_content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
        
        segments = []
        cumulative_time = 0.0
        
        for sentence in sentences:
            # Enhanced duration calculation
            word_count = len(sentence.split())
            
            # Base speaking rate: 140 words per minute for educational content
            base_duration = word_count / 2.3
            
            # Adjust for content complexity
            complexity_multiplier = 1.0
            if any(term in sentence.lower() for term in ['equation', 'formula', 'theorem']):
                complexity_multiplier = 1.4
            elif any(term in sentence.lower() for term in ['example', 'let\'s', 'consider']):
                complexity_multiplier = 1.2
            
            # Adjust for sentence length and punctuation
            if len(sentence) > 100:
                complexity_multiplier *= 1.1
            if ',' in sentence:
                complexity_multiplier *= 1.05
            
            duration = base_duration * complexity_multiplier
            
            # Determine emphasis
            emphasis = "normal"
            if any(word in sentence.lower() for word in ['important', 'crucial', 'key', 'remember']):
                emphasis = "emphasis"
                duration *= 1.1
            
            segments.append(VoiceoverSegment(
                text=sentence,
                start_time=cumulative_time,
                duration=duration,
                pause_after=0.8,  # Longer pauses for better comprehension
                emphasis=emphasis
            ))
            
            cumulative_time += duration + 0.8
        
        return segments
    
    def _extract_visual_elements(self, content: str, element_type: str) -> List[str]:
        """Enhanced visual element extraction"""
        elements = []
        
        for pattern, cue_type in self.visual_cue_patterns.items():
            if cue_type == element_type:
                matches = re.findall(pattern, content)
                elements.extend(matches)
        
        cleaned_elements = []
        for element in elements:
            cleaned = element.strip()
            if cleaned and not cleaned.lower().endswith(('.png', '.jpg', '.jpeg')):
                cleaned += '.png'
            cleaned_elements.append(cleaned)
        
        return list(set(cleaned_elements))
    
    def _analyze_content_for_enhanced_animations(self, content: str, title: str) -> List[str]:
        """Enhanced animation cue analysis"""
        cues = []
        content_lower = content.lower()
        title_lower = title.lower()
        
        # Title-based animations
        if any(word in title_lower for word in ['introduction', 'intro']):
            cues.extend(['create_title_sequence', 'fade_in_background'])
        elif any(word in title_lower for word in ['conclusion', 'summary']):
            cues.extend(['create_summary_animation', 'highlight_key_points'])
        
        # Content-based animations
        if 'equation' in content_lower:
            cues.extend(['build_equation_step_by_step', 'highlight_equation_parts'])
        
        if any(word in content_lower for word in ['graph', 'plot', 'chart']):
            cues.extend(['create_animated_graph', 'show_data_points'])
        
        if 'regression line' in content_lower:
            cues.extend(['animate_regression_line', 'show_residuals'])
        
        if any(word in content_lower for word in ['example', 'let\'s see']):
            cues.extend(['create_example_animation', 'step_by_step_solution'])
        
        # Mathematical content animations
        if re.search(r'y\s*=\s*', content_lower):
            cues.append('animate_function_construction')
        
        if any(word in content_lower for word in ['correlation', 'relationship']):
            cues.append('visualize_correlation')
        
        return list(set(cues))
    
    def _extract_mathematical_content_enhanced(self, content: str) -> List[str]:
        """Enhanced mathematical content extraction with context"""
        math_content = []
        
        # Enhanced patterns for mathematical expressions
        patterns = [
            r'[Yy]\s*=\s*[^.!?]+',  # Equations
            r'[a-zA-Z]\s*=\s*[^.!?]+',  # Variable assignments
            r'r\s*=\s*\d+\.?\d*',  # Correlation coefficients
            r'\b\d+\.?\d*%\b',  # Percentages
            r'[Rr]²?\s*=\s*\d+\.?\d*',  # R-squared values
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            math_content.extend(matches)
        
        return list(set(math_content))
    
    def _calculate_precise_duration(self, segments: List[VoiceoverSegment], content: str) -> float:
        """Calculate precise section duration"""
        segment_duration = sum(seg.duration + seg.pause_after for seg in segments)
        
        # Add time for visual elements
        visual_time = len(re.findall(r'\[DISPLAY [^\]]+\]', content)) * 3.0
        
        # Add time for pauses
        pause_matches = re.findall(r'\[([A-Z]+ PAUSE)\]', content)
        pause_duration = sum(self.timing_mappings.get(pause, 1.0) for pause in pause_matches)
        
        # Add buffer time for smooth transitions
        transition_time = 2.0
        
        return segment_duration + visual_time + pause_duration + transition_time
    
    def _determine_visual_style(self, content: str, title: str) -> str:
        """Determine appropriate visual style"""
        if any(word in title.lower() for word in ['advanced', 'mathematical', 'derivation']):
            return "formal"
        elif any(word in title.lower() for word in ['introduction', 'basic', 'simple']):
            return "playful"
        return "professional"
    
    def _determine_complexity_level(self, content: str) -> str:
        """Determine content complexity level"""
        math_terms = len(re.findall(r'\b(equation|formula|theorem|proof|derivative)\b', content.lower()))
        
        if math_terms >= 5:
            return "advanced"
        elif math_terms >= 2:
            return "medium"
        return "beginner"
    
    def _calculate_complexity_score(self, sections: List[AnimationSection]) -> float:
        """Calculate overall complexity score"""
        total_score = 0.0
        
        for section in sections:
            score = 0.0
            score += len(section.mathematical_content) * 0.5
            score += len(section.images) * 0.3
            score += len(section.animation_cues) * 0.2
            score += section.estimated_duration * 0.01
            
            if section.complexity_level == "advanced":
                score *= 1.5
            elif section.complexity_level == "medium":
                score *= 1.2
            
            total_score += score
        
        return total_score / len(sections) if sections else 0.0
    
    def _determine_educational_level(self, sections: List[AnimationSection]) -> str:
        """Determine overall educational level"""
        advanced_count = sum(1 for s in sections if s.complexity_level == "advanced")
        total_sections = len(sections)
        
        if advanced_count / total_sections > 0.6:
            return "advanced"
        elif advanced_count / total_sections > 0.3:
            return "intermediate"
        return "beginner"
    
    def _generate_method_name(self, title: str) -> str:
        """Generate descriptive method names"""
        method_name = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        method_name = re.sub(r'\s+', '_', method_name.lower())
        
        if not method_name or method_name[0].isdigit():
            method_name = f"section_{method_name}"
        
        return f"animate_{method_name}"

# ============================================================================
# ENHANCED MANIM CODE GENERATOR WITH SELF-HEALING
# ============================================================================

class EnhancedManimCodeGenerator:
    """Enhanced Manim code generator with 3Blue1Brown-style animations"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.parser = AdvancedNarrativeParser()
        self.max_healing_attempts = 8
        
        # Enhanced base template with professional styling
        self.base_template = '''from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np
import os
from pathlib import Path
import math

config.frame_width = 16
config.frame_height = 9
config.pixel_height = 1080
config.pixel_width = 1920

class NarrativeEducationalAnimation(VoiceoverScene):
    def construct(self):
        # Initialize TTS with enhanced settings
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        
        # Set professional color scheme
        self.camera.background_color = "#0F0F23"  # 3Blue1Brown style background
        
        # Add subtle background elements
        self.add_background_elements()
        
        # Execute narrative sections
{method_calls}
        
        # Final fade out
        self.play(FadeOut(*self.mobjects), run_time=2)
        self.wait(1)

{helper_methods}

{section_methods}
'''

    def generate_enhanced_manim_code(self, narrative_script: str, images_folder: str = "",
                                   metadata: Optional[Dict] = None) -> str:
        """Generate enhanced Manim code with self-healing"""
        print("🚀 Starting enhanced Manim code generation...")
        
        parsed_data = self.parser.parse_narrative_script(narrative_script)
        sections = parsed_data['sections']
        
        available_images = self._get_available_images(images_folder)
        
        # Generate code with multiple attempts and self-healing
        for attempt in range(self.max_healing_attempts):
            try:
                print(f"🔄 Generation attempt {attempt + 1}/{self.max_healing_attempts}")
                
                generated_code = self._generate_code_with_ai(sections, available_images, metadata, attempt)
                
                if generated_code:
                    # Validate and test the code
                    validated_code = self._validate_and_enhance_code(generated_code, sections)
                    
                    # Test compilation
                    if self._test_code_compilation(validated_code):
                        print("✅ Code generation and validation successful!")
                        return validated_code
                    else:
                        print(f"❌ Code compilation failed on attempt {attempt + 1}")
                        if attempt < self.max_healing_attempts - 1:
                            print("🔧 Attempting self-healing...")
                
            except Exception as e:
                print(f"❌ Error in attempt {attempt + 1}: {str(e)}")
                if attempt == self.max_healing_attempts - 1:
                    print("🆘 Falling back to template-based generation")
                    return self._generate_fallback_code(sections, available_images)
        
        return self._generate_fallback_code(sections, available_images)
    
    def _generate_code_with_ai(self, sections: List[AnimationSection], available_images: List[str], 
                              metadata: Optional[Dict], attempt: int) -> str:
        """Generate code using AI with enhanced prompts"""
        
        # Create enhanced prompt based on attempt number
        prompt = self._create_enhanced_prompt(sections, available_images, metadata, attempt)
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
                config=types.GenerateContentConfig(
                    temperature=0.1 if attempt < 3 else 0.2,  # Increase creativity on later attempts
                    max_output_tokens=16384,  # Increased for longer, more detailed code
                    top_k=40,
                    top_p=0.9,
                ),
            )
            
            if response.candidates:
                return response.candidates[0].content.parts[0].text
                
        except Exception as e:
            print(f"⚠️ AI generation error: {str(e)}")
            
        return None
    
    def _create_enhanced_prompt(self, sections: List[AnimationSection], available_images: List[str], 
                               metadata: Optional[Dict], attempt: int) -> str:
        """Create comprehensive prompt for high-quality educational animations"""
        
        prompt = f"""# ENHANCED EDUCATIONAL ANIMATION GENERATOR
# 3BLUE1BROWN STYLE MANIM CODE GENERATION - ATTEMPT {attempt + 1}

## MISSION
Create exceptional educational animations that rival 3Blue1Brown's quality with:
- Smooth, professional animations with perfect timing
- Clear, engaging visual explanations
- Perfect audio-visual synchronization  
- Comprehensive educational content presentation
- Built-in subtitle generation
- Error-resistant code structure

## CRITICAL REQUIREMENTS

### 1. BASE STRUCTURE (MANDATORY)
```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np
import os
from pathlib import Path
import math

config.frame_width = 16
config.frame_height = 9
config.pixel_height = 1080
config.pixel_width = 1920

class NarrativeEducationalAnimation(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.camera.background_color = "#0F0F23"
        self.add_background_elements()
        # Method calls here
        self.play(FadeOut(*self.mobjects), run_time=2)
        self.wait(1)
```

### 2. ENHANCED ANIMATION PRINCIPLES

**Perfect Timing Synchronization:**
```python
with self.voiceover(text="Your narration here") as tracker:
    # CRITICAL: Always synchronize animations to tracker.duration
    animation = Create(object)
    self.play(animation, run_time=tracker.duration)
    # If animation is shorter, add: self.wait(tracker.duration - animation_run_time)
```

**Smooth Transitions:**
- Use `Transform` instead of `ReplacementTransform` for equations
- Apply `LaggedStart` for multiple object animations
- Use `Succession` for sequential animations
- Always clear screen with `FadeOut(*self.mobjects)` before new sections

**Professional Color Scheme:**
- Background: `#0F0F23` (3Blue1Brown dark blue)
- Primary text: `WHITE` or `#F0F0F0`
- Emphasis: `YELLOW` (#FFD700)
- Mathematics: `BLUE` (#1E90FF)
- Examples: `GREEN` (#32CD32)
- Warnings: `RED` (#FF6B6B)

### 3. SUBTITLE INTEGRATION
Every voiceover MUST include subtitle display:
```python
with self.voiceover(text="Your text") as tracker:
    subtitle = self.create_subtitle("Your text")
    self.play(Write(subtitle), run_time=0.5)
    # Your animations here
    self.play(FadeOut(subtitle), run_time=0.3)
```

### 4. MATHEMATICAL ANIMATIONS
Build equations step by step:
```python
eq1 = MathTex(r"Y")
eq2 = MathTex(r"Y = a")  
eq3 = MathTex(r"Y = a + bX")
self.play(Write(eq1))
self.wait(0.5)
self.play(Transform(eq1, eq2))
self.wait(0.5)
self.play(Transform(eq1, eq3))
```

### 5. ENHANCED HELPER METHODS (MANDATORY TO INCLUDE)

```python
def add_background_elements(self):
    \"\"\"Add subtle 3Blue1Brown style background\"\"\"
    grid = NumberPlane(
        background_line_style={{"stroke_color": "#1A1A2E", "stroke_width": 1}}
    ).set_opacity(0.1)
    self.add(grid)

def create_subtitle(self, text, font_size=24):
    \"\"\"Create professional subtitles\"\"\"
    subtitle = Text(
        text[:60] + "..." if len(text) > 60 else text,
        font_size=font_size,
        color=WHITE,
        font="Arial"
    ).to_edge(DOWN, buff=0.5)
    
    # Add background for readability
    bg = Rectangle(
        width=subtitle.width + 0.5,
        height=subtitle.height + 0.2,
        fill_color=BLACK,
        fill_opacity=0.7,
        stroke_width=0
    ).move_to(subtitle.get_center())
    
    return Group(bg, subtitle)

def load_image_safe(self, image_path, scale=0.6, position=RIGHT*3):
    \"\"\"Enhanced safe image loading\"\"\"
    try:
        if not os.path.isabs(image_path):
            image_path = Path(os.getcwd()) / image_path
        
        img = ImageMobject(str(image_path))
        img.scale(scale)
        img.move_to(position)
        
        # Add subtle border
        border = Rectangle(
            width=img.width + 0.1,
            height=img.height + 0.1,
            stroke_color=WHITE,
            stroke_width=2,
            fill_opacity=0
        ).move_to(img.get_center())
        
        return Group(img, border)
        
    except Exception as e:
        print(f"Warning: Could not load image {{image_path}}. Error: {{e}}")
        placeholder = Rectangle(width=3, height=2, color=GREY_B, fill_opacity=0.3)
        placeholder.move_to(position)
        text = Text("Image\\nUnavailable", font_size=16, color=WHITE)
        text.move_to(position)
        return Group(placeholder, text)

def create_professional_title(self, title_text, subtitle_text=""):
    \"\"\"Create 3Blue1Brown style titles\"\"\"
    title = Text(
        title_text, 
        font_size=64, 
        color=YELLOW, 
        font="Arial Black",
        weight=BOLD
    )
    
    if subtitle_text:
        subtitle = Text(
            subtitle_text, 
            font_size=32, 
            color=WHITE,
            font="Arial"
        )
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5)
    else:
        title_group = VGroup(title)
    
    title_group.move_to(ORIGIN)
    return title_group

def create_equation_buildup(self, equations_list, position=ORIGIN):
    \"\"\"Create step-by-step equation buildup\"\"\"
    if not equations_list:
        return []
    
    eq_objects = [MathTex(eq, font_size=48, color=WHITE).move_to(position) for eq in equations_list]
    return eq_objects

def highlight_object(self, obj, color=YELLOW, scale_factor=1.1):
    \"\"\"Highlight object with 3Blue1Brown style\"\"\"
    return [
        obj.animate.set_color(color).scale(scale_factor),
        Wait(0.5),
        obj.animate.set_color(WHITE).scale(1/scale_factor)
    ]
```

### 6. SECTION-SPECIFIC REQUIREMENTS

For each section, implement these patterns:

**Introduction Sections:**
- Engaging title sequence with smooth fade-ins
- Brief overview with visual preview
- Clear learning objectives

**Concept Sections:**
- Step-by-step visual buildup
- Interactive demonstrations
- Multiple examples with different approaches

**Mathematical Sections:**
- Equation development with annotations
- Visual representations of abstract concepts
- Color-coded components

**Example Sections:**
- Real-world context establishment  
- Step-by-step solution process
- Result interpretation and significance

**Conclusion Sections:**
- Key points summary with visual callbacks
- Future learning directions
- Encouraging closing message

### 7. SPECIFIC CONTENT TO IMPLEMENT

"""

        # Add section-specific details
        for i, section in enumerate(sections, 1):
            prompt += f"""
**Section {i}: {section.title}**
- Method: `{section.method_name}`
- Duration: {section.estimated_duration:.1f}s
- Complexity: {section.complexity_level}
- Visual Style: {section.visual_style}
- Animation Cues: {', '.join(section.animation_cues[:5])}
- Mathematical Content: {len(section.mathematical_content)} items

Key Voiceover Segments:
"""
            for j, seg in enumerate(section.segments[:3], 1):
                prompt += f"{j}. \"{seg.text[:80]}{'...' if len(seg.text) > 80 else ''}\"\n"
            
            if len(section.segments) > 3:
                prompt += f"... and {len(section.segments) - 3} more segments\n"

        prompt += f"""

### 8. AVAILABLE RESOURCES
- Images: {len(available_images)} files
- Image paths: {', '.join(available_images[:5])}{'...' if len(available_images) > 5 else ''}

### 9. CODE QUALITY REQUIREMENTS
- Every voiceover MUST have subtitle display
- Perfect audio-visual synchronization (use tracker.duration)
- Smooth scene transitions with proper cleanup
- Professional error handling with graceful fallbacks
- No hardcoded indices without bounds checking
- Consistent visual styling throughout
- Educational pacing with adequate pauses

### 10. OUTPUT FORMAT
Generate ONLY the complete Python code. No explanations, no markdown fences.
The code must be immediately executable with: `manim your_file.py -pql --disable_caching`

Start your Python code here:
"""

        return prompt
    
    def _validate_and_enhance_code(self, code: str, sections: List[AnimationSection]) -> str:
        """Comprehensive code validation and enhancement"""
        print("🔧 Validating and enhancing code...")
        
        # Extract clean code
        code = self._extract_clean_code(code)
        
        # Apply multiple enhancement passes
        code = self._fix_imports(code)
        code = self._ensure_class_structure(code)
        code = self._add_missing_helper_methods(code)
        code = self._fix_voiceover_synchronization(code)
        code = self._add_subtitle_integration(code)
        code = self._fix_common_errors(code)
        code = self._optimize_animations(code)
        
        return code
    
    def _extract_clean_code(self, generated_text: str) -> str:
        """Extract and clean generated code"""
        # Remove markdown fences
        code_block_match = re.search(r'```python\n(.*?)```', generated_text, re.DOTALL)
        if code_block_match:
            return code_block_match.group(1).strip()
        
        # Look for class definition start
        python_start = re.search(r'(from manim import|import manim|class\s+\w+.*VoiceoverScene)', generated_text)
        if python_start:
            return generated_text[python_start.start():].strip()
        
        return generated_text.strip()
    
    def _fix_imports(self, code: str) -> str:
        """Ensure all necessary imports are present"""
        required_imports = [
            "from manim import *",
            "from manim_voiceover import VoiceoverScene", 
            "from manim_voiceover.services.gtts import GTTSService",
            "import numpy as np",
            "import os",
            "from pathlib import Path",
            "import math"
        ]
        
        for import_stmt in required_imports:
            if import_stmt not in code:
                code = import_stmt + "\n" + code
        
        return code
    
    def _ensure_class_structure(self, code: str) -> str:
        """Ensure proper class structure and inheritance"""
        if "class NarrativeEducationalAnimation(VoiceoverScene):" not in code:
            # Fix class definition
            class_match = re.search(r'class\s+(\w+)\s*\([^)]*\):', code)
            if class_match:
                code = re.sub(
                    r'class\s+\w+\s*\([^)]*\):',
                    'class NarrativeEducationalAnimation(VoiceoverScene):',
                    code
                )
        
        return code
    
    def _add_missing_helper_methods(self, code: str) -> str:
        """Add essential helper methods if missing"""
        helper_methods = '''
    def add_background_elements(self):
        """Add subtle 3Blue1Brown style background"""
        grid = NumberPlane(
            background_line_style={"stroke_color": "#1A1A2E", "stroke_width": 1}
        ).set_opacity(0.1)
        self.add(grid)

    def create_subtitle(self, text, font_size=24):
        """Create professional subtitles"""
        subtitle = Text(
            text[:60] + "..." if len(text) > 60 else text,
            font_size=font_size,
            color=WHITE,
            font="Arial"
        ).to_edge(DOWN, buff=0.5)
        
        bg = Rectangle(
            width=subtitle.width + 0.5,
            height=subtitle.height + 0.2,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0
        ).move_to(subtitle.get_center())
        
        return Group(bg, subtitle)

    def load_image_safe(self, image_path, scale=0.6, position=RIGHT*3):
        """Enhanced safe image loading"""
        try:
            if not os.path.isabs(image_path):
                image_path = Path(os.getcwd()) / image_path
            
            img = ImageMobject(str(image_path))
            img.scale(scale)
            img.move_to(position)
            
            border = Rectangle(
                width=img.width + 0.1,
                height=img.height + 0.1,
                stroke_color=WHITE,
                stroke_width=2,
                fill_opacity=0
            ).move_to(img.get_center())
            
            return Group(img, border)
            
        except Exception as e:
            print(f"Warning: Could not load image {image_path}. Error: {e}")
            placeholder = Rectangle(width=3, height=2, color=GREY_B, fill_opacity=0.3)
            placeholder.move_to(position)
            text = Text("Image\\nUnavailable", font_size=16, color=WHITE)
            text.move_to(position)
            return Group(placeholder, text)

    def create_professional_title(self, title_text, subtitle_text=""):
        """Create 3Blue1Brown style titles"""
        title = Text(
            title_text, 
            font_size=64, 
            color=YELLOW, 
            font="Arial",
            weight=BOLD
        )
        
        if subtitle_text:
            subtitle = Text(
                subtitle_text, 
                font_size=32, 
                color=WHITE,
                font="Arial"
            )
            title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5)
        else:
            title_group = VGroup(title)
        
        title_group.move_to(ORIGIN)
        return title_group

    def create_equation_buildup(self, equations_list, position=ORIGIN):
        """Create step-by-step equation buildup"""
        if not equations_list:
            return []
        
        eq_objects = [MathTex(eq, font_size=48, color=WHITE).move_to(position) for eq in equations_list]
        return eq_objects

    def highlight_object(self, obj, color=YELLOW, scale_factor=1.1, run_time=1.0):
        """Highlight object with 3Blue1Brown style"""
        original_color = getattr(obj, 'color', WHITE)
        self.play(
            obj.animate.set_color(color).scale(scale_factor),
            run_time=run_time/2
        )
        self.wait(0.3)
        self.play(
            obj.animate.set_color(original_color).scale(1/scale_factor),
            run_time=run_time/2
        )
'''
        
        if "def add_background_elements(self):" not in code:
            # Find the end of the construct method to insert helper methods
            construct_end = re.search(r'(\n    def construct\(self\):.*?)(\n    def \w+|\nclass|\Z)', code, re.DOTALL)
            if construct_end:
                insert_pos = construct_end.end(1)
                code = code[:insert_pos] + helper_methods + code[insert_pos:]
        
        return code
    
    def _fix_voiceover_synchronization(self, code: str) -> str:
        """Fix voiceover synchronization issues"""
        # Pattern to find voiceover blocks without proper synchronization
        voiceover_pattern = r'with self\.voiceover\(text="[^"]*"\) as tracker:\s*\n(.*?)(?=\n    [a-zA-Z]|\n\n|\Z)'
        
        def fix_sync(match):
            content = match.group(1)
            if "tracker.duration" not in content and "self.play" in content:
                # Add proper synchronization
                lines = content.split('\n')
                fixed_lines = []
                for line in lines:
                    if "self.play(" in line and "run_time=" not in line:
                        # Add run_time parameter
                        line = line.rstrip().rstrip(')') + ', run_time=tracker.duration)'
                    fixed_lines.append(line)
                content = '\n'.join(fixed_lines)
            
            text_parts = match.group(0).split('"')
            text_content = text_parts[1] if len(text_parts) > 1 else "narration"
            return f'with self.voiceover(text="{text_content}") as tracker:\n{content}'
        
        try:
            code = re.sub(voiceover_pattern, fix_sync, code, flags=re.DOTALL)
        except Exception as e:
            print(f"Warning: Voiceover sync fix failed: {e}")
        return code
    
    def _add_subtitle_integration(self, code: str) -> str:
        """Add subtitle integration to all voiceover blocks"""
        voiceover_pattern = r'with self\.voiceover\(text="([^"]*)"\) as tracker:'
        
        def add_subtitles(match):
            text = match.group(1)
            return f'''with self.voiceover(text="{text}") as tracker:
            subtitle = self.create_subtitle("{text}")
            self.play(FadeIn(subtitle), run_time=0.5)'''
        
        # Only add subtitles if not already present
        if "create_subtitle" not in code or code.count("create_subtitle") < code.count("with self.voiceover"):
            code = re.sub(voiceover_pattern, add_subtitles, code)
            
            # Add subtitle fadeout before next voiceover or end of method
            code = re.sub(
                r'(self\.play\(FadeIn\(subtitle\), run_time=0\.5\)\s*\n.*?)\n(\s*)(with self\.voiceover|def \w+|$)',
                r'\1\n\2self.play(FadeOut(subtitle), run_time=0.3)\n\2\3',
                code,
                flags=re.DOTALL
            )
        
        return code
    
    def _fix_common_errors(self, code: str) -> str:
        """Fix common Manim coding errors"""
        fixes = [
            # Fix index access without bounds checking
            (r'equation\[(\d+)\]', r'equation[\1] if len(equation) > \1 else equation[0]'),
            
            # Fix empty mobjects fadeout
            (r'self\.play\(FadeOut\(\*self\.mobjects\)\)', 
             r'if self.mobjects: self.play(FadeOut(*self.mobjects))'),
            
            # Fix missing run_time in basic animations
            (r'self\.play\(Write\(([^)]+)\)\)', r'self.play(Write(\1), run_time=1.0)'),
            (r'self\.play\(Create\(([^)]+)\)\)', r'self.play(Create(\1), run_time=1.0)'),
            
            # Fix color assignments
            (r'color=([A-Z_]+)', r'color=\1'),
            
            # Add proper spacing after method definitions
            (r'def (\w+)\(self([^)]*)\):\s*\n', r'def \1(self\2):\n        '),
        ]
        
        for pattern, replacement in fixes:
            code = re.sub(pattern, replacement, code)
        
        return code
    
    def _optimize_animations(self, code: str) -> str:
        """Optimize animations for smooth playback"""
        optimizations = [
            # Use LaggedStart for multiple similar animations
            (r'self\.play\(Create\((\w+)\), Create\((\w+)\), Create\((\w+)\)\)',
             r'self.play(LaggedStart(Create(\1), Create(\2), Create(\3), lag_ratio=0.2))'),
            
            # Optimize Transform animations
            (r'self\.play\(Transform\((\w+), (\w+)\)\)',
             r'self.play(Transform(\1, \2), run_time=1.5)'),
            
            # Add proper waits between major sections
            (r'def animate_(\w+)\(self\):\s*\n',
             r'def animate_\1(self):\n        if self.mobjects: self.play(FadeOut(*self.mobjects))\n        '),
        ]
        
        for pattern, replacement in optimizations:
            code = re.sub(pattern, replacement, code)
        
        return code
    
    def _test_code_compilation(self, code: str) -> bool:
        """Test if the code compiles without syntax errors"""
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            return False
        except Exception as e:
            print(f"Compilation error: {e}")
            return False
    
    def _get_available_images(self, images_folder: str) -> List[str]:
        """Get available image files with full paths"""
        if not images_folder or not os.path.exists(images_folder):
            return []
        
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')
        images = []
        
        for file in os.listdir(images_folder):
            if file.lower().endswith(image_extensions):
                images.append(os.path.join(images_folder, file))
        
        return images
    
    def _generate_fallback_code(self, sections: List[AnimationSection], available_images: List[str]) -> str:
        """Generate robust fallback code with enhanced features"""
        method_calls = ""
        section_methods = ""
        
        for section in sections:
            method_calls += f"        self.{section.method_name}()\n"
            
            section_methods += f'''
    def {section.method_name}(self):
        """Enhanced animation: {section.title}"""
        # Clear previous content
        if self.mobjects:
            self.play(FadeOut(*self.mobjects))
        
        # Create professional title
        section_title = self.create_professional_title("{section.title}")
        self.play(FadeIn(section_title), run_time=2.0)
        self.wait(1.0)
        
        # Process each voiceover segment
        segments_data = {[f'"{seg.text}"' for seg in section.segments[:3]]}
        for i, segment_text in enumerate(segments_data):
            with self.voiceover(text=segment_text) as tracker:
                subtitle = self.create_subtitle(segment_text)
                self.play(FadeIn(subtitle), run_time=0.5)
                
                # Add visual content based on segment
                if i == 0:
                    # First segment - show main concept
                    concept_text = Text(
                        "Key Concept", 
                        font_size=36, 
                        color=YELLOW
                    ).next_to(section_title, DOWN, buff=1.0)
                    self.play(Write(concept_text), run_time=tracker.duration * 0.3)
                
                elif i == 1:
                    # Second segment - show simple visual element
                    visual_element = Circle(radius=0.5, color=BLUE, fill_opacity=0.3)
                    visual_element.move_to(RIGHT * 3)
                    self.play(Create(visual_element), run_time=tracker.duration * 0.4)
                    self.wait(tracker.duration * 0.6)
                
                else:
                    # Other segments - show explanatory content
                    explanation = Text(
                        f"Point {{i+1}}",
                        font_size=28,
                        color=WHITE
                    ).move_to(DOWN * 2)
                    self.play(Write(explanation), run_time=tracker.duration * 0.5)
                    self.wait(tracker.duration * 0.5)
                
                self.play(FadeOut(subtitle), run_time=0.3)
        
        self.wait(2.0)  # Pause between sections
'''
        
        # Create the helper methods section
        helper_methods = '''
    def add_background_elements(self):
        """Add professional background"""
        grid = NumberPlane(
            background_line_style={"stroke_color": "#1A1A2E", "stroke_width": 1}
        ).set_opacity(0.1)
        self.add(grid)

    def create_subtitle(self, text, font_size=24):
        """Create professional subtitles"""
        subtitle = Text(
            text[:60] + "..." if len(text) > 60 else text,
            font_size=font_size,
            color=WHITE,
            font="Arial"
        ).to_edge(DOWN, buff=0.5)
        
        bg = Rectangle(
            width=subtitle.width + 0.5,
            height=subtitle.height + 0.2,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0
        ).move_to(subtitle.get_center())
        
        return Group(bg, subtitle)

    def load_image_safe(self, image_path, scale=0.6, position=RIGHT*3):
        """Safe image loading with professional styling"""
        try:
            if not os.path.isabs(image_path):
                image_path = Path(os.getcwd()) / image_path
            
            img = ImageMobject(str(image_path))
            img.scale(scale)
            img.move_to(position)
            
            border = Rectangle(
                width=img.width + 0.1,
                height=img.height + 0.1,
                stroke_color=WHITE,
                stroke_width=2,
                fill_opacity=0
            ).move_to(img.get_center())
            
            return Group(img, border)
            
        except Exception as e:
            print(f"Warning: Could not load image {image_path}. Error: {e}")
            placeholder = Rectangle(width=3, height=2, color=GREY_B, fill_opacity=0.3)
            placeholder.move_to(position)
            text = Text("Image\\nUnavailable", font_size=16, color=WHITE)
            text.move_to(position)
            return Group(placeholder, text)

    def create_professional_title(self, title_text, subtitle_text=""):
        """Create engaging titles"""
        title = Text(
            title_text, 
            font_size=52, 
            color=YELLOW, 
            font="Arial",
            weight=BOLD
        )
        
        if subtitle_text:
            subtitle = Text(
                subtitle_text, 
                font_size=28, 
                color=WHITE,
                font="Arial"
            )
            title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.5)
        else:
            title_group = VGroup(title)
        
        title_group.move_to(ORIGIN)
        return title_group
'''
        
        return self.base_template.format(
            method_calls=method_calls,
            helper_methods=helper_methods,
            section_methods=section_methods
        )

# ============================================================================
# SELF-HEALING CODE SYSTEM
# ============================================================================

class SelfHealingSystem:
    """Advanced self-healing system for Manim code correction"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.max_healing_attempts = 5
    
    def heal_code(self, code: str, error_logs: str) -> str:
        """Heal code using AI-powered error correction"""
        print("🏥 Starting code healing process...")
        
        healing_prompt = self._create_healing_prompt(code, error_logs)
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[{"role": "user", "parts": [{"text": healing_prompt}]}],
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=16384,
                    top_k=40,
                    top_p=0.9,
                ),
            )
            
            if response.candidates:
                healed_code = response.candidates[0].content.parts[0].text
                return self._extract_clean_code(healed_code)
        
        except Exception as e:
            print(f"❌ Healing failed: {e}")
        
        return code  # Return original if healing fails
    
    def _create_healing_prompt(self, code: str, error_logs: str) -> str:
        """Create prompt for code healing"""
        return f"""# MANIM CODE HEALING EXPERT

You are a senior Manim developer specializing in fixing broken animations.

## TASK
Fix the following Manim code that has errors. Maintain all original functionality and animations.

## CRITICAL RULES
1. Keep ALL original voiceover text and animations
2. Fix ONLY the errors, don't change working parts
3. Ensure perfect audio-visual synchronization
4. Add proper error handling for missing images/files
5. Return ONLY the corrected Python code
6. NO explanations, NO markdown fences, NO extra text

## COMMON ERROR PATTERNS TO FIX
- Index out of bounds: Check array lengths before accessing
- Missing mobjects: Guard FadeOut with `if self.mobjects:`
- Synchronization issues: Use `run_time=tracker.duration`
- Import errors: Add missing imports
- Syntax errors: Fix malformed code
- Attribute errors: Use correct Manim API methods

## BROKEN CODE:
{code}

## ERROR LOGS:
{error_logs}

## CORRECTED CODE (start immediately):
"""
    
    def _extract_clean_code(self, generated_text: str) -> str:
        """Extract clean code from AI response"""
        code_block_match = re.search(r'```python\n(.*?)```', generated_text, re.DOTALL)
        if code_block_match:
            return code_block_match.group(1).strip()
        
        return generated_text.strip()

# ============================================================================
# COMPREHENSIVE EDUCATIONAL VIDEO SYSTEM
# ============================================================================

class ComprehensiveEducationalVideoSystem:
    """Main system orchestrator for professional educational video generation"""
    
    def __init__(self, config_file: str = ".env"):
        load_dotenv(config_file)
        
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ Google/Gemini API key not found. Please set GOOGLE_API_KEY or GEMINI_API_KEY")
        
        self.config = self._load_configuration()
        self.parser = AdvancedNarrativeParser()
        self.code_generator = EnhancedManimCodeGenerator(self.api_key)
        self.healing_system = SelfHealingSystem(self.api_key)
        
        print("🎬 Comprehensive Educational Video System initialized")
        print(f"📝 Narrative: {self.config['narrative_path']}")
        print(f"🖼️ Images: {self.config['images_folder']}")
        print(f"💾 Output: {self.config['output_file']}")
    
    def _load_configuration(self) -> Dict:
        """Load system configuration"""
        return {
            'narrative_path': os.getenv('NARRATIVE_PATH', 'generated_narrative_script.txt'),
            'images_folder': os.getenv('IMAGES_FOLDER', 'output/RELU-Function and Derived Function Review_images'),
            'output_file': os.getenv('OUTPUT_MANIM_FILE', 'enhanced_educational_animation.py'),
            'video_output': os.getenv('VIDEO_OUTPUT_DIR', 'videos'),
            'quality': os.getenv('RENDER_QUALITY', 'high'),
            'include_subtitles': os.getenv('INCLUDE_SUBTITLES', 'true').lower() == 'true',
            'max_healing_attempts': int(os.getenv('MAX_HEALING_ATTEMPTS', '5')),
            'frame_rate': int(os.getenv('FRAME_RATE', '30'))
        }
    
    def generate_complete_educational_video(self, narrative_file: str = None, 
                                          render_immediately: bool = True) -> Dict:
        """Complete pipeline from narrative to final video"""
        print("\n" + "="*80)
        print("🎥 COMPREHENSIVE EDUCATIONAL VIDEO GENERATION")
        print("="*80)
        
        try:
            # Step 1: Process narrative
            narrative_path = narrative_file or self.config['narrative_path']
            narrative_script = self._load_narrative_script(narrative_path)
            
            print(f"📖 Loaded narrative: {len(narrative_script)} characters")
            
            # Step 2: Generate enhanced Manim code
            print("\n🤖 Generating enhanced Manim code...")
            generated_code = self.code_generator.generate_enhanced_manim_code(
                narrative_script=narrative_script,
                images_folder=self.config['images_folder']
            )
            
            # Step 3: Self-healing validation
            print("\n🔧 Validating and self-healing...")
            final_code = self._validate_with_healing(generated_code)
            
            # Step 4: Save code
            self._save_generated_code(final_code)
            
            # Step 5: Render video (if requested)
            video_path = None
            if render_immediately:
                print("\n🎬 Rendering professional video...")
                video_path = self._render_video_with_subtitles()
            
            # Step 6: Generate results
            results = {
                'success': True,
                'narrative_file': narrative_path,
                'manim_file': self.config['output_file'],
                'video_file': video_path,
                'code_length': len(final_code),
                'estimated_duration': self._estimate_video_duration(narrative_script),
                'features': [
                    'Professional 3Blue1Brown-style animations',
                    'Perfect audio-visual synchronization',
                    'Built-in subtitle generation',
                    'Self-healing code system',
                    'Educational pacing and flow'
                ]
            }
            
            self._print_success_summary(results)
            return results
            
        except Exception as e:
            error_msg = f"❌ System error: {str(e)}"
            print(error_msg)
            traceback.print_exc()
            
            return {
                'success': False,
                'error': error_msg,
                'traceback': traceback.format_exc()
            }
    
    def _load_narrative_script(self, file_path: str) -> str:
        """Load and validate narrative script"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Narrative script not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            raise ValueError("Narrative script is empty")
        
        if '##' not in content:
            raise ValueError("No section headers (##) found in narrative script")
        
        return content
    
    def _validate_with_healing(self, code: str) -> str:
        """Validate code with self-healing capabilities"""
        for attempt in range(self.config['max_healing_attempts']):
            print(f"🔍 Validation attempt {attempt + 1}/{self.config['max_healing_attempts']}")
            
            # Test the code
            error_logs = self._test_code_execution(code)
            
            if not error_logs:
                print("✅ Code validation successful!")
                return code
            
            print(f"❌ Errors found: {error_logs[:200]}...")
            
            if attempt < self.config['max_healing_attempts'] - 1:
                print("🏥 Applying self-healing...")
                code = self.healing_system.heal_code(code, error_logs)
            else:
                print("⚠️ Max healing attempts reached, proceeding with last version")
        
        return code
    
    def _test_code_execution(self, code: str) -> str:
        """Test code execution and capture errors"""
        # Save code to temporary file
        temp_file = "temp_test_code.py"
        
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Test compilation first
            try:
                compile(code, temp_file, 'exec')
            except SyntaxError as e:
                return f"Syntax Error: {str(e)}"
            
            # Test basic execution (dry run)
            result = subprocess.run(
                [sys.executable, "-c", f"import sys; sys.path.append('.'); exec(open('{temp_file}').read())"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return result.stderr
            
            return ""  # No errors
            
        except Exception as e:
            return str(e)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def _save_generated_code(self, code: str) -> None:
        """Save generated code with backup"""
        output_path = self.config['output_file']
        
        if os.path.exists(output_path):
            backup_path = f"{output_path}.backup.{int(time.time())}"
            os.rename(output_path, backup_path)
            print(f"📋 Created backup: {backup_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"💾 Saved enhanced code: {output_path}")
    
    def _render_video_with_subtitles(self) -> Optional[str]:
        """Render video with professional settings and subtitles"""
        manim_file = self.config['output_file']
        if not os.path.exists(manim_file):
            print(f"❌ Manim file not found: {manim_file}")
            return None
        
        # Create output directory
        output_dir = self.config['video_output']
        os.makedirs(output_dir, exist_ok=True)
        
        # Set quality based on config
        quality_flags = {
            'low': '-ql',
            'medium': '-qm', 
            'high': '-qh',
            'ultra': '-qk'  # 4K
        }
        quality_flag = quality_flags.get(self.config['quality'], '-qh')
        
        # Manim command
        command = [
            "manim",
            manim_file,
            "NarrativeEducationalAnimation",
            quality_flag,
            "--media_dir", output_dir,
            "--custom_folders",
            "--disable_caching",
            "--flush_cache"
        ]
        
        try:
            print(f"🎬 Rendering with command: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            
            print("✅ Video rendering successful!")
            
            # Find the generated video
            video_path = self._find_generated_video(output_dir, manim_file)
            
            if video_path and os.path.exists(video_path):
                print(f"🎥 Video available at: {video_path}")
                return video_path
            else:
                print("⚠️ Could not locate generated video file")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Video rendering failed: {e}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            return None
    
    def _find_generated_video(self, output_dir: str, manim_file: str) -> Optional[str]:
        """Find the generated video file"""
        video_dir = os.path.join(
            output_dir,
            "videos",
            Path(manim_file).stem,
            f"{self.config['quality']}_30fps"
        )
        
        if os.path.exists(video_dir):
            for file in os.listdir(video_dir):
                if file.endswith('.mp4'):
                    return os.path.join(video_dir, file)
        
        # Fallback: search recursively in output directory
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.mp4') and 'NarrativeEducationalAnimation' in file:
                    return os.path.join(root, file)
        
        return None
    
    def _estimate_video_duration(self, narrative_script: str) -> float:
        """Estimate total video duration from narrative script"""
        parsed_data = self.parser.parse_narrative_script(narrative_script)
        return parsed_data['metadata']['total_duration']
    
    def _print_success_summary(self, results: Dict) -> None:
        """Print comprehensive success summary"""
        print("\n" + "="*80)
        print("🎉 EDUCATIONAL VIDEO GENERATION COMPLETE!")
        print("="*80)
        
        print(f"📄 Narrative processed: {results['narrative_file']}")
        print(f"🐍 Manim code generated: {results['manim_file']}")
        if results['video_file']:
            print(f"🎥 Video rendered: {results['video_file']}")
        print(f"📊 Code length: {results['code_length']:,} characters")
        print(f"⏱️ Estimated duration: {results['estimated_duration']:.1f} seconds")
        
        print(f"\n✨ Features included:")
        for feature in results['features']:
            print(f"   • {feature}")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Review generated code: {results['manim_file']}")
        if results['video_file']:
            print(f"   2. Watch video: {results['video_file']}")
        else:
            print(f"   2. Render video manually: manim {results['manim_file']} -qh --disable_caching")
        print(f"   3. Make adjustments and re-render as needed")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("🎬 Comprehensive Educational Video Generation System")
    print("🎓 Creating 3Blue1Brown-style educational content")
    
    try:
        system = ComprehensiveEducationalVideoSystem()
        
        # Check for command line arguments
        narrative_file = None
        render_now = True
        
        if len(sys.argv) > 1:
            narrative_file = sys.argv[1]
            if len(sys.argv) > 2:
                render_now = sys.argv[2].lower() in ['true', '1', 'yes', 'y']
        
        # Generate complete educational video
        results = system.generate_complete_educational_video(
            narrative_file=narrative_file,
            render_immediately=render_now
        )
        
        if results['success']:
            print("\n🌟 Ready to educate and inspire!")
            return 0
        else:
            print(f"\n❌ Generation failed: {results.get('error', 'Unknown error')}")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️ Process interrupted by user")
        return 130
    except Exception as e:
        print(f"\n💥 System error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
    
    
    
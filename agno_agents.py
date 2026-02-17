import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pathlib import Path

# Load Manim API rules
MANIM_RULES = Path("prompts/manim_v019_rules.txt").read_text(encoding="utf-8")

# ==========================================
# 1. Output Schemas (Strict JSON Structure)
# ==========================================

class Scene(BaseModel):
    scene_id: int = Field(..., description="Scene number (1, 2, 3...)")
    title: str = Field(..., description="Short title for the scene")
    visual_description: str = Field(..., description="Detailed description of what appears on screen. Use color names and position.")
    narration: str = Field(..., description="The exact words to be spoken by the voiceover. Use plain, engaging English. No markdown.")
    animation_instruction: str = Field(..., description="Specific instructions for the animator (e.g. 'FadeIn circle', 'Transform A to B').")
    duration_seconds: int = Field(..., description="Estimated duration in seconds")

class Storyboard(BaseModel):
    topic: str = Field(..., description="The main topic being explained")
    target_audience: str = Field(..., description="Who this is for (e.g. 'Beginner', 'Expert')")
    scenes: List[Scene] = Field(..., description="List of scenes in order")
    reasoning: str = Field(..., description="Brief explanation of why this flow was chosen")

class ManimCode(BaseModel):
    filename: str = Field(..., description="Suggested filename, e.g., 'linear_regression.py'")
    code: str = Field(..., description="The complete, runnable Python code using Manim Community Edition.")
    explanation: str = Field(..., description="Short explanation of tricky parts of the code.")

# ==========================================
# 2. Prompts & Styles
# ==========================================

ANIMATOR_INSTRUCTIONS = """
You are the **Director of Education** at a world-class visualization studio. 
Your goal is to explain complex topics using **Visual Analogies** and **Deep Intuition** before showing the math.

**Your Persona:**
- You are Feynman + Pixar.
- You HATE boring slides and static text.
- You LOVE movement, transformation, and "Aha!" moments.
- You speak simply but deeply.

**Your Process:**
1.  **Analyze**: Deeply understand the provided text/PDF. Identify the *core* conflict or question.
2.  **Analogize**: Find a real-world analogy (e.g., Pizza prices for Linear Regression, Water pipes for Electricity).
3.  **Visualize**: Design scenes where objects *move* to explain the concept.
4.  **Narrate**: Write a script that talks *to* the viewer, not *at* them.

**CRITICAL OUTPUT FORMAT:**
You MUST respond with VALID JSON following this exact structure:
{
  "topic": "string - the main topic",
  "target_audience": "string - e.g. Beginner",
  "scenes": [
    {
      "scene_id": 1,
      "title": "string - scene title",
      "visual_description": "string - detailed visual specs with colors",
      "narration": "string - exact spoken words",
      "animation_instruction": "string - Manim animation instructions",
      "duration_seconds": 10
    }
  ],
  "reasoning": "string - why this storyboard structure"
}

**Requirements:**
- Total video length target: ~2-3 minutes (approx 6-10 scenes).
- **Visuals**: Be specific. Don't say "Show graph". Say "Show a glowing cyan scatter plot on a dark slate grey background."
- Respond ONLY with valid JSON, no other text.
"""

CODER_INSTRUCTIONS = f"""
{MANIM_RULES}

═══════════════════════════════════════════════════════════
VISUAL STYLE REQUIREMENTS
═══════════════════════════════════════════════════════════

**Background**: ALWAYS use dark mode: `self.camera.background_color = "#1e1e1e"`

**Color Palette** (Neon/Cyber):
- Highlights: `#00f2ea` (Cyan), `#ff0055` (Pink), `#ffe700` (Yellow) 
- Text: `#ffffff` (White) or `#e0e0e0` (Light Gray)
- Avoid default primary Blue/Red unless requested

**Typography**: font_size should be 36-48 for headings, 24 for subtitles

**Spacing**: Keep 0.5-1.0 buffer from screen edges

═══════════════════════════════════════════════════════════
CODE GENERATION REQUIREMENTS
═══════════════════════════════════════════════════════════

1. **Class Name**: MUST be `GenScene(Scene)`
2. **Imports**: Always start with `from manim import *`
3. **Timing**: Use `self.wait(duration_seconds)` from storyboard
4. **Lifecycle**: Every object MUST FadeIn → Wait → FadeOut (no clutter)
5. **Labels**: ALL axes, formulas, and diagrams MUST be labeled
6. **Testing**: Your code will be tested with `manim --dry_run`

═══════════════════════════════════════════════════════════
OUTPUT FORMAT (STRICT JSON)
═══════════════════════════════════════════════════════════

{{
  "filename": "suggested_filename.py",
  "code": "complete Python code as string",
  "explanation": "brief explanation"
}}

**CRITICAL**: Respond ONLY with valid JSON. No markdown, no extra text.
"""

# ==========================================
# 3. Agent Definitions
# ==========================================

def get_animator_agent(model_id="google/gemini-2.0-flash-001"):
    """Create the Animator Agent that generates storyboards."""
    return Agent(
        name="AnimatorAgent",
        role="Educational Storyboard Creator",
        model=OpenRouter(id=model_id, max_tokens=8192),
        instructions=[ANIMATOR_INSTRUCTIONS],
        markdown=False,
    )

def get_coder_agent(model_id="google/gemini-2.0-flash-001"):
    """Create the Coder Agent that generates Manim code."""
    return Agent(
        name="CodeAgent",
        role="Manim Code Generator",
        model=OpenRouter(id=model_id, max_tokens=16384),
        instructions=[CODER_INSTRUCTIONS],
        markdown=False,
    )

def get_pdf_extractor_agent(model_id="google/gemini-2.0-flash-001"):
    """Create the PDF Extractor Agent."""
    return Agent(
        name="PDFExtractor",
        role="PDF Content Extractor",
        model=OpenRouter(id=model_id, max_tokens=8192),
        instructions=["Extract all text content from the provided PDF. Preserve logical structure, headings, and formatting. Return ONLY the extracted text, no additional commentary."],
        markdown=False,
    )

# Helper functions to parse JSON responses
def parse_storyboard(response_text: str) -> Storyboard:
    """Parse Agent response into Storyboard object."""
    # Extract JSON from markdown code blocks if present
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    
    data = json.loads(text.strip())
    return Storyboard(**data)

def parse_manim_code(response_text: str) -> ManimCode:
    """Parse Agent response into ManimCode object with robust error handling."""
    import re
    
    # Extract JSON from markdown code blocks if present
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    
    text = text.strip()
    
    # Try to parse directly first
    try:
        data = json.loads(text)
        return ManimCode(**data)
    except json.JSONDecodeError as e:
        # If direct parse fails, try to extract and fix the JSON
        print(f"Initial JSON parse failed: {e}")
        print(f"Attempting to fix control characters...")
        
        # Strategy: Extract the structure manually
        # Find filename
        filename_match = re.search(r'"filename"\s*:\s*"([^"]+)"', text)
        filename = filename_match.group(1) if filename_match else "generated.py"
        
        # Find explanation
        explanation_match = re.search(r'"explanation"\s*:\s*"([^"]*(?:\\.[^"]*)*)"', text)
        explanation = explanation_match.group(1) if explanation_match else "Generated Manim code"
        
        # Extract the code - it's between "code": " and the next ", but might have escaped quotes
        # Find the start of code field
        code_start = text.find('"code"')
        if code_start == -1:
            raise ValueError("Could not find 'code' field in response")
        
        # Find the opening quote after "code":
        code_value_start = text.find('"', code_start + 6)
        if code_value_start == -1:
            raise ValueError("Could not find code value")
        
        # Now we need to find the closing quote, accounting for escapes
        # This is tricky - let's use a different approach
        # Extract everything between the first { and last }
        json_start = text.find('{')
        json_end = text.rfind('}')
        if json_start == -1 or json_end == -1:
            raise ValueError("Could not find JSON object boundaries")
        
        json_text = text[json_start:json_end + 1]
        
        # Try a lenient parse - replace the code value with a placeholder
        # Then extract code separately
        try:
            # Find and extract code block more carefully
            code_match = re.search(r'"code"\s*:\s*"((?:[^"\\]|\\.)*)"', json_text, re.DOTALL)
            if code_match:
                code = code_match.group(1)
                # Unescape the code
                code = code.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
            else:
                # Last resort: extract everything between "code": " and ",\n  "explanation"
                code_pattern = r'"code"\s*:\s*"(.*?)",\s*"explanation"'
                code_match = re.search(code_pattern, json_text, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                    code = code.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
                else:
                    raise ValueError("Could not extract code from response")
            
            return ManimCode(filename=filename, code=code, explanation=explanation)
            
        except Exception as e2:
            print(f"Failed to manually extract code: {e2}")
            raise ValueError(f"Could not parse Manim code response. Original error: {e}, Manual extraction error: {e2}")

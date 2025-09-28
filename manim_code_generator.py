#!/usr/bin/env python3
"""
Enhanced Professional Manim Code Generator with Advanced Educational Visualizations
Creates dynamic, concept-focused animations that build understanding progressively
Compatible with Manim 0.19.0+ and Google GenAI 1.19.0 (2025)
"""

import os
import re
import json
import time
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

# Updated imports for Google GenAI SDK
from google import genai
from google.genai import types

from narrative_parser import AdvancedNarrativeParser, AnimationSection


class EnhancedManimCodeGenerator:
    """
    Professional Manim code generator with advanced educational visualizations
    """

    def __init__(self, api_key: str):
        # Initialize Google GenAI client
        self.client = genai.Client(api_key=api_key)
        self.parser = AdvancedNarrativeParser()
        
        # Enhanced base template with professional animation capabilities
        self.professional_base_template = '''import gc
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np

class {class_name}(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#0d1117"
        
        # Professional color scheme
        self.colors = {{
            'primary': "#58a6ff", 'secondary': "#ffa657", 'success': "#56d364",
            'warning': "#e3b341", 'danger': "#f85149", 'text': "#f0f6fc",
            'accent': "#bd93f9", 'highlight': "#ff79c6", 'muted': "#6272a4",
            'actual': "#50fa7b", 'predicted': "#ff5555", 'error': "#ffb86c"
        }}
        
        # Layout zones for consistent positioning
        self.zones = {{
            'title': UP * 3.2, 'header': UP * 2.5, 'main': ORIGIN,
            'left': LEFT * 5, 'right': RIGHT * 4.5, 'bottom': DOWN * 3,
            'formula': UP * 1.5, 'graph': DOWN * 0.5, 'legend': RIGHT * 5 + UP * 2
        }}
        
        # Animation timing constants
        self.timing = {{
            'fast': 0.5, 'normal': 1.0, 'slow': 1.5, 'pause': 0.3
        }}
        
        # Persistent elements that stay throughout video
        self.persistent_elements = Group()
        
        # Execute sections with error handling
        try:
            self.setup_scene()
            self.intro_sequence()
{method_calls}
            self.conclusion_sequence()
            self.cleanup_scene()
        except Exception as e:
            print(f"Animation error: {{e}}")
            self.error_recovery()

    def setup_scene(self):
        """Setup persistent scene elements"""
        # Add subtle background pattern
        background_dots = Group()
        for i in range(20):
            for j in range(12):
                dot = Dot(radius=0.02, color=self.colors['muted'], fill_opacity=0.3)
                dot.move_to(LEFT * 6 + RIGHT * 0.6 * i + UP * 3 + DOWN * 0.5 * j)
                background_dots.add(dot)
        background_dots.set_opacity(0.1)
        self.add(background_dots)

    def intro_sequence(self):
        """Professional intro with topic-specific elements"""
        # Main title with professional styling
        title = Text("Educational Exploration", font_size=48, color=self.colors['primary'])
        title.move_to(self.zones['title'])
        
        # Animated underline
        underline = Line(LEFT * 3, RIGHT * 3, color=self.colors['accent'], stroke_width=3)
        underline.next_to(title, DOWN, buff=0.2)
        underline.set_opacity(0)
        
        subtitle = Text("Deep Understanding Through Visualization", 
                       font_size=24, color=self.colors['text'])
        subtitle.next_to(underline, DOWN, buff=0.5)
        
        with self.voiceover(text="Welcome to our comprehensive exploration of this fascinating topic") as tracker:
            # Animated title appearance
            self.play(
                DrawBorderThenFill(title),
                run_time=tracker.duration * 0.4
            )
            self.play(
                Create(underline),
                FadeIn(subtitle),
                run_time=tracker.duration * 0.6
            )
        
        self.wait(self.timing['pause'])
        
        # Transform to make space for content
        self.play(
            title.animate.scale(0.7).move_to(self.zones['header']),
            FadeOut(underline),
            subtitle.animate.scale(0.8).next_to(title, DOWN, buff=0.1),
            run_time=self.timing['normal']
        )
        
        # Add title to persistent elements
        self.persistent_elements.add(title, subtitle)

    def conclusion_sequence(self):
        """Professional conclusion with summary elements"""
        # Clear main content but keep persistent elements
        self.clear_main_content()
        
        conclusion_title = Text("Key Insights", font_size=36, color=self.colors['success'])
        conclusion_title.move_to(self.zones['main'] + UP * 2)
        
        insights = VGroup(
            Text("• Deep understanding achieved", color=self.colors['text']),
            Text("• Concepts visualized clearly", color=self.colors['text']),
            Text("• Ready for practical application", color=self.colors['text'])
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        insights.next_to(conclusion_title, DOWN, buff=0.5)
        
        with self.voiceover(text="We've explored the key concepts and gained deep understanding through visualization") as tracker:
            self.play(Write(conclusion_title), run_time=tracker.duration * 0.3)
            for insight in insights:
                self.play(FadeIn(insight), run_time=tracker.duration * 0.2)
        
        self.wait(2)

    def cleanup_scene(self):
        """Clean up scene resources"""
        gc.collect()

    def error_recovery(self):
        """Graceful error recovery"""
        error_msg = Text("Processing educational content...", 
                        font_size=24, color=self.colors['warning'])
        error_msg.move_to(self.zones['main'])
        self.play(Write(error_msg))
        self.wait(2)

    def clear_main_content(self):
        """Clear main content area while preserving persistent elements"""
        # This would be implemented to selectively clear content
        pass

    def create_scatter_plot_with_regression(self, data_points, title="Data Visualization", 
                                          show_errors=True, animate_line_fitting=True):
        """
        Create professional scatter plot with regression line and error visualization
        """
        # Create axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=6,
            y_length=4,
            axis_config={{
                "color": self.colors['text'],
                "stroke_width": 2,
                "include_numbers": True,
                "font_size": 20
            }}
        ).move_to(self.zones['graph'])
        
        # Axis labels
        x_label = axes.get_x_axis_label("X Variable", direction=DOWN, buff=0.3)
        y_label = axes.get_y_axis_label("Y Variable", direction=LEFT, buff=0.3)
        
        # Create data points
        actual_points = Group()
        predicted_points = Group()
        error_lines = Group()
        
        for i, (x, y) in enumerate(data_points):
            # Actual data point
            actual_point = Dot(axes.coords_to_point(x, y), 
                             color=self.colors['actual'], radius=0.08)
            actual_points.add(actual_point)
            
            # Predicted point (on regression line)
            y_pred = self.calculate_regression_prediction(x, data_points)
            pred_point = Dot(axes.coords_to_point(x, y_pred),
                           color=self.colors['predicted'], radius=0.06)
            predicted_points.add(pred_point)
            
            if show_errors:
                # Error line
                error_line = Line(
                    axes.coords_to_point(x, y),
                    axes.coords_to_point(x, y_pred),
                    color=self.colors['error'],
                    stroke_width=2
                )
                error_lines.add(error_line)
        
        # Regression line
        regression_line = self.create_regression_line(axes, data_points)
        
        # Legend
        legend = self.create_legend([
            ("Actual Data", self.colors['actual']),
            ("Predictions", self.colors['predicted']),
            ("Errors", self.colors['error']),
            ("Best Fit Line", self.colors['primary'])
        ])
        
        return {{
            'axes': axes,
            'labels': Group(x_label, y_label),
            'actual_points': actual_points,
            'predicted_points': predicted_points,
            'error_lines': error_lines,
            'regression_line': regression_line,
            'legend': legend
        }}

    def animate_regression_concept(self, plot_elements):
        """
        Animate the regression concept step by step
        """
        axes = plot_elements['axes']
        actual_points = plot_elements['actual_points']
        predicted_points = plot_elements['predicted_points']
        error_lines = plot_elements['error_lines']
        regression_line = plot_elements['regression_line']
        legend = plot_elements['legend']
        
        # Step 1: Show axes and data
        with self.voiceover(text="Let's start with our data points representing real observations") as tracker:
            self.play(
                Create(axes),
                Write(plot_elements['labels']),
                run_time=tracker.duration * 0.5
            )
            
            # Animate points appearing one by one
            for point in actual_points:
                self.play(GrowFromCenter(point), run_time=tracker.duration * 0.5 / len(actual_points))
        
        # Step 2: Show the goal - find the best fit line
        with self.voiceover(text="Our goal is to find the line that best represents the relationship in this data") as tracker:
            self.play(Create(regression_line), run_time=tracker.duration)
        
        # Step 3: Show predictions
        with self.voiceover(text="This line allows us to make predictions for any X value") as tracker:
            for pred_point in predicted_points:
                self.play(GrowFromCenter(pred_point), run_time=tracker.duration / len(predicted_points))
        
        # Step 4: Visualize errors
        with self.voiceover(text="The difference between actual and predicted values represents our prediction errors") as tracker:
            for error_line in error_lines:
                self.play(Create(error_line), run_time=tracker.duration / len(error_lines))
        
        # Step 5: Show legend
        with self.voiceover(text="Each element helps us understand the relationship between variables") as tracker:
            self.play(FadeIn(legend), run_time=tracker.duration)
        
        self.wait(self.timing['pause'])

    def create_regression_line(self, axes, data_points):
        """Create regression line from data points"""
        # Simple linear regression calculation
        n = len(data_points)
        sum_x = sum(point[0] for point in data_points)
        sum_y = sum(point[1] for point in data_points)
        sum_xy = sum(point[0] * point[1] for point in data_points)
        sum_x2 = sum(point[0] ** 2 for point in data_points)
        
        # Calculate slope and intercept
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Create line
        x_min, x_max = 0, 10
        y_min = slope * x_min + intercept
        y_max = slope * x_max + intercept
        
        line = Line(
            axes.coords_to_point(x_min, y_min),
            axes.coords_to_point(x_max, y_max),
            color=self.colors['primary'],
            stroke_width=3
        )
        
        return line

    def calculate_regression_prediction(self, x, data_points):
        """Calculate regression prediction for a given x"""
        # Simple implementation - in real use, this would use the fitted line
        n = len(data_points)
        sum_x = sum(point[0] for point in data_points)
        sum_y = sum(point[1] for point in data_points)
        sum_xy = sum(point[0] * point[1] for point in data_points)
        sum_x2 = sum(point[0] ** 2 for point in data_points)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        return slope * x + intercept

    def create_legend(self, items):
        """Create a professional legend"""
        legend_items = Group()
        
        for i, (label, color) in enumerate(items):
            # Create indicator (dot or line based on what it represents)
            if "Line" in label:
                indicator = Line(LEFT * 0.3, RIGHT * 0.3, color=color, stroke_width=3)
            else:
                indicator = Dot(color=color, radius=0.06)
            
            text = Text(label, font_size=16, color=self.colors['text'])
            text.next_to(indicator, RIGHT, buff=0.2)
            
            item = Group(indicator, text)
            legend_items.add(item)
        
        legend_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend_box = SurroundingRectangle(
            legend_items, 
            color=self.colors['muted'],
            fill_opacity=0.1,
            stroke_opacity=0.5,
            buff=0.3
        )
        
        legend = Group(legend_box, legend_items)
        legend.move_to(self.zones['legend'])
        
        return legend

    def create_formula_animation(self, formula_tex, title="Mathematical Foundation"):
        """Create animated formula with step-by-step revelation"""
        title_text = Text(title, font_size=32, color=self.colors['secondary'])
        title_text.move_to(self.zones['formula'] + UP * 0.5)
        
        # Create formula with highlighting capability
        formula = MathTex(formula_tex, color=self.colors['text'], font_size=36)
        formula.move_to(self.zones['formula'])
        
        # Explanation box
        explanation = Text("", font_size=20, color=self.colors['muted'])
        explanation.next_to(formula, DOWN, buff=0.5)
        
        return {{
            'title': title_text,
            'formula': formula,
            'explanation': explanation
        }}

    def animate_formula_derivation(self, steps, explanations):
        """Animate step-by-step formula derivation"""
        current_formula = None
        
        for i, (step, explanation) in enumerate(zip(steps, explanations)):
            formula_elements = self.create_formula_animation(step, f"Step {{i+1}}")
            
            with self.voiceover(text=explanation) as tracker:
                if i == 0:
                    # First step - introduce
                    self.play(
                        Write(formula_elements['title']),
                        Write(formula_elements['formula']),
                        run_time=tracker.duration * 0.7
                    )
                else:
                    # Transform from previous step
                    self.play(
                        Transform(current_formula, formula_elements['formula']),
                        Transform(formula_elements['title'], formula_elements['title']),
                        run_time=tracker.duration * 0.7
                    )
                
                # Show explanation
                explanation_text = Text(explanation[:100], font_size=18, color=self.colors['muted'])
                explanation_text.move_to(self.zones['bottom'])
                self.play(FadeIn(explanation_text), run_time=tracker.duration * 0.3)
                
                current_formula = formula_elements['formula']
            
            self.wait(self.timing['pause'])

    def load_image_safe(self, path, scale=0.5, position=None):
        """Safely load and position images with fallback"""
        try:
            if os.path.exists(path):
                img = ImageMobject(path).scale(scale)
                if position: 
                    img.move_to(position)
                return img
        except Exception as e:
            print(f"Could not load image {{path}}: {{e}}")
        
        # Professional fallback
        placeholder = RoundedRectangle(
            width=4, height=3, corner_radius=0.2,
            color=self.colors['text'], fill_opacity=0.05, stroke_opacity=0.3
        )
        icon = Text("📊", font_size=48)
        text = Text("Visual Content", font_size=16, color=self.colors['muted'])
        text.next_to(icon, DOWN)
        
        fallback_group = Group(placeholder, icon, text)
        if position:
            fallback_group.move_to(position)
        
        return fallback_group

{section_methods}
'''

    def generate_enhanced_manim_code(self, narrative_script: str, images_folder: str = "",
                                   metadata: Optional[Dict] = None, 
                                   complexity_analysis: Optional[Dict] = None,
                                   config: Optional[Dict] = None,
                                   parsed_data: Optional[Dict] = None) -> str:
        """
        Generate professional Manim code with advanced visualizations and voiceover
        """
        print("🎬 Starting professional Manim code generation with voiceover integration...")
        
        # Parse narrative script if not already parsed
        if parsed_data is None:
            parsed_data = self.parser.parse_narrative_script(narrative_script)
        
        sections = parsed_data['sections']
        
        print(f"📊 Processing {len(sections)} sections with enhanced visualizations and voiceover...")
        print(f"🎙️ Voiceover segments: {sum(len(s.segments) for s in sections)}")
        
        # Get available images
        available_images = self._get_available_images(images_folder)
        
        # Determine class name and topic type
        topic = sections[0].title if sections else "Educational"
        class_name = self._generate_class_name(topic)
        topic_type = self._analyze_topic_type(narrative_script)
        
        print(f"🎯 Detected topic type: {topic_type}")
        
        # Check if voiceover is enabled (default to True)
        voiceover_enabled = parsed_data.get('metadata', {}).get('voiceover_enabled', True)
        print(f"🎤 Voiceover enabled: {voiceover_enabled}")
        
        # Create enhanced prompt with topic-specific instructions and voiceover data
        prompt = self._create_professional_prompt_with_voiceover(
            sections, available_images, class_name, topic_type, complexity_analysis, parsed_data
        )
        
        print("Generating enhanced code with Gemini 2.0 Flash...")
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Lower for more consistent code
                    max_output_tokens=8192,
                    top_k=30,
                    top_p=0.85,
                ),
            )
            
            if response.candidates and response.candidates[0].content.parts:
                generated_code = response.candidates[0].content.parts[0].text
                print("Successfully generated professional Manim code with voiceover")
            else:
                print("Gemini response incomplete, using enhanced fallback with voiceover")
                generated_code = self._generate_professional_fallback_with_voiceover(
                    sections, available_images, class_name, topic_type, parsed_data
                )
            
        except Exception as e:
            print(f"Error with Gemini: {e}")
            generated_code = self._generate_professional_fallback_with_voiceover(
                sections, available_images, class_name, topic_type, parsed_data
            )
        
        # Clean and enhance code
        final_code = self._extract_and_clean_code(generated_code)
        final_code = self._enhance_code_for_topic(final_code, topic_type)
        final_code = self._validate_professional_code(final_code, class_name)
        
        print("Professional Manim code generation with voiceover complete!")
        return final_code

    def _create_professional_prompt_with_voiceover(self, sections: List[AnimationSection], 
                                                 available_images: List[str], class_name: str,
                                                 topic_type: str, complexity_analysis: Optional[Dict] = None,
                                                 parsed_data: Optional[Dict] = None) -> str:
        """Create professional prompt with voiceover integration"""
        
        # Topic-specific visualization instructions
        viz_instructions = self._get_topic_visualization_instructions(topic_type)
        
        prompt = f"""Generate PROFESSIONAL educational Manim code with ADVANCED VISUALIZATIONS and SYNCHRONIZED VOICEOVER.

CRITICAL REQUIREMENTS:
- Class: {class_name}(VoiceoverScene) 
- Create STUNNING, EDUCATIONAL animations like 3Blue1Brown quality
- Use ADVANCED visual techniques: scatter plots, regression lines, error visualization
- PROGRESSIVE revelation - build understanding step by step
- Keep ALL relevant elements visible - DON'T erase previous content unnecessarily
- Use color coding for different concepts (actual vs predicted, etc.)
- Include SMOOTH animations and transitions
- SYNCHRONIZE all animations with voiceover using 'with self.voiceover(text="...") as tracker:'
- ⚠️ CRITICAL: Ensure all text and animations are arranged so there is no overlap between any objects, using appropriate positioning methods like .arrange(), .next_to(), and .shift(). All elements must be clearly readable and not cover each other at any point in the animation.

TOPIC TYPE DETECTED: {topic_type.upper()}
{viz_instructions}

VOICEOVER INTEGRATION:
- Use voiceover segments for natural speech timing
- Synchronize animations with tracker.duration
- Include natural pauses between concepts
- Use clear, educational language

SECTIONS TO IMPLEMENT ({len(sections)} total):
"""
        
        # Add section details with voiceover segments
        for i, section in enumerate(sections, 1):
            prompt += f"""
Section {i}: {section.title}
Method: {section.method_name}()
Voiceover segments: {len(section.segments)}
"""
            # Add first few voiceover segments as examples
            for j, segment in enumerate(section.segments[:2]):
                prompt += f"  - Segment {j+1}: \"{segment.text[:100]}...\"\n"

        # Add professional code structure requirements
        prompt += f"""
GENERATE COMPLETE, PROFESSIONAL MANIM CODE with VOICEOVER:

```python
import gc
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np

class {class_name}(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#0d1117"
        
        # Professional color scheme with semantic meaning
        self.colors = {{
            'primary': "#58a6ff", 'secondary': "#ffa657", 'success': "#56d364",
            'actual': "#50fa7b", 'predicted': "#ff5555", 'error': "#ffb86c",
            'text': "#f0f6fc", 'accent': "#bd93f9"
        }}
        
        # Execute all sections with professional transitions
        self.intro_sequence()
        # ALL section methods here with voiceover synchronization
        self.conclusion_sequence()
    
    # Implement ALL methods with:
    # - with self.voiceover(text="...") as tracker: blocks
    # - Professional scatter plots and regression lines
    # - Color-coded predictions vs actual values  
    # - Progressive concept building
    # - Smooth animations synchronized with speech
    # - Educational clarity and engagement
```

MAKE IT VISUALLY STUNNING AND EDUCATIONALLY POWERFUL WITH PERFECT VOICEOVER SYNC!"""

        return prompt

    def _generate_professional_fallback_with_voiceover(self, sections: List[AnimationSection], 
                                                     available_images: List[str], class_name: str,
                                                     topic_type: str, parsed_data: Dict) -> str:
        """Generate professional fallback code with voiceover integration"""
        
        method_calls = ""
        section_methods = ""
        
        for i, section in enumerate(sections):
            method_calls += f"            self.{section.method_name}()\n"
            
            # Generate topic-specific section method with voiceover
            if topic_type == 'regression':
                section_methods += self._generate_regression_section_with_voiceover(section, i, available_images)
            elif topic_type == 'mathematics':
                section_methods += self._generate_math_section_with_voiceover(section, i, available_images)
            else:
                section_methods += self._generate_general_section_with_voiceover(section, i, available_images)

        return self.professional_base_template.format(
            class_name=class_name,
            method_calls=method_calls,
            section_methods=section_methods
        )

    def _generate_regression_section_with_voiceover(self, section: AnimationSection, index: int, 
                                                  available_images: List[str]) -> str:
        """Generate regression section with synchronized voiceover"""
        
        # Use actual voiceover segments from the parsed section
        voiceover_segments = section.segments if section.segments else [
            type('VoiceoverSegment', (), {'text': f'Let us explore {section.title} through visual analysis'})()
        ]
        
        # Sample data points for demonstration
        data_points = [(1, 2.1), (2, 3.9), (3, 6.1), (4, 7.8), (5, 9.9), (6, 12.2), (7, 13.8), (8, 16.1)]
        
        # Generate voiceover text from segments
        voiceover_texts = [
            segment.text for segment in voiceover_segments[:4]  # Use first 4 segments
        ]
        
        # Fill in default texts if not enough segments
        while len(voiceover_texts) < 4:
            voiceover_texts.extend([
                f"Let's examine {section.title} with professional visualization",
                "We'll see actual data points and their relationship",
                "The regression line shows the best fit through our data",
                "Understanding errors helps us evaluate model performance"
            ])
        
        return f'''
    def {section.method_name}(self):
        """Professional regression visualization: {section.title}"""
        
        # Section header with professional styling
        header = Text("{section.title}", font_size=32, color=self.colors['secondary'])
        header.move_to(self.zones['header'])
        
        with self.voiceover(text="{voiceover_texts[0][:150]}") as tracker:
            self.play(Write(header), run_time=tracker.duration)
        
        # Create professional scatter plot with regression line
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 18, 3],
            x_length=7, y_length=5,
            axis_config={{"color": self.colors['text'], "stroke_width": 2}}
        ).move_to(self.zones['main'] + DOWN * 0.5)
        
        # Axis labels
        x_label = axes.get_x_axis_label("Independent Variable (X)")
        y_label = axes.get_y_axis_label("Dependent Variable (Y)")
        
        # Data points
        data_points = {data_points}
        actual_points = Group()
        predicted_points = Group()
        error_lines = Group()
        
        for x, y in data_points:
            # Actual data point (green)
            actual = Dot(axes.coords_to_point(x, y), color=self.colors['actual'], radius=0.08)
            actual_points.add(actual)
            
            # Predicted point on line (red) 
            y_pred = 1.8 * x + 0.5  # Simple linear relationship
            predicted = Dot(axes.coords_to_point(x, y_pred), color=self.colors['predicted'], radius=0.06)
            predicted_points.add(predicted)
            
            # Error line (orange)
            error_line = Line(
                axes.coords_to_point(x, y), axes.coords_to_point(x, y_pred),
                color=self.colors['error'], stroke_width=2
            )
            error_lines.add(error_line)
        
        # Regression line
        regression_line = axes.plot(lambda x: 1.8 * x + 0.5, color=self.colors['primary'], stroke_width=4)
        
        # Step 1: Introduce the data with voiceover
        with self.voiceover(text="{voiceover_texts[1][:150]}") as tracker:
            self.play(Create(axes), Write(x_label), Write(y_label), run_time=tracker.duration * 0.4)
            
            # Animate points appearing one by one
            for i, point in enumerate(actual_points):
                self.play(GrowFromCenter(point), run_time=tracker.duration * 0.6 / len(actual_points))
        
        # Step 2: Show the regression line with voiceover
        with self.voiceover(text="{voiceover_texts[2][:150]}") as tracker:
            self.play(Create(regression_line), run_time=tracker.duration)
        
        # Step 3: Show predictions with voiceover
        with self.voiceover(text="This line allows us to make predictions - here are the predicted values in red") as tracker:
            for pred_point in predicted_points:
                self.play(GrowFromCenter(pred_point), run_time=tracker.duration / len(predicted_points))
        
        # Step 4: Visualize errors with voiceover
        with self.voiceover(text="{voiceover_texts[3][:150]}") as tracker:
            for error_line in error_lines:
                self.play(Create(error_line), run_time=tracker.duration / len(error_lines))
        
        # Create legend
        legend = Group(
            Group(Dot(color=self.colors['actual'], radius=0.06), Text("Actual Data", font_size=16, color=self.colors['text'])).arrange(RIGHT, buff=0.2),
            Group(Dot(color=self.colors['predicted'], radius=0.06), Text("Predictions", font_size=16, color=self.colors['text'])).arrange(RIGHT, buff=0.2),
            Group(Line(LEFT*0.2, RIGHT*0.2, color=self.colors['error']), Text("Errors", font_size=16, color=self.colors['text'])).arrange(RIGHT, buff=0.2),
            Group(Line(LEFT*0.2, RIGHT*0.2, color=self.colors['primary']), Text("Best Fit Line", font_size=16, color=self.colors['text'])).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        legend_box = SurroundingRectangle(legend, color=self.colors['text'], fill_opacity=0.05, stroke_opacity=0.3)
        legend_group = Group(legend_box, legend).scale(0.8).move_to(self.zones['right'])
        
        with self.voiceover(text="This legend helps us understand each element of our visualization") as tracker:
            self.play(FadeIn(legend_group), run_time=tracker.duration)
        
        self.wait(1)
        
        # Keep everything visible for the next section
        self.persistent_elements.add(header, axes, x_label, y_label, actual_points, 
                                   predicted_points, error_lines, regression_line, legend_group)
        '''

    def _generate_math_section_with_voiceover(self, section: AnimationSection, index: int, 
                                            available_images: List[str]) -> str:
        """Generate mathematics section with synchronized voiceover"""
        
        voiceover_segments = section.segments if section.segments else []
        voiceover_text = voiceover_segments[0].text if voiceover_segments else f"Let's explore the mathematical foundation of {section.title}"
        
        return f'''
    def {section.method_name}(self):
        """Mathematical concept visualization: {section.title}"""
        
        # Section header
        header = Text("{section.title}", font_size=32, color=self.colors['secondary'])
        header.move_to(self.zones['header'])
        
        with self.voiceover(text="{voiceover_text[:150]}") as tracker:
            self.play(Write(header), run_time=tracker.duration)
        
        # Mathematical formula with step-by-step revelation
        formula_parts = [
            "y = mx + b",
            "\\text{{where }} m = \\text{{slope}}",
            "\\text{{and }} b = \\text{{y-intercept}}"
        ]
        
        explanations = [
            "The basic linear equation relates y to x",
            "The slope determines how steep the line is", 
            "The y-intercept is where the line crosses the y-axis"
        ]
        
        current_formula = None
        for i, (part, explanation) in enumerate(zip(formula_parts, explanations)):
            formula = MathTex(part, color=self.colors['text'], font_size=40)
            formula.move_to(self.zones['formula'])
            
            with self.voiceover(text=explanation) as tracker:
                if i == 0:
                    self.play(Write(formula), run_time=tracker.duration)
                else:
                    self.play(Transform(current_formula, formula), run_time=tracker.duration)
                current_formula = formula
        
        # Add visual explanation
        explanation = Text("This equation is the foundation of linear regression", 
                         font_size=20, color=self.colors['muted'])
        explanation.move_to(self.zones['bottom'])
        
        with self.voiceover(text="This mathematical relationship is what we use to make predictions") as tracker:
            self.play(FadeIn(explanation), run_time=tracker.duration)
        
        self.wait(1)
        self.persistent_elements.add(header, current_formula, explanation)
'''

    def _generate_general_section_with_voiceover(self, section: AnimationSection, index: int, 
                                               available_images: List[str]) -> str:
        """Generate general section with synchronized voiceover"""
        
        clean_title = section.title.replace('"', "'")
        voiceover_segments = section.segments if section.segments else []
        
        # Use actual voiceover text if available
        if voiceover_segments:
            main_voiceover = voiceover_segments[0].text
            content_voiceover = voiceover_segments[1].text if len(voiceover_segments) > 1 else "Let's explore this concept through clear explanations and examples"
        else:
            main_voiceover = clean_title
            content_voiceover = "Let's explore this concept through clear explanations and examples"
        
        return f'''
    def {section.method_name}(self):
        """Professional section: {clean_title}"""
        
        # Section header with professional styling
        header = Text("{clean_title}", font_size=32, color=self.colors['secondary'])
        header.move_to(self.zones['header'])
        
        with self.voiceover(text="{main_voiceover[:150]}") as tracker:
            self.play(Write(header), run_time=tracker.duration)
        
        # Main content with voiceover synchronization
        content_lines = [
            "Key concepts and principles",
            "Detailed explanations with examples", 
            "Practical applications and insights"
        ]
        
        content_group = Group()
        for line in content_lines:
            text = Text(line, font_size=20, color=self.colors['text'])
            content_group.add(text)
        
        content_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content_group.move_to(self.zones['main'])
        
        # Animate content with voiceover
        with self.voiceover(text="{content_voiceover[:150]}") as tracker:
            for line in content_group:
                self.play(FadeIn(line), run_time=tracker.duration / len(content_group))
        
        self.wait(1)
        self.persistent_elements.add(header, content_group)
        '''

    def _analyze_topic_type(self, narrative_script: str) -> str:
        """Analyze the type of topic to determine appropriate visualization strategy"""
        script_lower = narrative_script.lower()
        
        # Define topic patterns
        topic_patterns = {
            'regression': ['regression', 'linear regression', 'predict', 'correlation', 'best fit'],
            'mathematics': ['equation', 'formula', 'theorem', 'proof', 'derivative', 'integral'],
            'statistics': ['probability', 'distribution', 'mean', 'variance', 'standard deviation'],
            'data_science': ['data', 'machine learning', 'model', 'training', 'features'],
            'physics': ['force', 'energy', 'motion', 'wave', 'particle'],
            'chemistry': ['molecule', 'atom', 'reaction', 'bond'],
            'biology': ['cell', 'dna', 'evolution', 'organism'],
            'computer_science': ['algorithm', 'programming', 'software', 'computer']
        }
        
        # Score each topic type
        topic_scores = {}
        for topic_type, keywords in topic_patterns.items():
            score = sum(1 for keyword in keywords if keyword in script_lower)
            if score > 0:
                topic_scores[topic_type] = score
        
        # Return the highest scoring topic type
        if topic_scores:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        else:
            return 'general'

    def _create_professional_prompt(self, sections: List[AnimationSection], 
                                  available_images: List[str], class_name: str,
                                  topic_type: str, complexity_analysis: Optional[Dict] = None) -> str:
        """Create professional prompt with topic-specific visualization instructions"""
        
        # Topic-specific visualization instructions
        viz_instructions = self._get_topic_visualization_instructions(topic_type)
        
        prompt = f"""Generate PROFESSIONAL educational Manim code with ADVANCED VISUALIZATIONS.

CRITICAL REQUIREMENTS:
- Class: {class_name}(VoiceoverScene) 
- Create STUNNING, EDUCATIONAL animations like 3Blue1Brown quality
- Use ADVANCED visual techniques: scatter plots, regression lines, error visualization
- PROGRESSIVE revelation - build understanding step by step
- Keep ALL relevant elements visible - DON'T erase previous content unnecessarily
- Use color coding for different concepts (actual vs predicted, etc.)
- Include SMOOTH animations and transitions
- ⚠️ CRITICAL: Ensure all text and animations are arranged so there is no overlap between any objects, using appropriate positioning methods like .arrange(), .next_to(), and .shift(). All elements must be clearly readable and not cover each other at any point in the animation.

TOPIC TYPE DETECTED: {topic_type.upper()}
{viz_instructions}

SECTIONS TO IMPLEMENT ({len(sections)} total):
"""
        
        # Add section details
        for i, section in enumerate(sections, 1):
            content_preview = section.segments[0].text[:200] if section.segments else "No content"
            prompt += f"""
Section {i}: {section.title}
Method: {section.method_name}()
Content: {len(section.segments)} segments
Preview: {content_preview}...
"""

        # Add professional code structure requirements
        prompt += f"""
GENERATE COMPLETE, PROFESSIONAL MANIM CODE:

```python
import gc
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np

class {class_name}(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#0d1117"
        
        # Professional color scheme with semantic meaning
        self.colors = {{
            'primary': "#58a6ff", 'secondary': "#ffa657", 'success': "#56d364",
            'actual': "#50fa7b", 'predicted': "#ff5555", 'error': "#ffb86c",
            'text': "#f0f6fc", 'accent': "#bd93f9"
        }}
        
        # Execute all sections with professional transitions
        self.intro_sequence()
        # ALL section methods here with advanced visualizations
        self.conclusion_sequence()
    
    # Implement ALL methods with:
    # - Professional scatter plots and regression lines
    # - Color-coded predictions vs actual values  
    # - Progressive concept building
    # - Smooth animations and transitions
    # - Educational clarity and engagement
```

MAKE IT VISUALLY STUNNING AND EDUCATIONALLY POWERFUL!"""

        return prompt

    def _get_topic_visualization_instructions(self, topic_type: str) -> str:
        """Get topic-specific visualization instructions"""
        instructions = {
            'regression': """
REGRESSION-SPECIFIC VISUALIZATIONS:
- Create professional scatter plots with actual data points
- Animate the "best fit" line being drawn
- Show predicted values as different colored points
- Draw error lines between actual and predicted values
- Use color coding: Green=Actual, Red=Predicted, Orange=Errors
- Animate the concept of minimizing errors
- Show the regression equation being built step by step
- Include R-squared visualization if relevant
""",
            
            'mathematics': """
MATHEMATICS-SPECIFIC VISUALIZATIONS:  
- Step-by-step formula derivations with highlighting
- Geometric interpretations where applicable
- Function graphs and transformations
- Interactive coordinate systems
- Color-coded mathematical components
- Progressive equation building
""",
            
            'statistics': """
STATISTICS-SPECIFIC VISUALIZATIONS:
- Probability distributions with animations
- Histogram transformations
- Central tendency visualizations
- Variance and standard deviation graphics
- Interactive data exploration
""",
            
            'data_science': """
DATA SCIENCE-SPECIFIC VISUALIZATIONS:
- Data pipeline animations
- Model training visualizations
- Feature importance displays
- Decision boundary animations
- Performance metric graphics
""",
            
            'general': """
GENERAL EDUCATIONAL VISUALIZATIONS:
- Concept relationship diagrams
- Process flow animations
- Comparative visualizations
- Progressive information revelation
- Interactive demonstrations
"""
        }
        
        return instructions.get(topic_type, instructions['general'])

    def _generate_professional_fallback(self, sections: List[AnimationSection], 
                                      available_images: List[str], class_name: str,
                                      topic_type: str) -> str:
        """Generate professional fallback code with topic-specific elements"""
        
        method_calls = ""
        section_methods = ""
        
        for i, section in enumerate(sections):
            method_calls += f"            self.{section.method_name}()\n"
            
            # Generate topic-specific section method
            if topic_type == 'regression':
                section_methods += self._generate_regression_section(section, i, available_images)
            elif topic_type == 'mathematics':
                section_methods += self._generate_math_section(section, i, available_images)
            else:
                section_methods += self._generate_general_section(section, i, available_images)

        return self.professional_base_template.format(
            class_name=class_name,
            method_calls=method_calls,
            section_methods=section_methods
        )

    def _generate_regression_section(self, section: AnimationSection, index: int, 
                                   available_images: List[str]) -> str:
        """Generate regression-specific section with professional visualizations"""
        
        # Sample data points for demonstration
        data_points = [(1, 2.1), (2, 3.9), (3, 6.1), (4, 7.8), (5, 9.9), (6, 12.2), (7, 13.8), (8, 16.1)]
        
        return f'''
    def {section.method_name}(self):
        """Professional regression visualization: {section.title}"""
        
        # Section header with professional styling
        header = Text("{section.title}", font_size=32, color=self.colors['secondary'])
        header.move_to(self.zones['header'])
        
        with self.voiceover(text="{section.title} - let's explore this concept visually") as tracker:
            self.play(Write(header), run_time=tracker.duration)
        
        # Create professional scatter plot with regression line
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 18, 3],
            x_length=7, y_length=5,
            axis_config={{"color": self.colors['text'], "stroke_width": 2}}
        ).move_to(self.zones['main'] + DOWN * 0.5)
        
        # Axis labels
        x_label = axes.get_x_axis_label("Independent Variable (X)")
        y_label = axes.get_y_axis_label("Dependent Variable (Y)")
        
        # Data points
        data_points = {data_points}
        actual_points = Group()
        predicted_points = Group()
        error_lines = Group()
        
        for x, y in data_points:
            # Actual data point (green)
            actual = Dot(axes.coords_to_point(x, y), color=self.colors['actual'], radius=0.08)
            actual_points.add(actual)
            
            # Predicted point on line (red) 
            y_pred = 1.8 * x + 0.5  # Simple linear relationship
            predicted = Dot(axes.coords_to_point(x, y_pred), color=self.colors['predicted'], radius=0.06)
            predicted_points.add(predicted)
            
            # Error line (orange)
            error_line = Line(
                axes.coords_to_point(x, y), axes.coords_to_point(x, y_pred),
                color=self.colors['error'], stroke_width=2
            )
            error_lines.add(error_line)
        
        # Regression line
        regression_line = axes.plot(lambda x: 1.8 * x + 0.5, color=self.colors['primary'], stroke_width=4)
        
        # Step 1: Introduce the data
        with self.voiceover(text="Let's start by examining our actual data points - these represent real observations") as tracker:
            self.play(Create(axes), Write(x_label), Write(y_label), run_time=tracker.duration * 0.4)
            
            # Animate points appearing one by one
            for i, point in enumerate(actual_points):
                self.play(GrowFromCenter(point), run_time=tracker.duration * 0.6 / len(actual_points))
        
        # Step 2: Show the regression line
        with self.voiceover(text="Now we'll find the best fitting line that represents the relationship in our data") as tracker:
            self.play(Create(regression_line), run_time=tracker.duration)
        
        # Step 3: Show predictions
        with self.voiceover(text="This line allows us to make predictions - here are the predicted values in red") as tracker:
            for pred_point in predicted_points:
                self.play(GrowFromCenter(pred_point), run_time=tracker.duration / len(predicted_points))
        
        # Step 4: Visualize errors
        with self.voiceover(text="The orange lines show the difference between actual and predicted values - these are our errors") as tracker:
            for error_line in error_lines:
                self.play(Create(error_line), run_time=tracker.duration / len(error_lines))
        
        # Create legend
        legend = Group(
            Group(Dot(color=self.colors['actual'], radius=0.06), Text("Actual Data", font_size=16, color=self.colors['text'])).arrange(RIGHT, buff=0.2),
            Group(Dot(color=self.colors['predicted'], radius=0.06), Text("Predictions", font_size=16, color=self.colors['text'])).arrange(RIGHT, buff=0.2),
            Group(Line(LEFT*0.2, RIGHT*0.2, color=self.colors['error']), Text("Errors", font_size=16, color=self.colors['text'])).arrange(RIGHT, buff=0.2),
            Group(Line(LEFT*0.2, RIGHT*0.2, color=self.colors['primary']), Text("Best Fit Line", font_size=16, color=self.colors['text'])).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        legend_box = SurroundingRectangle(legend, color=self.colors['text'], fill_opacity=0.05, stroke_opacity=0.3)
        legend_group = Group(legend_box, legend).scale(0.8).move_to(self.zones['right'])
        
        with self.voiceover(text="This legend helps us understand each element of our visualization") as tracker:
            self.play(FadeIn(legend_group), run_time=tracker.duration)
        
        self.wait(1)
        
        # Keep everything visible for the next section
        self.persistent_elements.add(header, axes, x_label, y_label, actual_points, 
                                   predicted_points, error_lines, regression_line, legend_group)
        '''

    def _generate_math_section(self, section: AnimationSection, index: int, 
                             available_images: List[str]) -> str:
        """Generate mathematics-specific section with formula animations"""
        
        return f'''
    def {section.method_name}(self):
        """Mathematical concept visualization: {section.title}"""
        
        # Clear previous content but keep persistent elements
        self.clear_non_persistent()
        
        # Section header
        header = Text("{section.title}", font_size=32, color=self.colors['secondary'])
        header.move_to(self.zones['header'])
        
        with self.voiceover(text="Let's explore the mathematical foundation of {section.title}") as tracker:
            self.play(Write(header), run_time=tracker.duration)
        
        # Mathematical formula with step-by-step revelation
        formula_parts = [
            "y = mx + b",
            "\\text{{where }} m = \\text{{slope}}",
            "\\text{{and }} b = \\text{{y-intercept}}"
        ]
        
        current_formula = None
        for i, part in enumerate(formula_parts):
            formula = MathTex(part, color=self.colors['text'], font_size=40)
            formula.move_to(self.zones['formula'])
            
            explanation_text = [
                "The basic linear equation relates y to x",
                "The slope determines how steep the line is",
                "The y-intercept is where the line crosses the y-axis"
            ][i]
            
            with self.voiceover(text=explanation_text) as tracker:
                if i == 0:
                    self.play(Write(formula), run_time=tracker.duration)
                else:
                    self.play(Transform(current_formula, formula), run_time=tracker.duration)
                current_formula = formula
        
        # Add visual explanation
        explanation = Text("This equation is the foundation of linear regression", 
                         font_size=20, color=self.colors['muted'])
        explanation.move_to(self.zones['bottom'])
        
        with self.voiceover(text="This mathematical relationship is what we use to make predictions") as tracker:
            self.play(FadeIn(explanation), run_time=tracker.duration)
        
        self.wait(1)
        self.persistent_elements.add(header, current_formula, explanation)
'''

    def _generate_general_section(self, section: AnimationSection, index: int, 
                                available_images: List[str]) -> str:
        """Generate general section with professional styling"""
        
        clean_title = section.title.replace('"', "'")
        content_text = section.segments[0].text[:150] if section.segments else "Key concept explanation"
        clean_content = content_text.replace('"', "'")
        
        return f'''
    def {section.method_name}(self):
        """Professional section: {clean_title}"""
        
        # Clear previous non-persistent content
        self.clear_non_persistent()
        
        # Section header with professional styling
        header = Text("{clean_title}", font_size=32, color=self.colors['secondary'])
        header.move_to(self.zones['header'])
        
        with self.voiceover(text="{clean_title}") as tracker:
            self.play(Write(header), run_time=tracker.duration)
        
        # Main content with proper positioning
        content_lines = [
            "{clean_content[:60]}",
            "{clean_content[60:120] if len(clean_content) > 60 else 'Additional insights and explanations'}",
            "Key takeaways and practical applications"
        ]
        
        content_group = Group()
        for i, line in enumerate(content_lines):
            text = Text(line, font_size=20, color=self.colors['text'])
            content_group.add(text)
        
        content_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        content_group.move_to(self.zones['main'])
        
        # Animate content appearance
        with self.voiceover(text="Let's explore this concept through clear explanations and examples") as tracker:
            for line in content_group:
                self.play(FadeIn(line), run_time=tracker.duration / len(content_group))
        
        # Add visual element if image available
        if {index} < len({str(available_images)}) and {str(available_images)}:
            image_path = {str(available_images)}[{index}]
            visual = self.load_image_safe(image_path, scale=0.4, position=self.zones['right'])
            
            with self.voiceover(text="This visual representation helps illustrate the concept") as tracker:
                self.play(FadeIn(visual), run_time=tracker.duration)
                self.persistent_elements.add(visual)
        
        self.wait(1)
        self.persistent_elements.add(header, content_group)
'''

    def _enhance_code_for_topic(self, code: str, topic_type: str) -> str:
        """Enhance code based on topic type"""
        if topic_type == 'regression':
            # Add regression-specific enhancements
            if 'clear_non_persistent' not in code:
                code = code.replace(
                    'def cleanup_scene(self):',
                    'def clear_non_persistent(self):\n        """Clear non-persistent elements while keeping important context"""\n        # Implementation would selectively clear content\n        pass\n    \n    def cleanup_scene(self):'
                )
        
        return code

    def _validate_professional_code(self, code: str, class_name: str) -> str:
        """Validate and ensure professional code quality"""
        # Ensure required imports
        required_imports = [
            'import gc',
            'from manim import *',
            'from manim_voiceover import VoiceoverScene',
            'from manim_voiceover.services.gtts import GTTSService',
            'import numpy as np'
        ]
        
        for imp in required_imports:
            if imp not in code:
                code = imp + '\n' + code
        
        # Ensure proper class definition
        if f'class {class_name}(VoiceoverScene):' not in code:
            code = re.sub(r'class\s+\w+.*VoiceoverScene.*:', f'class {class_name}(VoiceoverScene):', code)
        
        # Ensure essential setup
        essential_setup = [
            'self.set_speech_service(GTTSService())',
            'self.camera.background_color = "#0d1117"',
            'self.colors = {'
        ]
        
        for setup in essential_setup:
            if setup not in code:
                construct_match = re.search(r'def construct\(self\):\s*', code)
                if construct_match:
                    insertion_point = construct_match.end()
                    code = code[:insertion_point] + f'\n        {setup}\n        ' + code[insertion_point:]
        
        return code

    def _get_available_images(self, images_folder: str) -> List[str]:
        """Get available image files"""
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
        
        return images[:5]  # Limit to prevent token overflow

    def _generate_class_name(self, topic: str) -> str:
        """Generate clean class name"""
        clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
        words = clean_topic.split()
        
        if words:
            class_name = ''.join(word.capitalize() for word in words[:2])
            if not class_name.endswith('Animation'):
                class_name += "Animation"
        else:
            class_name = "ProfessionalAnimation"
        
        return class_name

    def _extract_and_clean_code(self, generated_text: str) -> str:
        """Extract and clean Python code from response"""
        # Remove markdown code blocks
        code_block_pattern = r'```(?:python)?\s*(.*?)```'
        code_match = re.search(code_block_pattern, generated_text, re.DOTALL)
        
        if code_match:
            return code_match.group(1).strip()
        
        # Look for class definition start
        class_pattern = r'(import.*|from manim import.*|class\s+\w+.*VoiceoverScene)'
        class_match = re.search(class_pattern, generated_text, re.DOTALL)
        
        if class_match:
            return generated_text[class_match.start():].strip()
        
        return generated_text.strip()


# Test function
if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set GOOGLE_API_KEY environment variable")
        exit(1)
    
    generator = EnhancedManimCodeGenerator(api_key)
    
    # Test with regression example
    sample_narrative = '''
## Introduction to Linear Regression
Linear regression is a fundamental statistical method used to model relationships between variables. It helps us understand how one variable affects another.

## Understanding the Relationship  
When we have data points, we want to find the best line that represents the relationship. This line minimizes the distance between predicted and actual values.

## Mathematical Foundation
The linear regression equation is y = mx + b, where m is the slope and b is the y-intercept. This simple equation allows us to make predictions.

## Practical Applications
Linear regression is used in economics, finance, marketing, and many other fields to make data-driven decisions and predictions.
'''
    
    print("Testing professional code generation...")
    generated_code = generator.generate_enhanced_manim_code(sample_narrative)
    
    print("\n" + "="*50)
    print("GENERATED PROFESSIONAL CODE PREVIEW:")
    print("="*50)
    print(generated_code[:2000] + "\n... (preview)")
    print("="*50)
    print("Professional code generation test completed!")
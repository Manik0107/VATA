#!/usr/bin/env python3
"""
DSPy-Enhanced Educational Manim Code Generator
Complete workflow for document-grounded animation generation
Compatible with DSPy 2.5+, Google GenAI 1.19+, and Manim 0.19+
"""

import os
import json
import time
import dspy
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
OVERALL_MANIM_CODE_GUIDELINES = Path("prompts/prompt1.txt").read_text(encoding="utf-8")

# =============================================================================
# DSPy SIGNATURES - Define Input/Output Contracts
# =============================================================================

class DocumentExtractionSignature(dspy.Signature):
    """Extract structured educational content from a document."""
    # Input: Raw document content and topic query
    document_content = dspy.InputField(desc="Full text content of the educational document")
    topic_query = dspy.InputField(desc="Specific topic/concept to extract from document")
    
    # Outputs: Structured extraction results
    extracted_formulas = dspy.OutputField(desc="All mathematical formulas exactly as they appear in the document")
    step_by_step_explanations = dspy.OutputField(desc="Detailed explanations from the document in order")
    visual_descriptions = dspy.OutputField(desc="Descriptions of graphs, diagrams, visual elements from document")
    key_concepts = dspy.OutputField(desc="Main concepts and definitions from the document")
    derivations = dspy.OutputField(desc="Mathematical derivations and proofs exactly as shown in document")

class EducationalPlanSignature(dspy.Signature):
    """Create comprehensive, detailed teaching plan with specific learning objectives and pedagogical strategies."""
    
    topic = dspy.InputField(desc="Main topic to be taught")
    extracted_content = dspy.InputField(desc="Rich prompt with structured content from document and guidelines")
    
    # Detailed teaching plan outputs
    teaching_sequence = dspy.OutputField(desc="Comprehensive step-by-step teaching progression with 8-12 detailed learning stages. Each stage should include: specific learning objectives, key concepts to cover, pedagogical approach, examples to use, common misconceptions to address, and assessment methods. Format as numbered list with detailed sub-points.")
    explanation_breakdown = dspy.OutputField(desc="Detailed pedagogical breakdown for each concept explaining HOW to teach it effectively. Include: cognitive load management, scaffolding techniques, analogies and metaphors, visual aids needed, interactive elements, and differentiation strategies for different learning styles. Minimum 300 words with specific teaching strategies.")
    prerequisite_concepts = dspy.OutputField(desc="Comprehensive hierarchical map of ALL prerequisite concepts with clear dependency relationships. Include: foundational mathematical concepts, prior knowledge assumptions, conceptual building blocks, and suggested pre-assessment questions. Format as structured outline.")
    visual_requirements = dspy.OutputField(desc="Detailed specifications for EACH visual element needed including: specific Manim animations, mathematical visualizations, interactive demonstrations, 3D models, graphs, diagrams, color schemes, and multimedia integration. Include timing and transition requirements for each visual component.")

# Enhanced DSPy Signatures for Gap Detection and Concept Explanation
class ConceptGapAnalyzer(dspy.Signature):
    """Analyze educational content to automatically identify unexplained technical terms that need clarification."""
    
    content = dspy.InputField(desc="Educational content including formulas, explanations, and main topic discussion")
    context = dspy.InputField(desc="Learning context and target audience level")
    
    technical_terms = dspy.OutputField(desc="List of technical terms mentioned without sufficient explanation")
    prerequisite_concepts = dspy.OutputField(desc="Essential concepts that must be explained before the main topic")
    explanation_gaps = dspy.OutputField(desc="Specific knowledge gaps that would prevent complete understanding")
    concept_dependencies = dspy.OutputField(desc="Dependency mapping showing which concepts must be explained first")

class ConceptExplanationGenerator(dspy.Signature):
    """Generate comprehensive explanations for prerequisite concepts with visual demonstrations."""
    
    concept = dspy.InputField(desc="Technical concept that needs explanation")
    context = dspy.InputField(desc="Context where this concept will be used in the main topic")
    audience_level = dspy.InputField(desc="Target audience knowledge level")
    
    explanation_text = dspy.OutputField(desc="Clear, step-by-step explanation building from basics")
    visual_demonstration = dspy.OutputField(desc="Detailed visual breakdown showing how the concept works")
    interactive_elements = dspy.OutputField(desc="Interactive components to reinforce concept understanding")
    connection_to_main_topic = dspy.OutputField(desc="Clear connection explaining why this concept is needed for the main topic")

class AnimationStoryboardSignature(dspy.Signature):
    """Generate comprehensive cinematic storyboard for educational Manim animations with detailed scene breakdowns."""
    
    teaching_plan = dspy.InputField(desc="Comprehensive teaching plan with learning objectives and content breakdown")
    content = dspy.InputField(desc="Formatted content including prerequisites and main topic information")
    prerequisite_explanations = dspy.InputField(desc="JSON-formatted prerequisite concept explanations")
    
    # Storyboard outputs with proper cinematic elements
    concept_introduction_sequence = dspy.OutputField(desc="Detailed sequence for introducing prerequisite concepts with specific animations and visuals")
    cinematic_arc = dspy.OutputField(desc="Complete storytelling arc with hook, rising action, climax, and resolution")
    scenes = dspy.OutputField(desc="Scene-by-scene breakdown with specific Manim animations, timing, and visual elements")
    visuals = dspy.OutputField(desc="Detailed visual specifications including Manim objects, colors, and animation techniques")
    timing = dspy.OutputField(desc="Professional timing specifications for each scene with transitions")
    narration = dspy.OutputField(desc="Engaging voice-over script synchronized with animations")
    interactive_elements = dspy.OutputField(desc="Interactive components with setup and teardown specifications")
    engagement_techniques = dspy.OutputField(desc="Advanced engagement methods and visual metaphors")
    animation_lifecycle = dspy.OutputField(desc="Complete animation lifecycle management for each element")

class ManimCodeSignature(dspy.Signature):
    """Generate sophisticated, educational Manim code with rich visualizations and animations from storyboard specifications."""
    # Input: Animation specifications
    storyboard = dspy.InputField(desc="Detailed animation storyboard and specifications")
    class_name = dspy.InputField(desc="Name for the Manim scene class")
    
    # Output: Advanced Manim code
    manim_code = dspy.OutputField(desc="Complete, runnable Python Manim code with sophisticated animations, mathematical visualizations, interactive elements, neural network diagrams, step-by-step concept building, smooth transitions, and engaging visual storytelling")
    code_explanation = dspy.OutputField(desc="Comprehensive explanation of the generated code including animation techniques, educational design principles, visual hierarchy, and cognitive engagement strategies")

class EnhancedNarrationSignature(dspy.Signature):
    """Generate actual educational narration with precise visual synchronization."""
    
    topic = dspy.InputField(desc="Educational topic to narrate")
    teaching_content = dspy.InputField(desc="Structured teaching content to be narrated")
    
    actual_narration_script = dspy.OutputField(desc="Complete spoken narration script with natural, educational language explaining concepts clearly. No meta-descriptions, only actual words to be spoken.")
    visual_synchronization = dspy.OutputField(desc="Precise timing marks showing when each visual element should appear during narration")
    engagement_techniques = dspy.OutputField(desc="Specific rhetorical questions, analogies, and emphasis techniques used in narration")

class DetailedStoryboardSignature(dspy.Signature):
    """Create comprehensive visual storyboard with minute animation details."""
    
    concept = dspy.InputField(desc="Specific concept requiring detailed visual treatment")
    educational_context = dspy.InputField(desc="Learning objectives and pedagogical requirements")
    
    scene_composition = dspy.OutputField(desc="Exact visual layout, object positioning, color schemes, and composition details")
    animation_specifications = dspy.OutputField(desc="Precise Manim animations with timing, parameters, and sequencing")
    visual_storytelling = dspy.OutputField(desc="Progressive visual narrative that supports learning objectives")


# =============================================================================
# DSPy MODULES - Implement the Workflow Stages
# =============================================================================

class DocumentGroundedExtractor(dspy.Module):
    """Enhanced extractor that identifies content gaps and generates prerequisite explanations."""
    
    def __init__(self):
        super().__init__()
        # Use ChainOfThought for step-by-step extraction reasoning
        self.extractor = dspy.ChainOfThought(DocumentExtractionSignature)
        self.gap_analyzer = dspy.ChainOfThought(ConceptGapAnalyzer)
        self.concept_explainer = dspy.ChainOfThought(ConceptExplanationGenerator)
        
    def forward(self, document_path: str, topic: str) -> Dict[str, Any]:
        """
        Extract structured content from document for a specific topic.
        
        Args:
            document_path: Path to the educational document
            topic: Specific concept/topic to extract
            
        Returns:
            Dictionary containing extracted structured content
        """
        # Read document content
        try:
            if document_path.lower().endswith('.pdf'):
                document_content = self._extract_pdf_with_gemini(document_path)
            else:
                with open(document_path, 'r', encoding='utf-8') as f:
                    document_content = f.read()
        except Exception as e:
            raise ValueError(f"Could not read document: {e}")
        
        # Use DSPy module to extract structured content
        extraction_result = self.extractor(
            document_content=document_content,
            topic_query=topic
        )
        
        # Analyze for concept gaps and unexplained terms
        print("🔍 Analyzing content for knowledge gaps...")
        combined_content = f"""
        Topic: {topic}
        
        Key Concepts: {extraction_result.key_concepts}
        
        Explanations: {extraction_result.step_by_step_explanations}
        
        Formulas: {extraction_result.extracted_formulas}
        """
        
        gap_analysis = self.gap_analyzer(
            content=combined_content,
            context="Educational animation for students learning neural networks and deep learning concepts"
        )
        
        # Generate comprehensive explanations for prerequisite concepts
        print("📚 Generating prerequisite concept explanations...")
        prerequisite_explanations = {}
        
        if gap_analysis.prerequisite_concepts:
            # Parse prerequisite concepts (handle both string and list formats)
            concepts_text = gap_analysis.prerequisite_concepts
            if isinstance(concepts_text, str):
                # Split by common delimiters and clean
                concepts_list = [c.strip() for c in concepts_text.replace('\n', ',').split(',') if c.strip()]
            else:
                concepts_list = [str(concepts_text)]
            
            for concept in concepts_list[:5]:  # Limit to top 5 concepts to avoid token limits
                if concept and len(concept.strip()) > 2:
                    try:
                        print(f"  📖 Explaining: {concept}")
                        concept_explanation = self._retry_with_backoff(
                            lambda: self.concept_explainer(
                                concept=concept.strip(),
                                context=f"Prerequisite for understanding {topic} in neural networks",
                                audience_level="Intermediate students with basic calculus knowledge"
                            )
                        )
                        
                        prerequisite_explanations[concept.strip()] = {
                            "explanation": concept_explanation.explanation_text,
                            "visual_demo": concept_explanation.visual_demonstration,
                            "interactive": concept_explanation.interactive_elements,
                            "connection": concept_explanation.connection_to_main_topic
                        }
                    except Exception as e:
                        print(f"  ⚠️ Could not explain {concept}: {e}")
                        continue
        
        return {
            "formulas": extraction_result.extracted_formulas,
            "explanations": extraction_result.step_by_step_explanations,
            "visuals": extraction_result.visual_descriptions,
            "concepts": extraction_result.key_concepts,
            "derivations": extraction_result.derivations,
            "source_document": document_path,
            # Enhanced gap analysis results
            "technical_terms": gap_analysis.technical_terms,
            "prerequisite_concepts": gap_analysis.prerequisite_concepts,
            "explanation_gaps": gap_analysis.explanation_gaps,
            "concept_dependencies": gap_analysis.concept_dependencies,
            "prerequisite_explanations": prerequisite_explanations
        }
    
    def _retry_with_backoff(self, func, max_retries=3, base_delay=1):
        """Retry function with exponential backoff for rate limiting."""
        import time
        import random
        
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                error_message = str(e).lower()
                
                # Check if it's a rate limit error
                if "rate limit" in error_message or "429" in error_message or "quota" in error_message:
                    if attempt < max_retries - 1:
                        # Extract retry delay from error if available
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        
                        # Try to extract the suggested delay from error message
                        import re
                        retry_match = re.search(r'retry in (\d+(?:\.\d+)?)s', error_message)
                        if retry_match:
                            suggested_delay = float(retry_match.group(1))
                            delay = max(delay, suggested_delay)
                        
                        print(f"  ⏳ Rate limit hit. Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                        continue
                    else:
                        print(f"  ❌ Max retries exceeded for rate limiting")
                        raise e
                else:
                    # Non-rate-limit error, don't retry
                    raise e
        
        return None
    
    def _extract_pdf_with_gemini(self, pdf_path: str) -> str:
        """Use Gemini to extract text from PDF directly."""
        api_key =  os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        client = genai.Client(api_key=api_key)
        
        # Read PDF as bytes
        pdf_bytes = Path(pdf_path).read_bytes()
        
        # Use Gemini for PDF text extraction
        prompt = """Extract all text content from this PDF document. 
        Preserve all mathematical formulas, equations, and formatting.
        Keep the logical structure and order of information intact."""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type='application/pdf',
                ),
                prompt
            ],
            config=types.GenerateContentConfig(temperature=0.1)
        )
        
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            raise ValueError("Failed to extract text from PDF")

class EducationalPlanner(dspy.Module):
    """Create comprehensive teaching plans from extracted content."""
    
    def __init__(self):
        super().__init__()
        # Use ChainOfThought for systematic planning
        self.planner = dspy.ChainOfThought(EducationalPlanSignature)
        
    def forward(self, topic: str, extracted_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comprehensive structured teaching plan from extracted document content.
        
        Args:
            topic: Topic to create plan for
            extracted_content: Content extracted from document with prerequisites
            
        Returns:
            Dictionary containing detailed teaching plan
        """
        # Create comprehensive educational planning prompt
        prompt_template = f"""
You are an expert educational designer creating a comprehensive teaching plan for advanced Manim animations.

TOPIC: {topic}

EXTRACTED CONTENT:
{self._format_extracted_content(extracted_content)}

PREREQUISITE CONCEPTS IDENTIFIED:
{extracted_content.get('prerequisite_concepts', 'None identified')}

EXPLANATION GAPS TO ADDRESS:
{extracted_content.get('explanation_gaps', 'None identified')}

EDUCATIONAL DESIGN REQUIREMENTS:

1. TEACHING SEQUENCE (8-12 detailed stages):
Create a comprehensive learning progression that:
- Starts with foundational concepts and builds systematically
- Addresses each prerequisite concept before moving to advanced topics
- Includes specific learning objectives for each stage
- Incorporates active learning techniques and engagement strategies
- Provides multiple examples and non-examples
- Addresses common misconceptions at each stage
- Includes formative assessment checkpoints

2. EXPLANATION BREAKDOWN (detailed pedagogical strategies):
For each concept, specify:
- Cognitive load management techniques
- Scaffolding approaches (worked examples → guided practice → independent practice)
- Multiple representation strategies (verbal, visual, symbolic, kinesthetic)
- Analogies and metaphors that connect to student prior knowledge
- Interactive elements that promote active engagement
- Differentiation strategies for different learning styles
- Error analysis and misconception addressing

3. PREREQUISITE CONCEPTS (comprehensive dependency map):
Create detailed hierarchical structure including:
- Mathematical foundations required
- Conceptual building blocks with explicit connections
- Prior knowledge assumptions with verification strategies
- Learning pathway dependencies
- Suggested diagnostic assessments

4. VISUAL REQUIREMENTS (specific Manim specifications):
For each teaching stage, specify:
- Exact Manim animations needed (Create, Write, Transform, etc.)
- Mathematical visualizations (3D plots, function graphs, geometric constructions)
- Interactive demonstrations with parameter controls
- Color coding and visual hierarchy principles
- Animation timing and pacing for cognitive processing
- Screen layout and information organization
- Transition effects between concepts

Create a professional, research-based teaching plan that ensures deep conceptual understanding.
"""
        
        # Generate comprehensive teaching plan with retry logic
        try:
            plan_result = self._retry_with_backoff(
                lambda: self.planner(
                    topic=topic,
                    extracted_content=prompt_template
                )
            )
        except Exception as e:
            print(f"❌ Failed to generate teaching plan: {e}")
            # Return minimal fallback plan
            plan_result = type('obj', (object,), {
                'teaching_sequence': f"Basic introduction to {topic}",
                'explanation_breakdown': f"Explain {topic} concepts step by step",
                'prerequisite_concepts': "Basic mathematical concepts",
                'visual_requirements': f"Simple animations for {topic}"
            })()
        
        # Generate enhanced visual specifications
        enhanced_visuals = self._create_enhanced_visual_specifications(topic, extracted_content)
        
        return {
            "sequence": plan_result.teaching_sequence,
            "breakdown": plan_result.explanation_breakdown,
            "prerequisites": plan_result.prerequisite_concepts,
            "visual_needs": plan_result.visual_requirements,
            "enhanced_visual_specs": enhanced_visuals,  # Integrated enhancement
            "source_content": extracted_content
        }
    
    def _create_enhanced_visual_specifications(self, topic: str, content: Dict[str, Any]) -> str:
        """Generate detailed visual specifications for each teaching concept."""
        
        visual_specs = f"""
ENHANCED VISUAL SPECIFICATIONS FOR: {topic}

For each concept in the teaching sequence, specify:

1. SCENE COMPOSITION:
- Background color and style
- Main visual elements positioning
- Text placement and hierarchy
- Visual flow direction

2. ANIMATION DETAILS:
- Object creation order and timing
- Movement patterns and trajectories  
- Color transitions and effects
- Interactive element specifications

3. EDUCATIONAL DESIGN PRINCIPLES:
- Visual chunking of information
- Progressive disclosure techniques
- Attention-directing elements
- Memory reinforcement visuals

4. MANIM IMPLEMENTATION SPECS:
- Exact class names and parameters
- Animation sequences with timing
- Color schemes using Manim constants
- Scene management and cleanup

Based on extracted content: {content.get('concepts', 'General concepts')}

DETAILED REQUIREMENTS:
- Prerequisites to visualize: {content.get('prerequisite_concepts', 'None')}
- Key formulas to animate: {content.get('formulas', 'None')}
- Visual descriptions from document: {content.get('visuals', 'None')}
- Step-by-step explanations to illustrate: {content.get('explanations', 'None')}

COGNITIVE LOAD CONSIDERATIONS:
- Maximum 3-4 visual elements on screen simultaneously
- Use progressive disclosure for complex concepts
- Implement clear visual hierarchy with color coding
- Include transition pauses for mental processing

ACCESSIBILITY REQUIREMENTS:
- High contrast color schemes
- Clear typography with adequate sizing
- Alternative text descriptions for screen readers
- Keyboard navigation support for interactive elements

ENGAGEMENT TECHNIQUES:
- Interactive hover effects on key elements
- Progressive revelation of information
- Visual metaphors connecting abstract concepts to concrete examples
- Gamification elements where appropriate

TECHNICAL SPECIFICATIONS:
- Resolution: 1920x1080 (16:9 aspect ratio)
- Frame rate: 60fps for smooth animations
- Color palette: Use Manim's color constants for consistency
- Animation duration: 2-4 seconds per major transition
- Text sizing: Large enough for mobile viewing
"""
        return visual_specs
    
    def _format_extracted_content(self, content: Dict[str, Any]) -> str:
        """Format extracted content for the planner."""
        formatted = f"""
EXTRACTED CONTENT:

Key Concepts: {content.get('concepts', 'No concepts extracted')}

Formulas: {content.get('formulas', 'No formulas found')}

Step-by-step Explanations: {content.get('explanations', 'No explanations found')}

Visual Descriptions: {content.get('visuals', 'No visual descriptions found')}

Mathematical Derivations: {content.get('derivations', 'No derivations found')}

Technical Terms Identified: {content.get('technical_terms', 'None identified')}

Prerequisite Explanations Available: {len(content.get('prerequisite_explanations', {}))} concepts explained

Source Document: {content.get('source_document', 'Unknown source')}
"""
        return formatted.strip()
    
    def _retry_with_backoff(self, func, max_retries=3, base_delay=1):
        """Retry function with exponential backoff for rate limiting."""
        import time
        import random
        
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                error_message = str(e).lower()
                
                # Check if it's a rate limit error
                if "rate limit" in error_message or "429" in error_message or "quota" in error_message:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        
                        # Try to extract the suggested delay from error message
                        import re
                        retry_match = re.search(r'retry in (\d+(?:\.\d+)?)s', error_message)
                        if retry_match:
                            suggested_delay = float(retry_match.group(1))
                            delay = max(delay, suggested_delay)
                        
                        print(f"  ⏳ Rate limit hit. Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                        continue
                    else:
                        print(f"  ❌ Max retries exceeded for rate limiting")
                        raise e
                else:
                    raise e
        
        return None

class AnimationDesigner(dspy.Module):
    """Convert teaching plans into cinematic Manim animation storyboards."""
    
    def __init__(self):
        super().__init__()
        # Use ChainOfThought for cinematic animation planning
        self.designer = dspy.ChainOfThought(AnimationStoryboardSignature)
        
    def forward(self, topic: str, teaching_plan: Dict[str, Any], detailed_storyboard: bool = False) -> Dict[str, Any]:
        """
        Create cinematic animation storyboard with integrated prerequisite concept explanations.
        
        Args:
            topic: Animation topic
            teaching_plan: Structured teaching plan with prerequisite explanations
            
        Returns:
            Dictionary containing cinematic animation specifications
        """
        # Extract prerequisite explanations if available
        prerequisite_info = ""
        if "prerequisite_explanations" in teaching_plan.get("source_content", {}):
            prereqs = teaching_plan["source_content"]["prerequisite_explanations"]
            if prereqs:
                prerequisite_info = f"""
                
PREREQUISITE CONCEPTS TO EXPLAIN FIRST:
{json.dumps(prereqs, indent=2)}

CRITICAL: You MUST create concept introduction scenes for each prerequisite BEFORE the main topic.
Each prerequisite concept needs its own dedicated scene with:
- Clear explanation from basics
- Visual demonstration 
- Connection to why it's needed for the main topic
"""
        
        # Create comprehensive storyboard generation prompt
        prompt_template = f"""
You are creating educational narration scripts for Manim animations explaining: {topic}

TEACHING CONTENT TO NARRATE:
{self._format_teaching_plan(teaching_plan)}

NARRATION REQUIREMENTS:

1. ACTUAL EDUCATIONAL NARRATION (NOT meta-descriptions):
- Write the exact words to be spoken during the animation
- Use conversational, engaging language that explains concepts clearly
- Include strategic pauses marked with [PAUSE] for visual emphasis
- Ask rhetorical questions to maintain engagement
- Use analogies and examples to clarify complex concepts

2. DETAILED VISUAL STORYBOARD with minute specifications:
- Exact Manim object specifications (Circle(radius=0.5, color=BLUE))
- Precise positioning coordinates
- Animation timing in seconds
- Color schemes with specific Manim color constants
- Camera movements and zoom specifications
- Scene transitions and effects

3. SYNCHRONIZATION BETWEEN NARRATION AND VISUALS:
- Mark exactly when visual elements should appear during speech
- Specify animation duration to match narration pace
- Include timing cues for visual emphasis

EXAMPLE FORMAT:
Narration: "Neural networks are like digital brains [PAUSE] that learn from data."
Visual: Circle(color=BLUE) appears at ORIGIN, followed by arrows connecting to smaller circles
Timing: 3 seconds for narration, 2 seconds for visual buildup

Create comprehensive narration and visual specifications for: {topic}
"""
        if detailed_storyboard:
            detailed_visual_specs = self._create_detailed_visual_storyboard(teaching_plan)
            prompt_template += f"\n\nDETAILED VISUAL SPECIFICATIONS:\n{detailed_visual_specs}"
        # Prepare prerequisite explanations for storyboard generation
        prerequisite_explanations_formatted = ""
        if teaching_plan.get("source_content", {}).get("prerequisite_explanations"):
            prereqs = teaching_plan["source_content"]["prerequisite_explanations"]
            prerequisite_explanations_formatted = json.dumps(prereqs, indent=2)
        
        # Generate cinematic storyboard with prerequisite integration
        storyboard_result = self.designer(
            teaching_plan=prompt_template,
            content=self._format_teaching_plan(teaching_plan),
            prerequisite_explanations=prerequisite_explanations_formatted
        )
        
        return {
            "concept_introduction_sequence": storyboard_result.concept_introduction_sequence,
            "cinematic_arc": storyboard_result.cinematic_arc,
            "scenes": storyboard_result.scenes,
            "visuals": storyboard_result.visuals,
            "timing": storyboard_result.timing,
            "narration": storyboard_result.narration,
            "interactive_elements": storyboard_result.interactive_elements,
            "engagement_techniques": storyboard_result.engagement_techniques,
            "animation_lifecycle": storyboard_result.animation_lifecycle,
            "source_plan": teaching_plan
        }
    
    def _create_detailed_visual_storyboard(self, teaching_plan: Dict[str, Any]) -> str:
        """Create minute-detail visual storyboard for each teaching concept."""
        
        detailed_storyboard = f"""
    DETAILED VISUAL STORYBOARD WITH MINUTE SPECIFICATIONS:

    Based on the teaching sequence: {teaching_plan['sequence']}

    For each concept in the teaching plan, create:

    1. EXACT VISUAL SPECIFICATIONS:
    - Camera angles and movements (zoom levels, panning directions)
    - Object positioning with coordinates
    - Color schemes with hex codes
    - Animation timing in seconds
    - Visual metaphors and analogies
    - Interactive elements placement

    2. SCENE-BY-SCENE BREAKDOWN:
    - Opening frame composition
    - Element introduction order
    - Transition effects between concepts
    - Visual emphasis techniques (highlighting, pulsing, etc.)
    - Text placement and typography specifications

    3. ANIMATION LIFECYCLE FOR EACH ELEMENT:
    - Entrance animations (FadeIn timing, Create duration)
    - On-screen behavior (Indicate effects, Transform sequences)
    - Exit animations (FadeOut timing, cleanup specifications)

    4. EDUCATIONAL ENGAGEMENT TECHNIQUES:
    - Visual hooks to maintain attention
    - Progressive disclosure of information
    - Visual reinforcement of key concepts
    - Memory aids through visual associations

    Create specific storyboard for: {teaching_plan.get('visual_needs', 'General educational content')}
    """
        return detailed_storyboard
    
    def _format_teaching_plan(self, plan: Dict[str, Any]) -> str:
        """Format teaching plan for animation design."""
        formatted = f"""
        TEACHING PLAN:
        
        Teaching Sequence: {plan['sequence']}
        
        Explanation Breakdown: {plan['breakdown']}
        
        Prerequisites: {plan['prerequisites']}
        
        Visual Requirements: {plan['visual_needs']}
        """
        return formatted.strip()

class EnhancedNarrationGenerator(dspy.Module):
    """Generate actual educational narration with visual synchronization."""
    
    def __init__(self):
        super().__init__()
        self.narrator = dspy.ChainOfThought(EnhancedNarrationSignature)
        
    def forward(self, topic: str, teaching_content: str) -> Dict[str, Any]:
        """Generate synchronized narration and visuals."""
        narration_result = self.narrator(
            topic=topic,
            teaching_content=teaching_content
        )
        
        return {
            "narration_script": narration_result.actual_narration_script,
            "visual_sync": narration_result.visual_synchronization,
            "engagement": narration_result.engagement_techniques
        }

class DetailedStoryboardGenerator(dspy.Module):
    """Generate minute-detail visual storyboards."""
    
    def __init__(self):
        super().__init__()
        self.storyboard_generator = dspy.ChainOfThought(DetailedStoryboardSignature)
        
    def forward(self, concept: str, context: str) -> Dict[str, Any]:
        """Generate detailed visual specifications."""
        storyboard_result = self.storyboard_generator(
            concept=concept,
            educational_context=context
        )
        
        return {
            "scene_composition": storyboard_result.scene_composition,
            "animation_specs": storyboard_result.animation_specifications,
            "visual_story": storyboard_result.visual_storytelling
        }

class ManimCodeGenerator(dspy.Module):
    """Generate complete, modern, and pedagogically rich Manim code with proper animation lifecycle and automatic comprehensive labeling."""
    
    def __init__(self):
        super().__init__()
        # Setup DSPy chain of thought with Gemini and sensible parameters
        self.generator = dspy.ChainOfThought(ManimCodeSignature)
        
        # Universal Labeling System - automatically integrated into all animations
        self.universal_labeling_system = """
# =============================================
# UNIVERSAL LABELING SYSTEM
# =============================================
# Automatic comprehensive labeling for all educational animations

class UniversalLabelingSystem:
    \"\"\"
    Universal educational labeling system for any topic.
    Automatically creates professional labels for neural networks, mathematical functions,
    coordinates, states, components, and all visual elements.
    \"\"\"
    
    def __init__(self, scene):
        self.scene = scene
        self.label_group = VGroup()
        
    def create_smart_label(self, obj, text, direction=UP, buff=0.3, color=WHITE, font_size=24):
        \"\"\"Create intelligent contextual labels for any object.\"\"\"
        label = Text(text, font_size=font_size, color=color)
        
        # Use numpy array comparison safely for direction constants
        if np.array_equal(direction, UP):
            label.next_to(obj, UP, buff=buff)
        elif np.array_equal(direction, DOWN):
            label.next_to(obj, DOWN, buff=buff)
        elif np.array_equal(direction, LEFT):
            label.next_to(obj, LEFT, buff=buff)
        elif np.array_equal(direction, RIGHT):
            label.next_to(obj, RIGHT, buff=buff)
        else:
            label.next_to(obj, direction, buff=buff)
            
        self.label_group.add(label)
        return label
    
    def create_coordinate_label(self, point, text, color=YELLOW):
        \"\"\"Label coordinate points and mathematical locations.\"\"\"
        coord_dot = Dot(point, color=color)
        coord_label = Text(text, font_size=20, color=color).next_to(coord_dot, UR, buff=0.1)
        
        coord_group = VGroup(coord_dot, coord_label)
        self.label_group.add(coord_group)
        return coord_group
    
    def create_component_labels(self, objects_dict, colors_dict=None):
        \"\"\"Label multiple components with consistent styling.\"\"\"
        labels = VGroup()
        
        for name, obj in objects_dict.items():
            color = colors_dict.get(name, WHITE) if colors_dict else WHITE
            
            # Determine smart positioning based on object type
            if hasattr(obj, 'get_center'):
                # For mathematical objects, label above
                if isinstance(obj, (MathTex, Tex)):
                    direction = UP
                # For shapes, label to the right
                elif isinstance(obj, (Circle, Rectangle, Square)):
                    direction = RIGHT
                # For arrows and lines, label above
                elif isinstance(obj, (Arrow, Line)):
                    direction = UP
                # Default positioning
                else:
                    direction = UP
            else:
                direction = UP
                
            label = self.create_smart_label(obj, name, direction=direction, color=color)
            labels.add(label)
        
        return labels
    
    def create_math_annotation(self, formula_obj, explanation, side=RIGHT):
        \"\"\"Add mathematical annotations and explanations.\"\"\"
        annotation = Text(explanation, font_size=18, color=BLUE).next_to(formula_obj, side, buff=0.5)
        
        # Add connecting line
        if side == RIGHT:
            connection = Line(formula_obj.get_right(), annotation.get_left(), color=BLUE, stroke_width=1)
        else:
            connection = Line(formula_obj.get_left(), annotation.get_right(), color=BLUE, stroke_width=1)
        
        annotation_group = VGroup(annotation, connection)
        self.label_group.add(annotation_group)
        return annotation_group
    
    def create_state_indicator(self, obj, state_text, color=GREEN):
        \"\"\"Create state indicators for process animations.\"\"\"
        indicator = Text(f"State: {state_text}", font_size=16, color=color)
        indicator.to_corner(UL)
        
        self.label_group.add(indicator)
        return indicator
    
    def create_neural_network_labels(self, neurons, layer_names, weights=None):
        \"\"\"Specialized labeling for neural network components.\"\"\"
        nn_labels = VGroup()
        
        # Label neuron layers
        for i, layer in enumerate(neurons):
            layer_name = layer_names[i] if i < len(layer_names) else f"Layer {i+1}"
            
            # Layer title
            layer_title = Text(layer_name, font_size=20, color=YELLOW)
            layer_title.next_to(layer, UP, buff=0.5)
            nn_labels.add(layer_title)
            
            # Individual neuron labels
            for j, neuron in enumerate(layer):
                neuron_label = Text(f"N{i+1}.{j+1}", font_size=12, color=WHITE)
                neuron_label.next_to(neuron, DOWN, buff=0.1)
                nn_labels.add(neuron_label)
        
        # Label weights if provided
        if weights:
            for i, weight_group in enumerate(weights):
                weight_label = Text(f"W{i+1}", font_size=14, color=ORANGE)
                weight_label.next_to(weight_group, UP, buff=0.2)
                nn_labels.add(weight_label)
        
        self.label_group.add(nn_labels)
        return nn_labels
    
    def create_function_comparison_labels(self, functions_dict):
        \"\"\"Label multiple functions for comparison.\"\"\"
        comparison_labels = VGroup()
        
        for name, func_obj in functions_dict.items():
            # Function name
            func_label = Text(name, font_size=18, color=BLUE, weight=BOLD)
            func_label.next_to(func_obj, UP, buff=0.3)
            
            # Add to group
            comparison_labels.add(func_label)
        
        self.label_group.add(comparison_labels)
        return comparison_labels
    
    def animate_labels_in(self):
        \"\"\"Animate all labels appearing.\"\"\"
        if len(self.label_group) > 0:
            return FadeIn(self.label_group, lag_ratio=0.1)
        return None
    
    def animate_labels_out(self):
        \"\"\"Animate all labels disappearing.\"\"\"
        if len(self.label_group) > 0:
            return FadeOut(self.label_group, lag_ratio=0.1)
        return None
    
    def clear_labels(self):
        \"\"\"Clear all labels from the scene.\"\"\"
        self.label_group.clear()

# =============================================
# END UNIVERSAL LABELING SYSTEM
# =============================================
"""
        
    def forward(self, storyboard: dict, class_name: str = "EducationalAnimation") -> dict:
        # Compose final prompt by prepending overall guideline prompt
        prompt_template = f"""
{OVERALL_MANIM_CODE_GUIDELINES}

{self.universal_labeling_system}

UNIVERSAL LABELING SYSTEM REQUIREMENTS - MUST BE IMPLEMENTED:
- MANDATORY: Include the UniversalLabelingSystem class at the top of your generated code
- MANDATORY: Initialize labeling system in __init__ or construct(): self.labeler = UniversalLabelingSystem(self)
- MANDATORY: Use comprehensive labeling for ALL visual elements:
  * Label ALL mathematical functions with create_function_comparison_labels()
  * Label ALL coordinate points with create_coordinate_label()
  * Label ALL neural network components with create_neural_network_labels()
  * Label ALL diagram components with create_component_labels()
  * Add mathematical annotations with create_math_annotation()
  * Show process states with create_state_indicator()

LABELING IMPLEMENTATION PATTERN:
```python
class {class_name}(Scene):
    def __init__(self):
        super().__init__()
        self.labeler = UniversalLabelingSystem(self)
    
    def scene_example(self):
        # Create objects
        relu_eq = MathTex("f(x) = max(0, x)")
        leaky_relu_eq = MathTex("f(x) = max(αx, x)")
        
        # MANDATORY: Label everything
        func_labels = self.labeler.create_function_comparison_labels({{
            "ReLU Function": relu_eq,
            "Leaky ReLU Function": leaky_relu_eq
        }})
        
        # Add mathematical annotations
        relu_annotation = self.labeler.create_math_annotation(
            relu_eq, "Zero for negative values", side=RIGHT
        )
        
        # Show animations with labels
        self.play(Write(relu_eq), Write(leaky_relu_eq))
        self.play(self.labeler.animate_labels_in())
        self.play(Create(relu_annotation))
```

ANIMATION LIFECYCLE REQUIREMENTS:
- Every animation element must follow: ENTRANCE → EXPLANATION → CLEANUP → EXIT
- Use proper Manim animations: FadeIn, Create, Write for entrances
- Use FadeOut, Uncreate, Unwrite for exits  
- Clear screen between major sections with self.clear() or selective removal
- No elements should linger indefinitely on screen
- Smooth transitions between scenes with proper timing
- ALWAYS animate labels in/out with self.labeler.animate_labels_in() and self.labeler.animate_labels_out()

COMPREHENSIVE LABELING CHECKLIST - VERIFY ALL ARE INCLUDED:
✓ Mathematical equations labeled with function names
✓ Coordinate points labeled with values
✓ Neural network layers labeled with names and neuron IDs
✓ Graph axes labeled with units and scales
✓ Comparison elements clearly distinguished
✓ Process states indicated throughout animation
✓ Annotations explaining key concepts
✓ Component relationships made explicit

Cinematic Animation Storyboard for topic '{class_name}':
{self._format_storyboard(storyboard)}

Generate the full runnable Manim v0.19+ Python code with complete animation lifecycle management AND mandatory comprehensive labeling using the UniversalLabelingSystem.
Ensure every element has proper entrance, explanation time, exit animations, AND professional labeling throughout.
"""
        # Run the DSPy generator chain with this prompt
        code_result = self.generator(
            storyboard=prompt_template,
            class_name=class_name
        )
        return {
            "manim_code": code_result.manim_code,
            "code_explanation": code_result.code_explanation,
            "class_name": class_name,
            "storyboard": storyboard
        }
    
    def _format_storyboard(self, storyboard: dict) -> str:
        """Format complete storyboard with ALL specifications including enhanced features for code generation"""
        
        formatted_storyboard = f"""
COMPLETE STORYBOARD FOR CODE GENERATION:

DETAILED SCENE DESCRIPTIONS:
{storyboard.get("scenes", "")}

TIMING SPECIFICATIONS: 
{storyboard.get("timing", "")}

NARRATION SCRIPTS:
{storyboard.get("narration", "")}

VISUAL SPECIFICATIONS:
{storyboard.get("visuals", "")}

ANIMATION LIFECYCLE:
{storyboard.get("animation_lifecycle", "")}

ENGAGEMENT TECHNIQUES:
{storyboard.get("engagement_techniques", "")}

INTERACTIVE ELEMENTS:
{storyboard.get("interactive_elements", "")}

CINEMATIC ARC:
{storyboard.get("cinematic_arc", "")}

CONCEPT INTRODUCTION SEQUENCE:
{storyboard.get("concept_introduction_sequence", "")}"""

        # Add enhanced features if available
        if storyboard.get("enhanced_narration_script"):
            formatted_storyboard += f"""

ENHANCED NARRATION SCRIPT:
{storyboard.get("enhanced_narration_script", "")}

VISUAL SYNCHRONIZATION:
{storyboard.get("visual_synchronization", "")}"""

        if storyboard.get("detailed_scene_composition"):
            formatted_storyboard += f"""

DETAILED SCENE COMPOSITION:
{storyboard.get("detailed_scene_composition", "")}

DETAILED ANIMATION SPECIFICATIONS:
{storyboard.get("detailed_animation_specs", "")}

DETAILED VISUAL STORYTELLING:
{storyboard.get("detailed_visual_story", "")}"""

        formatted_storyboard += f"""

CRITICAL INSTRUCTIONS FOR CODE GENERATION:
1. Implement EVERY scene exactly as specified above
2. Use the provided narration scripts but REMOVE all [PAUSE] markers to prevent TTS issues
3. Follow the exact timing specifications provided
4. Include all visual elements and animations described
5. Use enhanced narration and detailed specifications when available
6. Create professional 3D animations, neural network diagrams, and comparison tables as specified
7. Do NOT create generic animations - implement the specific scenes described with sophisticated visual elements
"""
        return formatted_storyboard
# =============================================================================
# MAIN DSPy PIPELINE - Orchestrates the Complete Workflow
# =============================================================================

class DSPyManipWorkflow(dspy.Module):
    """Complete DSPy-powered workflow for document-grounded Manim animation generation."""
    
    def __init__(self, api_key: str):
        super().__init__()
        
        self.api_key = api_key
        # Initialize DSPy modules
        self.extractor = DocumentGroundedExtractor()
        self.planner = EducationalPlanner()
        self.designer = AnimationDesigner()
        self.narrator = EnhancedNarrationGenerator()
        self.detailed_storyboard = DetailedStoryboardGenerator()
        self.generator = ManimCodeGenerator()
        
        self._setup_dspy_lm()
        
    def _setup_dspy_lm(self):
        import os
        os.environ['GEMINI_API_KEY'] = self.api_key
        
        # Try different models in order of preference
        models_to_try = [
            "gemini/gemini-2.5-flash",  # More stable with higher limits
            # "gemini/gemini-2.0-flash-exp",  # Experimental version
            # "gemini/gemini-1.5-pro",  # Backup option
            # "gemini/gemini-2.0-flash"  # Original fallback
        ]
        
        for model in models_to_try:
            try:
                print(f"🔄 Trying model: {model}")
                lm = dspy.LM(
                    model=model,
                    api_key=self.api_key,
                    max_tokens=60000,  # Reduced to be more conservative
                    temperature=0.1,
                    top_p=0.9
                )
                dspy.settings.configure(lm=lm)
                print(f"✅ Successfully configured model: {model}")
                return
            except Exception as e:
                print(f"❌ Failed to configure {model}: {e}")
                continue
        
        raise ValueError("Could not configure any Gemini model. Check your API key and quotas.")

        
    def forward(self, document_path: str, topic: str, class_name: str = None, enhanced_narration: bool = False, detailed_storyboard: bool = False) -> Dict[str, Any]:
        print("Starting DSPy-powered document analysis...")
        
        # Stage 1: Extract content from document
        print("Extracting content from document...")
        extracted_content = self.extractor(document_path, topic)
        
        # Stage 2: Create educational plan
        print("Creating educational plan...")
        teaching_plan = self.planner(topic, extracted_content)
        
        # Stage 3: Design animation storyboard
        print("Designing animation storyboard...")
        storyboard = self.designer(topic, teaching_plan, detailed_storyboard)
        
        # Stage 4: Generate enhanced features BEFORE code generation
        enhanced_narration_result = None
        if enhanced_narration:
            print("Generating enhanced narration...")
            teaching_content_formatted = f"""
            Teaching Plan: {teaching_plan['sequence']}
            Key Concepts: {teaching_plan['breakdown']}
            """
            enhanced_narration_result = self.narrator(topic, teaching_content_formatted)

        detailed_storyboard_result = None
        if detailed_storyboard:
            print("Creating detailed visual storyboard...")
            detailed_storyboard_result = self.detailed_storyboard(
                concept=topic,
                context=teaching_plan['visual_needs']
            )
        
        # Stage 5: Merge enhanced features into storyboard
        if enhanced_narration_result or detailed_storyboard_result:
            print("Integrating enhanced features into storyboard...")
            storyboard = self._merge_enhanced_features(storyboard, enhanced_narration_result, detailed_storyboard_result)
        
        # Stage 6: Generate Manim code with enhanced storyboard
        print("Generating Manim code...")
        final_class_name = class_name or self._generate_class_name(topic)
        generated_code = self.generator(storyboard, final_class_name)
        
        # Compile final results
        results = {
            "success": True,
            "topic": topic,
            "document_source": document_path,
            "extracted_content": extracted_content,
            "teaching_plan": teaching_plan,
            "storyboard": storyboard,
            "enhanced_narration": enhanced_narration_result,
            "detailed_storyboard": detailed_storyboard_result,
            "generated_code": generated_code,
            "class_name": final_class_name,
            "timestamp": time.time()
        }
        
        print("DSPy workflow completed successfully!")
        return results
    
    def _merge_enhanced_features(self, storyboard: dict, enhanced_narration: dict = None, detailed_storyboard: dict = None) -> dict:
        """Merge enhanced narration and detailed storyboard features into the main storyboard."""
        
        # Start with the original storyboard
        merged_storyboard = storyboard.copy()
        
        # Merge enhanced narration if available
        if enhanced_narration:
            # Replace or enhance existing narration with the enhanced version
            merged_storyboard["enhanced_narration_script"] = enhanced_narration.get("narration_script", "")
            merged_storyboard["visual_synchronization"] = enhanced_narration.get("visual_sync", "")
            merged_storyboard["engagement_techniques"] = enhanced_narration.get("engagement", "")
            
            # Update the main narration field with enhanced version
            if enhanced_narration.get("narration_script"):
                merged_storyboard["narration"] = enhanced_narration["narration_script"]
        
        # Merge detailed storyboard if available
        if detailed_storyboard:
            # Add detailed visual specifications
            merged_storyboard["detailed_scene_composition"] = detailed_storyboard.get("scene_composition", "")
            merged_storyboard["detailed_animation_specs"] = detailed_storyboard.get("animation_specs", "")
            merged_storyboard["detailed_visual_story"] = detailed_storyboard.get("visual_story", "")
            
            # Enhance existing visual specifications
            if detailed_storyboard.get("scene_composition"):
                original_visuals = merged_storyboard.get("visuals", "")
                merged_storyboard["visuals"] = f"{original_visuals}\n\nDETAILED SPECIFICATIONS:\n{detailed_storyboard['scene_composition']}"
        
        return merged_storyboard
    
    def _generate_class_name(self, topic: str) -> str:
        """Generate a clean class name from topic."""
        import re
        clean_topic = re.sub(r'[^a-zA-Z0-9\\s]', '', topic)
        words = clean_topic.split()
        class_name = ''.join(word.capitalize() for word in words[:3])
        return f"{class_name}Animation" if class_name else "EducationalAnimation"
    
    def save_code(self, results: Dict[str, Any], output_path: str) -> str:
        metadata = f'''"""
    Class: {results["class_name"]}
    Topic: {results["topic"]}
    Run: manim {output_path} {results["class_name"]} -pql
    """
    '''

        generated_code = results["generated_code"].get("manim_code") or "# CODE GENERATION FAILED"
        final_code = metadata + "\n\n" + generated_code

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_code)
        print(f"💾 Saved code to: {output_path}")
        return output_path
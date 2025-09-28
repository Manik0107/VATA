#!/usr/bin/env python3
"""
Advanced Educational Script Generator with Deep Content Analysis
Compatible with Google GenAI SDK 1.19.0+ (2025)
Generates world-class, comprehensive educational narratives
"""

import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional, List, Tuple, Any
from dotenv import load_dotenv
import math

# Updated Google GenAI SDK imports
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

class ContentAnalyzer:
    """Advanced content analysis for deep educational understanding"""
    
    def __init__(self):
        self.analysis_categories = {
            'concepts': [],
            'formulas': [],
            'examples': [],
            'applications': [],
            'prerequisites': [],
            'difficulty_level': 'medium',
            'visual_elements': [],
            'mathematical_depth': 'basic',
            'interdisciplinary_connections': []
        }
    
    def deep_analyze_content(self, query: str, markdown_content: str, metadata: Dict) -> Dict:
        """Perform comprehensive content analysis"""
        print("🔍 Performing deep content analysis...")
        
        analysis = {
            'topic_taxonomy': self._analyze_topic_taxonomy(query),
            'content_structure': self._analyze_content_structure(markdown_content),
            'mathematical_complexity': self._analyze_mathematical_complexity(markdown_content),
            'prerequisite_knowledge': self._identify_prerequisites(query, markdown_content),
            'learning_objectives': self._extract_learning_objectives(query, markdown_content),
            'visual_opportunities': self._identify_visual_opportunities(markdown_content, metadata),
            'depth_levels': self._map_explanation_depths(query, markdown_content),
            'conceptual_connections': self._find_conceptual_connections(markdown_content),
            'pedagogical_approach': self._determine_pedagogical_approach(query, markdown_content),
            'content_gaps': self._identify_content_gaps(query, markdown_content)
        }
        
        print(f"✅ Analysis complete: {len(analysis)} dimensions analyzed")
        return analysis
    
    def _analyze_topic_taxonomy(self, query: str) -> Dict:
        """Analyze the educational taxonomy of the topic"""
        query_lower = query.lower()
        
        # Educational levels
        levels = {
            'elementary': ['basic', 'simple', 'introduction', 'beginner'],
            'intermediate': ['understand', 'explain', 'analyze', 'compare'],
            'advanced': ['derive', 'prove', 'synthesize', 'evaluate', 'optimize']
        }
        
        # Subject domains
        domains = {
            'mathematics': ['math', 'equation', 'formula', 'calculate', 'algebra', 'calculus', 'geometry'],
            'physics': ['force', 'energy', 'motion', 'wave', 'particle', 'quantum', 'relativity'],
            'chemistry': ['molecule', 'atom', 'reaction', 'bond', 'organic', 'inorganic'],
            'biology': ['cell', 'dna', 'evolution', 'organism', 'ecology', 'genetics'],
            'computer_science': ['algorithm', 'data structure', 'programming', 'software', 'ai', 'ml'],
            'engineering': ['design', 'system', 'optimization', 'control', 'signal'],
            'statistics': ['data', 'probability', 'distribution', 'regression', 'analysis']
        }
        
        # Cognitive processes (Bloom's taxonomy)
        cognitive_levels = {
            'remember': ['define', 'list', 'recall', 'identify'],
            'understand': ['explain', 'describe', 'interpret', 'summarize'],
            'apply': ['use', 'demonstrate', 'calculate', 'solve'],
            'analyze': ['compare', 'contrast', 'examine', 'break down'],
            'evaluate': ['assess', 'critique', 'justify', 'argue'],
            'create': ['design', 'construct', 'develop', 'formulate']
        }
        
        # Determine classifications
        educational_level = 'intermediate'  # default
        subject_domain = 'general'
        cognitive_level = 'understand'  # default
        
        for level, keywords in levels.items():
            if any(keyword in query_lower for keyword in keywords):
                educational_level = level
                break
        
        for domain, keywords in domains.items():
            if any(keyword in query_lower for keyword in keywords):
                subject_domain = domain
                break
        
        for level, keywords in cognitive_levels.items():
            if any(keyword in query_lower for keyword in keywords):
                cognitive_level = level
                break
        
        return {
            'educational_level': educational_level,
            'subject_domain': subject_domain,
            'cognitive_level': cognitive_level,
            'complexity_score': self._calculate_complexity_score(educational_level, cognitive_level)
        }
    
    def _analyze_content_structure(self, content: str) -> Dict:
        """Analyze the structure and organization of content"""
        lines = content.split('\n')
        
        structure = {
            'headers': [],
            'formulas': [],
            'code_blocks': [],
            'lists': [],
            'tables': [],
            'content_density': 0,
            'organization_quality': 'good'
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                structure['headers'].append(line)
            elif '$$' in line or line.startswith('$'):
                structure['formulas'].append(line)
            elif line.startswith('```'):
                structure['code_blocks'].append(line)
            elif line.startswith('- ') or line.startswith('* '):
                structure['lists'].append(line)
            elif '|' in line and line.count('|') > 2:
                structure['tables'].append(line)
        
        # Calculate content density
        total_chars = len(content)
        meaningful_chars = len(re.sub(r'\s+', ' ', content).strip())
        structure['content_density'] = meaningful_chars / max(total_chars, 1)
        
        # Assess organization quality
        if len(structure['headers']) > 0:
            structure['organization_quality'] = 'excellent'
        elif len(structure['lists']) > 2:
            structure['organization_quality'] = 'good'
        else:
            structure['organization_quality'] = 'needs_improvement'
        
        return structure
    
    def _analyze_mathematical_complexity(self, content: str) -> Dict:
        """Analyze mathematical complexity and requirements"""
        math_indicators = {
            'basic_arithmetic': ['+', '-', '*', '/', '='],
            'algebra': ['x', 'y', 'z', 'variable', 'equation'],
            'calculus': ['derivative', 'integral', 'limit', 'dx', 'dy'],
            'linear_algebra': ['matrix', 'vector', 'eigenvalue', 'determinant'],
            'statistics': ['mean', 'variance', 'probability', 'distribution'],
            'advanced': ['theorem', 'proof', 'lemma', 'corollary']
        }
        
        complexity_scores = {
            'basic_arithmetic': 1,
            'algebra': 2,
            'statistics': 3,
            'calculus': 4,
            'linear_algebra': 4,
            'advanced': 5
        }
        
        detected_areas = []
        max_complexity = 0
        
        content_lower = content.lower()
        for area, keywords in math_indicators.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_areas.append(area)
                max_complexity = max(max_complexity, complexity_scores[area])
        
        # Count mathematical expressions
        math_expressions = len(re.findall(r'\$.*?\$|\\\(.*?\\\)|\\\[.*?\\\]', content))
        
        return {
            'complexity_level': max_complexity,
            'mathematical_areas': detected_areas,
            'expression_count': math_expressions,
            'requires_visualization': max_complexity >= 2
        }
    
    def _identify_prerequisites(self, query: str, content: str) -> List[str]:
        """Identify prerequisite knowledge for the topic"""
        prerequisite_map = {
            'calculus': ['algebra', 'functions', 'limits'],
            'linear algebra': ['algebra', 'vectors', 'matrices'],
            'machine learning': ['statistics', 'linear algebra', 'calculus', 'programming'],
            'differential equations': ['calculus', 'algebra'],
            'quantum mechanics': ['physics', 'calculus', 'linear algebra'],
            'statistics': ['probability', 'algebra'],
            'neural networks': ['machine learning', 'calculus', 'programming'],
            'optimization': ['calculus', 'linear algebra'],
            'regression': ['statistics', 'algebra'],
            'geometry': ['algebra', 'trigonometry']
        }
        
        query_lower = query.lower()
        prerequisites = []
        
        for topic, prereqs in prerequisite_map.items():
            if topic in query_lower:
                prerequisites.extend(prereqs)
        
        # Add content-based prerequisites
        content_lower = content.lower()
        if 'derivative' in content_lower:
            prerequisites.append('calculus basics')
        if 'matrix' in content_lower:
            prerequisites.append('linear algebra')
        if 'probability' in content_lower:
            prerequisites.append('probability theory')
        
        return list(set(prerequisites))  # Remove duplicates
    
    def _extract_learning_objectives(self, query: str, content: str) -> List[str]:
        """Extract and generate comprehensive learning objectives"""
        objectives = []
        
        # Verb mapping for Bloom's taxonomy
        objective_verbs = {
            'remember': ['define', 'identify', 'recall', 'list'],
            'understand': ['explain', 'describe', 'interpret', 'summarize'],
            'apply': ['calculate', 'solve', 'demonstrate', 'use'],
            'analyze': ['compare', 'examine', 'break down', 'investigate'],
            'evaluate': ['assess', 'critique', 'justify', 'defend'],
            'create': ['design', 'construct', 'formulate', 'develop']
        }
        
        # Extract key concepts from content
        concepts = self._extract_key_concepts(content)
        
        # Generate objectives based on query analysis
        if 'explain' in query.lower() or 'understand' in query.lower():
            objectives.append(f"Understand the fundamental principles of {self._extract_main_topic(query)}")
            objectives.append(f"Explain how {self._extract_main_topic(query)} works in practice")
        
        if 'calculate' in query.lower() or 'solve' in query.lower():
            objectives.append(f"Apply mathematical techniques to solve {self._extract_main_topic(query)} problems")
        
        # Add concept-specific objectives
        for concept in concepts[:3]:  # Top 3 concepts
            objectives.append(f"Analyze the role of {concept} in the broader context")
        
        if not objectives:  # Default objectives
            main_topic = self._extract_main_topic(query)
            objectives = [
                f"Understand the core concepts of {main_topic}",
                f"Apply {main_topic} principles to solve problems",
                f"Analyze real-world applications of {main_topic}"
            ]
        
        return objectives
    
    def _identify_visual_opportunities(self, content: str, metadata: Dict) -> List[Dict]:
        """Identify opportunities for visual representations"""
        visual_ops = []
        
        # From metadata images
        if 'images' in metadata and isinstance(metadata['images'], list):
            for img in metadata['images']:
                visual_ops.append({
                    'type': 'image',
                    'source': img.get('image_name', ''),
                    'context': img.get('context_type', ''),
                    'description': img.get('description', ''),
                    'timing': 'context_dependent'
                })
        
        # From content analysis
        content_lower = content.lower()
        
        # Graphs and plots
        if any(word in content_lower for word in ['graph', 'plot', 'chart', 'curve']):
            visual_ops.append({
                'type': 'graph',
                'purpose': 'data_visualization',
                'timing': 'during_explanation'
            })
        
        # Mathematical formulas
        if re.search(r'\$.*?\$|\\\(.*?\\\)', content):
            visual_ops.append({
                'type': 'formula_animation',
                'purpose': 'step_by_step_derivation',
                'timing': 'during_mathematical_explanation'
            })
        
        # Geometric shapes
        if any(word in content_lower for word in ['circle', 'rectangle', 'triangle', 'polygon', 'sphere', 'cube']):
            visual_ops.append({
                'type': 'geometric_animation',
                'purpose': 'shape_demonstration',
                'timing': 'during_geometric_explanation'
            })
        
        # Process diagrams
        if any(word in content_lower for word in ['algorithm', 'process', 'step', 'procedure']):
            visual_ops.append({
                'type': 'process_diagram',
                'purpose': 'workflow_illustration',
                'timing': 'during_process_explanation'
            })
        
        return visual_ops
    
    def _map_explanation_depths(self, query: str, content: str) -> Dict:
        """Map different depth levels for explanations"""
        return {
            'surface_level': {
                'description': 'Basic definition and overview',
                'duration': '30-45 seconds',
                'approach': 'intuitive_understanding'
            },
            'intermediate_level': {
                'description': 'Detailed explanation with examples',
                'duration': '90-120 seconds', 
                'approach': 'conceptual_understanding'
            },
            'deep_level': {
                'description': 'Mathematical derivations and proofs',
                'duration': '120-180 seconds',
                'approach': 'rigorous_understanding'
            },
            'application_level': {
                'description': 'Real-world applications and case studies',
                'duration': '60-90 seconds',
                'approach': 'practical_understanding'
            }
        }
    
    def _find_conceptual_connections(self, content: str) -> List[Dict]:
        """Find connections between concepts"""
        # This would implement sophisticated concept mapping
        # For now, return basic structure
        return [
            {'type': 'prerequisite', 'concepts': ['basic_math', 'algebra']},
            {'type': 'related', 'concepts': ['statistics', 'data_analysis']},
            {'type': 'application', 'concepts': ['real_world_problems']}
        ]
    
    def _determine_pedagogical_approach(self, query: str, content: str) -> Dict:
        """Determine the best pedagogical approach"""
        approaches = {
            'constructivist': 'Build knowledge step by step',
            'inquiry_based': 'Start with questions and discover answers',
            'problem_based': 'Learn through solving real problems',
            'conceptual': 'Focus on understanding concepts deeply',
            'procedural': 'Learn through step-by-step procedures'
        }
        
        # Simple heuristic - this could be more sophisticated
        if 'why' in query.lower() or 'how' in query.lower():
            return {'primary': 'inquiry_based', 'secondary': 'constructivist'}
        elif 'solve' in query.lower() or 'calculate' in query.lower():
            return {'primary': 'problem_based', 'secondary': 'procedural'}
        else:
            return {'primary': 'conceptual', 'secondary': 'constructivist'}
    
    def _identify_content_gaps(self, query: str, content: str) -> List[str]:
        """Identify gaps in the content that need to be filled"""
        gaps = []
        
        # Check for missing fundamental explanations
        if 'define' in query.lower() and 'definition' not in content.lower():
            gaps.append('missing_definition')
        
        # Check for missing examples
        if 'example' not in content.lower() and len(content.split()) > 100:
            gaps.append('missing_examples')
        
        # Check for missing applications
        if 'application' not in content.lower() and 'use' not in content.lower():
            gaps.append('missing_applications')
        
        return gaps
    
    # Helper methods
    def _calculate_complexity_score(self, edu_level: str, cog_level: str) -> float:
        """Calculate overall complexity score"""
        edu_scores = {'elementary': 1.0, 'intermediate': 2.0, 'advanced': 3.0}
        cog_scores = {'remember': 1.0, 'understand': 1.5, 'apply': 2.0, 
                     'analyze': 2.5, 'evaluate': 3.0, 'create': 3.5}
        return edu_scores.get(edu_level, 2.0) * cog_scores.get(cog_level, 1.5)
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content"""
        # Simple extraction - could be more sophisticated with NLP
        words = re.findall(r'\b[A-Z][a-z]+\b', content)  # Capitalized words
        return list(set(words[:10]))  # Return unique, limited list
    
    def _extract_main_topic(self, query: str) -> str:
        """Extract the main topic from query"""
        # Remove common question words
        topic = re.sub(r'\b(what|how|why|when|where|explain|describe|understand)\b', '', query.lower()).strip()
        return topic if topic else 'the topic'


class AdvancedEducationalScriptGenerator:
    """
    World-class educational script generator with deep content analysis
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.analyzer = ContentAnalyzer()
        
        # Configuration paths with fallbacks
        self.config = {
            'json_metadata_path': os.getenv('JSON_METADATA_PATH', 'output/metadata.json'),
            'markdown_path': os.getenv('MARKDOWN_PATH', 'output/content.md'),
            'prompt_file_path': os.getenv('PROMPT_FILE_PATH', 'prompts/script_prompt.txt'),
            'output_script_path': os.getenv('OUTPUT_SCRIPT_PATH', 'output/generated_narrative_script.txt'),
            'output_dir': os.getenv('OUTPUT_DIR', 'output'),
            'analysis_report_path': os.getenv('ANALYSIS_REPORT_PATH', 'output/content_analysis_report.json')
        }
        
        # Ensure output directory exists
        Path(self.config['output_dir']).mkdir(parents=True, exist_ok=True)
    
    def generate_comprehensive_script(self, user_query: str, 
                                    custom_markdown_path: Optional[str] = None,
                                    custom_metadata_path: Optional[str] = None) -> Dict:
        """
        Generate world-class educational script with comprehensive analysis
        """
        print("🎯 Starting Comprehensive Educational Script Generation")
        print("="*80)
        
        try:
            # Phase 1: Load and validate content
            print("\n📚 Phase 1: Content Loading & Validation")
            content_result = self._load_and_validate_content(custom_markdown_path, custom_metadata_path)
            
            if not content_result['success']:
                return content_result
            
            # Phase 2: Deep content analysis
            print("\n🔬 Phase 2: Deep Content Analysis")
            analysis = self.analyzer.deep_analyze_content(
                user_query, 
                content_result['markdown_content'], 
                content_result['metadata']
            )
            
            # Phase 3: Generate comprehensive educational framework
            print("\n🏗️ Phase 3: Educational Framework Generation")
            framework = self._generate_educational_framework(user_query, analysis)
            
            # Phase 4: Create world-class prompt
            print("\n✍️ Phase 4: Advanced Prompt Creation")
            prompt = self._create_world_class_prompt(
                user_query=user_query,
                markdown_content=content_result['markdown_content'],
                metadata=content_result['metadata'],
                analysis=analysis,
                framework=framework
            )
            
            # Phase 5: Generate script with multiple iterations
            print("\n🤖 Phase 5: Script Generation & Refinement")
            generated_script = self._generate_and_refine_script(prompt, user_query)
            
            if not generated_script:
                return {'success': False, 'error': 'Failed to generate script content'}
            
            # Phase 6: Quality enhancement and validation
            print("\n✨ Phase 6: Quality Enhancement")
            final_script = self._enhance_and_validate_script(generated_script, user_query, analysis)
            
            # Phase 7: Save outputs and generate reports
            print("\n💾 Phase 7: Output Generation")
            output_path = self._save_script(final_script)
            analysis_report_path = self._save_analysis_report(analysis, framework)
            
            # Phase 8: Comprehensive analysis of final script
            final_analysis = self._analyze_final_script(final_script)
            
            result = {
                'success': True,
                'script_path': output_path,
                'analysis_report_path': analysis_report_path,
                'script_length': len(final_script),
                'estimated_duration': final_analysis['estimated_duration'],
                'section_count': final_analysis['section_count'],
                'word_count': final_analysis['word_count'],
                'visual_cues': final_analysis['visual_cues'],
                'depth_score': analysis['topic_taxonomy']['complexity_score'],
                'educational_quality': final_analysis['educational_quality'],
                'comprehensiveness_score': final_analysis['comprehensiveness_score'],
                'query': user_query
            }
            
            self._print_comprehensive_summary(result, analysis)
            return result
            
        except Exception as e:
            error_msg = f"❌ Comprehensive script generation failed: {str(e)}"
            print(error_msg)
            return {'success': False, 'error': error_msg}
    
    def _generate_educational_framework(self, query: str, analysis: Dict) -> Dict:
        """Generate comprehensive educational framework"""
        framework = {
            'learning_path': self._design_learning_path(analysis),
            'explanation_layers': self._design_explanation_layers(analysis),
            'visual_strategy': self._design_visual_strategy(analysis),
            'assessment_points': self._design_assessment_points(query),
            'engagement_elements': self._design_engagement_elements(analysis),
            'differentiation_strategies': self._design_differentiation_strategies(analysis)
        }
        
        return framework
    
    def _design_learning_path(self, analysis: Dict) -> List[Dict]:
        """Design optimal learning path"""
        path = [
            {
                'stage': 'hook',
                'duration': '20-30s',
                'purpose': 'capture_attention',
                'activities': ['intriguing_question', 'real_world_connection']
            },
            {
                'stage': 'foundation',
                'duration': '60-90s',
                'purpose': 'build_prerequisites',
                'activities': ['review_basics', 'establish_context']
            },
            {
                'stage': 'core_concept',
                'duration': '120-180s',
                'purpose': 'deep_understanding',
                'activities': ['systematic_explanation', 'multiple_representations']
            },
            {
                'stage': 'application',
                'duration': '90-120s',
                'purpose': 'transfer_learning',
                'activities': ['worked_examples', 'guided_practice']
            },
            {
                'stage': 'synthesis',
                'duration': '45-60s',
                'purpose': 'consolidate_learning',
                'activities': ['summary', 'connections', 'next_steps']
            }
        ]
        
        return path
    
    def _create_world_class_prompt(self, user_query: str, markdown_content: str, 
                                 metadata: Dict, analysis: Dict, framework: Dict) -> str:
        """Create world-class educational script generation prompt"""
        
        complexity_level = analysis['topic_taxonomy']['complexity_score']
        subject_domain = analysis['topic_taxonomy']['subject_domain']
        prerequisites = analysis['prerequisite_knowledge']
        learning_objectives = analysis['learning_objectives']
        
        prompt = f"""# WORLD-CLASS EDUCATIONAL SCRIPT GENERATOR
## Master Teacher Level - Comprehensive Topic Coverage

### MISSION STATEMENT
Create an exceptional educational script for "{user_query}" that rivals the best educational content from MIT, Stanford, Khan Academy, and 3Blue1Brown. The script must provide comprehensive, in-depth coverage that leaves no stone unturned while maintaining perfect clarity and engagement.

### EDUCATIONAL EXCELLENCE STANDARDS

#### 1. COMPREHENSIVE COVERAGE REQUIREMENTS
**Topic Analysis Results:**
- Subject Domain: {subject_domain}
- Complexity Level: {complexity_level:.1f}/5.0
- Prerequisites: {', '.join(prerequisites) if prerequisites else 'None identified'}
- Educational Approach: {analysis['pedagogical_approach']['primary']}

**Coverage Mandate - Must Include ALL:**
✅ **Historical Context**: How this concept developed, key contributors
✅ **Fundamental Principles**: Core underlying concepts with crystal-clear definitions
✅ **Mathematical Framework**: All relevant equations, derivations, and proofs
✅ **Multiple Perspectives**: Different ways to think about and approach the topic
✅ **Step-by-Step Breakdowns**: Detailed analysis of every component
✅ **Visual Representations**: How concepts look, behave, and interact
✅ **Worked Examples**: Multiple detailed examples with complete solutions
✅ **Edge Cases**: What happens in special or limiting conditions
✅ **Common Misconceptions**: What students often get wrong and why
✅ **Real-World Applications**: Where and how this is used in practice
✅ **Connections**: How this relates to other concepts and fields
✅ **Future Directions**: What comes next in learning this topic

#### 2. DEPTH REQUIREMENTS (Master Teacher Level)

**Layer 1 - Intuitive Foundation (60-90 seconds)**
- Start with familiar analogies and real-world connections
- Use concrete examples before abstract concepts
- Address the "why should I care?" question immediately
- Create mental models that students can build upon

**Layer 2 - Conceptual Framework (120-180 seconds)**  
- Provide precise definitions with multiple phrasings
- Explain the logical structure and reasoning
- Show how pieces fit together systematically
- Use multiple representation modes (verbal, visual, symbolic)

**Layer 3 - Mathematical Precision (90-150 seconds)**
- Present formal mathematical treatment
- Show derivations step-by-step with justification for each step
- Explain the meaning and interpretation of mathematical symbols
- Connect mathematical expressions to conceptual understanding

**Layer 4 - Application Mastery (120-180 seconds)**
- Work through multiple detailed examples
- Show problem-solving strategies and approaches
- Demonstrate how to recognize when to use these concepts
- Include both standard and creative applications

**Layer 5 - Advanced Insights (60-90 seconds)**
- Discuss limitations and assumptions
- Explore connections to advanced topics
- Address sophisticated questions that arise
- Provide perspective on ongoing research or developments

#### 3. SCRIPT STRUCTURE - MANDATORY SECTIONS

```
## Opening Hook (30-45 seconds)
[Compelling question or scenario that immediately grabs attention]
[VISUAL CUE: attention_grabbing_scene]

## Foundation Building (60-90 seconds)  
[Review prerequisites, establish context, motivation]
[VISUAL CUE: prerequisite_review_diagram]

## Core Concept Deep Dive (180-240 seconds)
[Comprehensive explanation with multiple angles]
[VISUAL CUE: primary_concept_animation]

## Mathematical Framework (120-180 seconds)
[Formal treatment, derivations, proofs]  
[VISUAL CUE: formula_development_sequence]

## Worked Examples (150-200 seconds)
[Multiple detailed examples with complete solutions]
[VISUAL CUE: step_by_step_problem_solving]

## Advanced Applications (90-120 seconds)
[Sophisticated real-world uses and extensions]
[VISUAL CUE: advanced_application_scenarios]

## Synthesis and Connections (60-90 seconds)
[How everything fits together, broader implications]
[VISUAL CUE: concept_integration_diagram]

## Mastery Check (30-45 seconds)
[Self-assessment questions, next learning steps]
[VISUAL CUE: summary_checkpoint_visual]
```

#### 4. NARRATION EXCELLENCE STANDARDS

**Voice and Tone:**
- Master teacher persona: authoritative yet approachable
- Conversational flow that sounds natural when spoken
- Appropriate pacing with strategic pauses for comprehension
- Enthusiasm that's genuine, not forced

**Language Precision:**
- Use precise technical vocabulary with clear definitions
- Employ analogies that illuminate rather than obscure
- Vary sentence structure for auditory interest  
- Include rhetorical questions that guide thinking

**Explanation Techniques:**
- **Progressive Disclosure**: Reveal complexity gradually
- **Multiple Modalities**: Verbal + visual + mathematical representations
- **Scaffolded Learning**: Each concept builds logically on previous ones
- **Metacognitive Guidance**: Explicitly discuss thinking processes

#### 5. VISUAL CUE MASTERY

**Enhanced Visual Cue System:**
- `[FADE_IN: concept_introduction]` - Gentle introduction of new elements
- `[BUILD_SEQUENCE: step1 → step2 → step3]` - Progressive construction
- `[HIGHLIGHT_TRANSFORM: before → after]` - Emphasize changes
- `[SPLIT_SCREEN: comparison_A | comparison_B]` - Side-by-side analysis
- `[ZOOM_FOCUS: detail_examination]` - Examine specific components
- `[ANIMATE_PROCESS: dynamic_demonstration]` - Show processes in action
- `[LAYER_REVEAL: concept_depth_explosion]` - Unpack complex ideas
- `[CONNECT_CONCEPTS: relationship_mapping]` - Show conceptual links

### CONTENT INTEGRATION ANALYSIS

**Source Material Analysis:**
- Markdown Content: {len(markdown_content)} characters of detailed information
- Available Images: {len(metadata.get('images', []))} visual elements
- Content Gaps Identified: {', '.join(analysis['content_gaps']) if analysis['content_gaps'] else 'None'}

**Learning Objectives:**
{chr(10).join(f"• {obj}" for obj in learning_objectives)}

**Visual Opportunities:**
{chr(10).join(f"• {visual['type']}: {visual.get('purpose', 'supporting_explanation')}" for visual in analysis['visual_opportunities'][:5])}

### SOURCE CONTENT TO LEVERAGE

**Primary Content:**
{markdown_content}

**Metadata Context:**
{metadata.get('image_summary_for_llm', 'No additional context available')}

### QUALITY ASSURANCE CHECKLIST

Before generating each section, ensure:
- [ ] Concept is explained from first principles
- [ ] Multiple examples are provided with complete solutions
- [ ] Visual cues support and enhance understanding
- [ ] Language is precise yet accessible
- [ ] Pacing allows for comprehension
- [ ] Connections to other concepts are explicit
- [ ] Real-world relevance is clear
- [ ] Common misconceptions are addressed

### FINAL OUTPUT REQUIREMENTS

Generate a complete educational script that:
✅ Provides PhD-level depth with undergraduate-level clarity
✅ Covers every aspect of the topic comprehensively  
✅ Uses sophisticated pedagogical techniques
✅ Includes rich visual cuing for professional animation
✅ Maintains perfect flow for text-to-speech narration
✅ Achieves 8-12 minutes of high-density educational content
✅ Rivals the best educational content ever created

**Target Duration:** 8-12 minutes (approximately 1200-1800 words)
**Educational Impact:** Student should have complete mastery of topic fundamentals
**Production Ready:** Immediately usable for professional educational video creation

Generate the complete world-class educational script now, starting with "## Opening Hook":
"""

        return prompt
    
    def _generate_and_refine_script(self, prompt: str, user_query: str) -> Optional[str]:
        """Generate script with multiple iterations and refinement"""
        try:
            # First generation with high creativity
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
                config=types.GenerateContentConfig(
                    temperature=0.7,  # Balanced creativity and consistency
                    max_output_tokens=8192,
                    top_k=40,
                    top_p=0.9,
                ),
            )
            
            if response.candidates and response.candidates[0].content.parts:
                initial_script = response.candidates[0].content.parts[0].text
                print("✅ Initial script generated successfully")
                
                # Refinement pass
                refinement_prompt = f"""
# SCRIPT REFINEMENT PASS

Review and enhance this educational script for "{user_query}":

{initial_script}

## Enhancement Requirements:
1. **Deepen Explanations**: Add more detailed explanations where needed
2. **Improve Flow**: Ensure smooth transitions between concepts
3. **Add Examples**: Include more concrete examples if missing
4. **Enhance Clarity**: Simplify complex sentences while maintaining accuracy
5. **Strengthen Connections**: Make relationships between concepts more explicit
6. **Perfect Timing**: Ensure appropriate pacing for narration

Generate the refined, enhanced version:
"""
                
                refinement_response = self.client.models.generate_content(
                    model="gemini-2.0-flash-exp",
                    contents=[{"role": "user", "parts": [{"text": refinement_prompt}]}],
                    config=types.GenerateContentConfig(
                        temperature=0.3,  # Lower temperature for refinement
                        max_output_tokens=8192,
                        top_k=30,
                        top_p=0.8,
                    ),
                )
                
                if refinement_response.candidates and refinement_response.candidates[0].content.parts:
                    refined_script = refinement_response.candidates[0].content.parts[0].text
                    print("✅ Script refined and enhanced")
                    return refined_script
                else:
                    print("⚠️ Refinement failed, using initial script")
                    return initial_script
            else:
                print("⚠️ Gemini returned empty response")
                return None
                
        except Exception as e:
            print(f"❌ Script generation error: {e}")
            return None
    
    def _enhance_and_validate_script(self, script: str, user_query: str, analysis: Dict) -> str:
        """Enhance and validate the generated script"""
        enhanced_script = script
        enhancements = []
        
        # Ensure comprehensive section structure
        required_sections = [
            'Opening Hook', 'Foundation Building', 'Core Concept', 
            'Mathematical Framework', 'Worked Examples', 'Advanced Applications',
            'Synthesis', 'Mastery Check'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in enhanced_script:
                missing_sections.append(section)
        
        if missing_sections:
            # Add missing sections
            for section in missing_sections:
                enhanced_script += f"\n\n## {section}\n\n[Enhanced content needed for {section.lower()} related to {user_query}]\n"
                enhancements.append(f'Added missing {section} section')
        
        # Enhance visual cues
        enhanced_script = self._enhance_visual_cues(enhanced_script)
        
        # Ensure proper narration flow
        enhanced_script = self._enhance_narration_flow(enhanced_script)
        
        # Validate content depth
        if len(enhanced_script.split()) < 1200:  # Minimum word count for comprehensive coverage
            enhanced_script += "\n\n## Additional Depth\n\n[This topic requires more comprehensive coverage to meet educational excellence standards]\n"
            enhancements.append('Added depth extension for comprehensive coverage')
        
        if enhancements:
            print(f"🔧 Script enhancements applied: {', '.join(enhancements)}")
        
        return enhanced_script
    
    def _enhance_visual_cues(self, script: str) -> str:
        """Enhance visual cues throughout the script"""
        # Replace basic cues with enhanced versions
        replacements = {
            '[SHOW': '[DISPLAY_VISUAL:',
            '[GRAPH': '[ANIMATE_GRAPH:',
            '[FORMULA': '[BUILD_FORMULA:',
            '[DIAGRAM': '[CREATE_DIAGRAM:',
            '[EXAMPLE': '[DEMONSTRATE_EXAMPLE:'
        }
        
        enhanced = script
        for old, new in replacements.items():
            enhanced = enhanced.replace(old, new)
        
        return enhanced
    
    def _enhance_narration_flow(self, script: str) -> str:
        """Enhance narration flow for better TTS performance"""
        # Add natural speech patterns
        enhanced = script
        
        # Add thinking transitions
        enhanced = re.sub(r'(\.) ([A-Z])', r'\1 Now, \2', enhanced)
        
        # Add pause cues for complex concepts
        enhanced = re.sub(r'(\[.*?\])', r'\1 [SHORT_PAUSE]', enhanced)
        
        return enhanced
    
    # Additional helper methods...
    def _load_and_validate_content(self, custom_markdown_path: Optional[str] = None,
                                 custom_metadata_path: Optional[str] = None) -> Dict:
        """Load and validate all content with comprehensive checks"""
        try:
            # Load markdown content
            markdown_path = custom_markdown_path or self.config['markdown_path']
            
            if not os.path.exists(markdown_path):
                return {
                    'success': False, 
                    'error': f'Content file not found: {markdown_path}'
                }
            
            with open(markdown_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read().strip()
            
            if not markdown_content:
                return {
                    'success': False,
                    'error': 'Content file is empty'
                }
            
            # Load and process metadata
            metadata_path = custom_metadata_path or self.config['json_metadata_path']
            metadata = self._load_and_process_metadata(metadata_path)
            
            # Validate content quality
            validation_result = self._validate_content_quality(markdown_content, metadata)
            
            if not validation_result['is_valid']:
                print(f"⚠️ Content quality issues detected: {', '.join(validation_result['issues'])}")
            
            print(f"✅ Content loaded and validated successfully")
            print(f"   📄 Markdown: {len(markdown_content)} characters")
            print(f"   📊 Metadata: {len(json.dumps(metadata))} characters")
            print(f"   📈 Quality score: {validation_result['quality_score']:.2f}/5.0")
            
            return {
                'success': True,
                'markdown_content': markdown_content,
                'metadata': metadata,
                'quality_assessment': validation_result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error loading content: {str(e)}'
            }
    
    def _validate_content_quality(self, content: str, metadata: Dict) -> Dict:
        """Validate content quality for educational purposes"""
        issues = []
        quality_score = 5.0
        
        # Check content length
        if len(content) < 500:
            issues.append("Content too brief for comprehensive explanation")
            quality_score -= 1.0
        
        # Check for structure
        if '##' not in content and '#' not in content:
            issues.append("No clear section structure")
            quality_score -= 0.5
        
        # Check for mathematical content markers
        if '$' not in content and 'equation' not in content.lower():
            issues.append("May lack mathematical depth")
            quality_score -= 0.3
        
        # Check for examples
        if 'example' not in content.lower():
            issues.append("Missing concrete examples")
            quality_score -= 0.5
        
        return {
            'is_valid': quality_score >= 3.0,
            'quality_score': max(0, quality_score),
            'issues': issues
        }
    
    def _load_and_process_metadata(self, metadata_path: str) -> Dict:
        """Load and enhance metadata with comprehensive analysis"""
        try:
            if not os.path.exists(metadata_path):
                print(f"⚠️ Metadata file not found: {metadata_path}")
                return {"image_summary_for_llm": "No metadata file available."}
            
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Enhanced metadata processing with detailed image analysis
            if "images" in metadata and isinstance(metadata["images"], list):
                image_summaries = []
                image_summaries.append(f"📸 Document contains {len(metadata['images'])} visual elements for educational enhancement:")
                
                for i, img in enumerate(metadata["images"], 1):
                    img_name = img.get("image_name", f"Image_{i}")
                    context = img.get("context_type", "general")
                    keywords = ", ".join(img.get("keywords", []))
                    description = img.get("description", "No description")
                    
                    # Enhanced image context analysis
                    educational_value = "high" if any(word in description.lower() for word in 
                                                    ['graph', 'chart', 'diagram', 'formula', 'equation']) else "medium"
                    
                    image_summaries.append(
                        f"  • {img_name} ({context}, educational_value: {educational_value})"
                        f"\n    Description: {description}"
                        f"{' | Keywords: ' + keywords if keywords else ''}"
                    )
                
                metadata["image_summary_for_llm"] = "\n".join(image_summaries)
                metadata["visual_educational_value"] = educational_value
            else:
                metadata["image_summary_for_llm"] = "No visual elements metadata available."
                metadata["visual_educational_value"] = "none"
            
            return metadata
            
        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON in metadata file: {metadata_path}")
            return {"image_summary_for_llm": "Invalid metadata file format."}
        except Exception as e:
            print(f"⚠️ Error processing metadata: {e}")
            return {"image_summary_for_llm": f"Error loading metadata: {e}"}
    
    def _save_analysis_report(self, analysis: Dict, framework: Dict) -> str:
        """Save comprehensive analysis report"""
        report_path = self.config['analysis_report_path']
        
        report = {
            'timestamp': str(Path().resolve()),
            'content_analysis': analysis,
            'educational_framework': framework,
            'generation_metadata': {
                'version': '2.0',
                'analysis_depth': 'comprehensive',
                'educational_standards': 'world_class'
            }
        }
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Analysis report saved: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"⚠️ Could not save analysis report: {e}")
            return ""
    
    def _analyze_final_script(self, script: str) -> Dict:
        """Comprehensive analysis of the final generated script"""
        lines = script.split('\n')
        words = script.split()
        
        # Enhanced analysis
        analysis = {
            'section_count': len([line for line in lines if line.startswith('## ')]),
            'word_count': len(words),
            'estimated_duration': len(words) / 150 * 60,  # seconds
            'visual_cues': {
                'total': len(re.findall(r'\[.*?\]', script)),
                'images': len(re.findall(r'\[DISPLAY.*?\]', script)),
                'animations': len(re.findall(r'\[ANIMATE.*?\]', script)),
                'builds': len(re.findall(r'\[BUILD.*?\]', script)),
                'highlights': len(re.findall(r'\[HIGHLIGHT.*?\]', script))
            },
            'educational_quality': self._assess_educational_quality(script),
            'comprehensiveness_score': self._calculate_comprehensiveness_score(script),
            'technical_depth': self._assess_technical_depth(script)
        }
        
        return analysis
    
    def _assess_educational_quality(self, script: str) -> float:
        """Assess the educational quality of the script"""
        quality_indicators = {
            'examples': len(re.findall(r'example', script, re.IGNORECASE)),
            'explanations': len(re.findall(r'(because|since|therefore|thus)', script, re.IGNORECASE)),
            'connections': len(re.findall(r'(related|connected|similar|different)', script, re.IGNORECASE)),
            'applications': len(re.findall(r'(application|use|practical)', script, re.IGNORECASE))
        }
        
        # Weighted scoring
        score = min(5.0, (
            quality_indicators['examples'] * 0.3 +
            quality_indicators['explanations'] * 0.3 +
            quality_indicators['connections'] * 0.2 +
            quality_indicators['applications'] * 0.2
        ) / 2)
        
        return score
    
    def _calculate_comprehensiveness_score(self, script: str) -> float:
        """Calculate how comprehensive the script is"""
        comprehensive_elements = [
            'definition', 'example', 'application', 'formula', 'graph',
            'history', 'connection', 'misconception', 'practice', 'summary'
        ]
        
        present_elements = sum(1 for element in comprehensive_elements 
                             if element in script.lower())
        
        return (present_elements / len(comprehensive_elements)) * 5.0
    
    def _assess_technical_depth(self, script: str) -> str:
        """Assess the technical depth level of the script"""
        depth_indicators = {
            'basic': ['definition', 'simple', 'basic', 'introduction'],
            'intermediate': ['formula', 'equation', 'calculate', 'solve'],
            'advanced': ['proof', 'derive', 'theorem', 'analysis', 'optimization']
        }
        
        scores = {}
        for level, indicators in depth_indicators.items():
            scores[level] = sum(1 for indicator in indicators if indicator in script.lower())
        
        max_level = max(scores, key=scores.get)
        return max_level if scores[max_level] > 0 else 'basic'
    
    # Remaining helper methods for design functions
    def _design_explanation_layers(self, analysis: Dict) -> Dict:
        """Design multi-layered explanation approach"""
        return {
            'intuitive': 'Start with everyday analogies and familiar concepts',
            'conceptual': 'Build theoretical understanding systematically', 
            'mathematical': 'Introduce formal mathematical treatment',
            'practical': 'Demonstrate real-world applications',
            'advanced': 'Explore sophisticated extensions and connections'
        }
    
    def _design_visual_strategy(self, analysis: Dict) -> Dict:
        """Design comprehensive visual strategy"""
        return {
            'primary_visuals': analysis['visual_opportunities'][:3],
            'supporting_visuals': analysis['visual_opportunities'][3:],
            'animation_sequences': ['build_up', 'transform', 'highlight'],
            'timing_strategy': 'sync_with_narration'
        }
    
    def _design_assessment_points(self, query: str) -> List[str]:
        """Design embedded assessment points"""
        return [
            'Can you explain the main concept in your own words?',
            'What would happen if we changed this parameter?',
            'How does this connect to what we learned earlier?',
            'Where might you use this in real life?'
        ]
    
    def _design_engagement_elements(self, analysis: Dict) -> List[str]:
        """Design student engagement elements"""
        return [
            'thought_provoking_questions',
            'surprising_connections',
            'real_world_relevance',
            'interactive_moments',
            'aha_moment_reveals'
        ]
    
    def _design_differentiation_strategies(self, analysis: Dict) -> Dict:
        """Design strategies for different learning needs"""
        return {
            'visual_learners': 'Rich diagrams and animations',
            'auditory_learners': 'Clear verbal explanations with examples',
            'kinesthetic_learners': 'Interactive elements and manipulatives',
            'reading_learners': 'Text summaries and written examples'
        }
    
    def _save_script(self, script: str) -> str:
        """Save the generated script with backup"""
        output_path = self.config['output_script_path']
        
        # Create backup if file exists
        if os.path.exists(output_path):
            backup_path = f"{output_path}.backup"
            try:
                os.rename(output_path, backup_path)
                print(f"📋 Created backup: {backup_path}")
            except Exception as e:
                print(f"⚠️ Could not create backup: {e}")
        
        # Save new script
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(script)
            
            print(f"💾 Script saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error saving script: {e}")
            return ""
    
    def _print_comprehensive_summary(self, result: Dict, analysis: Dict):
        """Print comprehensive success summary"""
        print("\n" + "="*80)
        print("🎉 WORLD-CLASS EDUCATIONAL SCRIPT GENERATION COMPLETE!")
        print("="*80)
        
        print(f"🎯 Topic: {result['query']}")
        print(f"📄 Script length: {result['script_length']:,} characters")
        print(f"📊 Word count: {result['word_count']} words")
        print(f"⏱️ Estimated duration: {result['estimated_duration']:.1f} seconds ({result['estimated_duration']/60:.1f} minutes)")
        print(f"📚 Sections: {result['section_count']}")
        print(f"🧠 Depth score: {result['depth_score']:.2f}/5.0")
        print(f"🎓 Educational quality: {result['educational_quality']:.2f}/5.0")
        print(f"📖 Comprehensiveness: {result['comprehensiveness_score']:.2f}/5.0")
        
        print(f"\n🎨 Visual elements breakdown:")
        for cue_type, count in result['visual_cues'].items():
            if isinstance(count, dict):
                for sub_type, sub_count in count.items():
                    if sub_count > 0:
                        print(f"   • {sub_type.title()}: {sub_count}")
            elif count > 0:
                print(f"   • {cue_type.title()}: {count}")
        
        print(f"\n🔬 Content Analysis Results:")
        taxonomy = analysis['topic_taxonomy']
        print(f"   • Subject Domain: {taxonomy['subject_domain'].title()}")
        print(f"   • Educational Level: {taxonomy['educational_level'].title()}")
        print(f"   • Cognitive Level: {taxonomy['cognitive_level'].title()}")
        print(f"   • Prerequisites: {', '.join(analysis['prerequisite_knowledge'][:3]) if analysis['prerequisite_knowledge'] else 'None'}")
        
        print(f"\n📁 Output files:")
        print(f"   • Main script: {result['script_path']}")
        print(f"   • Analysis report: {result.get('analysis_report_path', 'Not generated')}")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Review the comprehensive script")
        print(f"   2. Run: python main_advanced_system.py")
        print(f"   3. Generate world-class educational video!")
        
        print(f"\n💡 Quality Assessment:")
        if result['educational_quality'] >= 4.0:
            print("   ✅ Exceptional educational quality - ready for professional use")
        elif result['educational_quality'] >= 3.0:
            print("   ✅ High educational quality - suitable for educational content")
        else:
            print("   ⚠️ Educational quality could be enhanced - consider review")
        
        if result['comprehensiveness_score'] >= 4.0:
            print("   ✅ Comprehensive topic coverage achieved")
        elif result['comprehensiveness_score'] >= 3.0:
            print("   ✅ Good topic coverage with room for enhancement")
        else:
            print("   ⚠️ Topic coverage could be more comprehensive")
        
        print(f"\n🌟 Your world-class educational script is ready for animation!")


def main():
    """Main execution function with comprehensive CLI"""
    print("🎬 World-Class Educational Script Generator")
    print("🚀 Powered by Advanced Content Analysis & Google Gemini 2.0 Flash")
    print("📚 Generating Comprehensive, In-Depth Educational Content")
    print("="*80)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: Google API key not found!")
        print("   Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
        print("   Example: export GOOGLE_API_KEY='your_api_key_here'")
        print("   Get your API key from: https://aistudio.google.com/app/apikey")
        return 1
    
    try:
        # Initialize advanced generator
        print("🔧 Initializing Advanced Educational Script Generator...")
        generator = AdvancedEducationalScriptGenerator(api_key)
        print("✅ Generator initialized successfully")
        
        # Get user input with validation
        if len(sys.argv) > 1:
            user_query = ' '.join(sys.argv[1:])
            print(f"📖 Using command line topic: {user_query}")
        else:
            print("\n" + "="*50)
            print("📝 TOPIC INPUT")
            print("="*50)
            print("Enter the educational topic you want explained comprehensively.")
            print("Examples:")
            print("  • 'Explain linear regression in machine learning'")
            print("  • 'How does photosynthesis work in plants'")
            print("  • 'Derive the quadratic formula step by step'")
            print("  • 'What are neural networks and how do they learn'")
            print("-" * 50)
            user_query = input("🎯 Your topic: ").strip()
        
        if not user_query:
            print("❌ Error: Topic cannot be empty!")
            print("   Please provide a specific educational topic to explain")
            return 1
        
        if len(user_query.split()) < 2:
            print("⚠️ Warning: Very short topic query detected")
            print("   For best results, provide more specific details")
            confirm = input("   Continue anyway? (y/n): ").lower()
            if confirm != 'y':
                return 0
        
        # Optional custom paths with user guidance
        print("\n" + "="*50)
        print("📁 CONTENT FILES (Optional)")
        print("="*50)
        print("If you have custom content files, specify them below.")
        print("Otherwise, press Enter to use default paths.")
        print("-" * 50)
        
        custom_markdown = input("📄 Custom markdown file path: ").strip() or None
        custom_metadata = input("📊 Custom metadata file path: ").strip() or None
        
        if custom_markdown and not os.path.exists(custom_markdown):
            print(f"⚠️ Warning: Markdown file not found: {custom_markdown}")
            print("   Will attempt to use default path")
            custom_markdown = None
        
        if custom_metadata and not os.path.exists(custom_metadata):
            print(f"⚠️ Warning: Metadata file not found: {custom_metadata}")
            print("   Will attempt to use default path")
            custom_metadata = None
        
        # Generate the comprehensive script
        print(f"\n🚀 Starting comprehensive script generation for: '{user_query}'")
        print("   This may take 30-60 seconds for thorough analysis...")
        
        result = generator.generate_comprehensive_script(
            user_query=user_query,
            custom_markdown_path=custom_markdown,
            custom_metadata_path=custom_metadata
        )
        
        if result['success']:
            print("\n✨ World-class educational script generated successfully!")
            print("🎓 Ready to create exceptional educational content!")
            return 0
        else:
            print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")
            print("\n🔧 Troubleshooting suggestions:")
            print("   • Check that content files exist and are readable")
            print("   • Verify your internet connection for AI model access")
            print("   • Ensure your API key is valid and has quota remaining")
            print("   • Try a more specific topic query")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n👋 Script generation cancelled by user")
        print("   Your work has been saved up to the interruption point")
        return 0
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("\n🔧 This might help:")
        print("   • Check file permissions in the output directory")
        print("   • Verify all dependencies are installed")
        print("   • Try running with a simpler topic first")
        return 1


if __name__ == "__main__":
    exit(main())
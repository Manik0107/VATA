#!/usr/bin/env python3
"""
Advanced Narrative Parser for Educational Scripts
Compatible with Manim 0.19.0 and latest APIs (2025)
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class VoiceoverSegment:
    """Structured voiceover segment with timing and content"""
    text: str
    start_time: float = 0.0
    duration: float = 0.0
    pause_after: float = 0.0
    visual_cues: List[str] = None
    
    def __post_init__(self):
        if self.visual_cues is None:
            self.visual_cues = []


@dataclass
class AnimationSection:
    """Complete section data for animation generation"""
    title: str
    method_name: str
    segments: List[VoiceoverSegment]
    images: List[str]
    diagrams: List[str]
    animation_cues: List[str]
    estimated_duration: float
    mathematical_content: List[str]
    
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


class AdvancedNarrativeParser:
    """
    Advanced parser for educational narrative scripts with AI-powered analysis
    """
    
    def __init__(self):
        self.timing_mappings = {
            'SHORT PAUSE': 1.0,
            'MEDIUM PAUSE': 2.0,
            'LONG PAUSE': 3.0,
            'BRIEF PAUSE': 0.5,
            'EXTENDED PAUSE': 4.0
        }
        
        self.visual_cue_patterns = {
            r'\[DISPLAY IMAGE:\s*([^\]]+)\]': 'image',
            r'\[DISPLAY DIAGRAM:\s*([^\]]+)\]': 'diagram', 
            r'\[DISPLAY GRAPH:\s*([^\]]+)\]': 'graph',
            r'\[SHOW EQUATION:\s*([^\]]+)\]': 'equation',
            r'\[ANIMATE:\s*([^\]]+)\]': 'animation'
        }
        
        self.content_analysis_patterns = {
            'mathematical': [
                r'equation', r'formula', r'calculate', r'regression', 
                r'derivative', r'integral', r'matrix', r'function',
                r'slope', r'intercept', r'coefficient', r'variable'
            ],
            'conceptual': [
                r'concept', r'definition', r'understand', r'explain',
                r'theory', r'principle', r'idea', r'meaning'
            ],
            'data_visualization': [
                r'graph', r'plot', r'chart', r'data', r'scatter',
                r'line', r'visualization', r'axis', r'point'
            ],
            'interactive': [
                r'example', r'demonstrate', r'show', r'illustrate',
                r'case study', r'instance', r'practice'
            ]
        }
        
    def parse_narrative_script(self, script_content: str) -> Dict:
        """
        Main parsing method that converts narrative script to structured data
        """
        print("🔍 Starting advanced narrative parsing...")
        
        # Extract and process sections
        sections = self._extract_sections(script_content)
        processed_sections = []
        
        total_duration = 0.0
        total_images = 0
        total_animations = 0
        
        for section_data in sections:
            processed = self._process_section_advanced(section_data)
            processed_sections.append(processed)
            
            total_duration += processed.estimated_duration
            total_images += len(processed.images)
            total_animations += len(processed.animation_cues)
        
        result = {
            'sections': processed_sections,
            'metadata': {
                'total_sections': len(processed_sections),
                'total_duration': total_duration,
                'total_images': total_images,
                'total_animations': total_animations,
                'complexity_score': self._calculate_complexity_score(processed_sections)
            }
        }
        
        print(f"✅ Parsed {len(processed_sections)} sections")
        print(f"📊 Total duration: {total_duration:.1f}s")
        print(f"🖼️ Images to integrate: {total_images}")
        
        return result
    
    def _extract_sections(self, script: str) -> List[Dict]:
        """Extract section headers and content with improved parsing"""
        # Remove any BOM or invisible characters
        script = script.encode('utf-8').decode('utf-8-sig').strip()
        
        # Split by section headers (## Title)
        parts = re.split(r'^## (.+)$', script, flags=re.MULTILINE)
        
        # Remove empty first element if exists
        if parts and not parts[0].strip():
            parts = parts[1:]
            
        sections = []
        for i in range(0, len(parts), 2):
            if i + 1 < len(parts):
                title = parts[i].strip()
                content = parts[i + 1].strip()
                
                if title and content:  # Only add non-empty sections
                    sections.append({
                        'title': title,
                        'content': content,
                        'position': i // 2
                    })
        
        return sections
    
    def _process_section_advanced(self, section_data: Dict) -> AnimationSection:
        """Advanced processing of individual sections with AI-powered analysis"""
        title = section_data['title']
        content = section_data['content']
        
        # Extract voiceover segments with timing
        segments = self._extract_voiceover_segments(content)
        
        # Extract visual elements
        images = self._extract_visual_elements(content, 'image')
        diagrams = self._extract_visual_elements(content, 'diagram')
        
        # Analyze content for animation cues
        animation_cues = self._analyze_content_for_animations(content, title)
        
        # Extract mathematical content
        math_content = self._extract_mathematical_content(content)
        
        # Calculate duration with improved estimation
        duration = self._calculate_section_duration(segments, content)
        
        # Generate method name
        method_name = self._generate_method_name(title)
        
        return AnimationSection(
            title=title,
            method_name=method_name,
            segments=segments,
            images=images,
            diagrams=diagrams,
            animation_cues=animation_cues,
            estimated_duration=duration,
            mathematical_content=math_content
        )
    
    def _extract_voiceover_segments(self, content: str) -> List[VoiceoverSegment]:
        """Extract structured voiceover segments with timing analysis"""
        # Remove visual instructions for clean text
        clean_content = re.sub(r'\[[^\]]+\]', '', content)
        clean_content = re.sub(r'\([^)]*\)', '', clean_content)  # Remove stage directions
        
        # Split into sentences, preserving structure
        sentences = re.split(r'(?<=[.!?])\s+', clean_content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        segments = []
        cumulative_time = 0.0
        
        for sentence in sentences:
            # Estimate duration based on word count and complexity
            word_count = len(sentence.split())
            # Average speaking rate: 150-180 words per minute
            duration = word_count / 2.5  # 150 words per minute
            
            # Adjust for complexity (mathematical terms, technical language)
            if any(re.search(term, sentence.lower()) for term in ['equation', 'formula', 'regression']):
                duration *= 1.3  # Slower for complex content
            
            segments.append(VoiceoverSegment(
                text=sentence,
                start_time=cumulative_time,
                duration=duration,
                pause_after=0.5  # Default pause between sentences
            ))
            
            cumulative_time += duration + 0.5
        
        return segments
    
    def _extract_visual_elements(self, content: str, element_type: str) -> List[str]:
        """Extract specific visual elements using improved pattern matching"""
        elements = []
        
        for pattern, cue_type in self.visual_cue_patterns.items():
            if cue_type == element_type:
                matches = re.findall(pattern, content)
                elements.extend(matches)
        
        # Clean and validate filenames
        cleaned_elements = []
        for element in elements:
            cleaned = element.strip()
            if cleaned and not cleaned.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Assume PNG if no extension
                cleaned += '.png'
            cleaned_elements.append(cleaned)
        
        return list(set(cleaned_elements))  # Remove duplicates
    
    def _analyze_content_for_animations(self, content: str, title: str) -> List[str]:
        """AI-powered content analysis for animation cue generation"""
        cues = []
        content_lower = content.lower()
        title_lower = title.lower()
        
        # Analyze content patterns
        for category, patterns in self.content_analysis_patterns.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, content_lower))
            
            if matches >= 2:  # Threshold for significance
                cues.append(f"create_{category}_animation")
        
        # Title-based analysis
        if any(word in title_lower for word in ['introduction', 'intro']):
            cues.append('create_title_sequence')
            
        if any(word in title_lower for word in ['conclusion', 'summary', 'wrap']):
            cues.append('create_summary_animation')
            
        # Content-specific cues
        if 'regression line' in content_lower:
            cues.append('animate_regression_line')
            
        if any(word in content_lower for word in ['scatter', 'plot', 'points']):
            cues.append('create_scatter_plot')
            
        if 'equation' in content_lower or 'formula' in content_lower:
            cues.append('build_equation_step_by_step')
        
        return list(set(cues))  # Remove duplicates
    
    def _extract_mathematical_content(self, content: str) -> List[str]:
        """Extract mathematical formulas and equations"""
        math_content = []
        
        # Pattern for common mathematical expressions
        math_patterns = [
            r'Y\s*=\s*[^.]+',  # Equations like Y = a + bx
            r'[a-zA-Z]\s*=\s*[^.]+',  # Variable assignments
            r'[∑∫∂π±√]',  # Mathematical symbols
            r'\b\d+\.\d+\b',  # Decimal numbers
            r'\b[a-zA-Z]\^\d+\b'  # Exponents
        ]
        
        for pattern in math_patterns:
            matches = re.findall(pattern, content)
            math_content.extend(matches)
        
        return list(set(math_content))
    
    def _calculate_section_duration(self, segments: List[VoiceoverSegment], content: str) -> float:
        """Calculate section duration with improved accuracy"""
        # Base duration from segments
        segment_duration = sum(seg.duration + seg.pause_after for seg in segments)
        
        # Add time for visual elements
        visual_time = len(re.findall(r'\[DISPLAY [^\]]+\]', content)) * 2.0
        
        # Add time for pauses
        pause_matches = re.findall(r'\[([A-Z]+ PAUSE)\]', content)
        pause_duration = sum(self.timing_mappings.get(pause, 1.0) for pause in pause_matches)
        
        return segment_duration + visual_time + pause_duration
    
    def _generate_method_name(self, title: str) -> str:
        """Generate valid Python method name from section title"""
        # Remove special characters and convert to snake_case
        method_name = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        method_name = re.sub(r'\s+', '_', method_name.lower())
        
        # Ensure valid Python identifier
        if not method_name or method_name[0].isdigit():
            method_name = f"section_{method_name}"
            
        return f"animate_{method_name}"
    
    def _calculate_complexity_score(self, sections: List[AnimationSection]) -> float:
        """Calculate content complexity score for optimization"""
        total_score = 0.0
        
        for section in sections:
            score = 0.0
            
            # Mathematical content adds complexity
            score += len(section.mathematical_content) * 0.5
            
            # Visual elements add complexity  
            score += len(section.images) * 0.3
            score += len(section.diagrams) * 0.4
            
            # Animation cues add complexity
            score += len(section.animation_cues) * 0.2
            
            # Duration affects complexity
            score += section.estimated_duration * 0.01
            
            total_score += score
        
        return total_score / len(sections) if sections else 0.0

    def export_analysis_report(self, parsed_data: Dict, output_path: str = "narrative_analysis.json"):
        """Export detailed analysis report for debugging and optimization"""
        with open(output_path, 'w', encoding='utf-8') as f:
            # Convert dataclasses to dict for JSON serialization
            serializable_data = {
                'metadata': parsed_data['metadata'],
                'sections': []
            }
            
            for section in parsed_data['sections']:
                section_dict = {
                    'title': section.title,
                    'method_name': section.method_name,
                    'estimated_duration': section.estimated_duration,
                    'segments_count': len(section.segments),
                    'images': section.images,
                    'diagrams': section.diagrams,
                    'animation_cues': section.animation_cues,
                    'mathematical_content': section.mathematical_content,
                    'segments': [
                        {
                            'text': seg.text[:100] + '...' if len(seg.text) > 100 else seg.text,
                            'duration': seg.duration,
                            'start_time': seg.start_time
                        } for seg in section.segments
                    ]
                }
                serializable_data['sections'].append(section_dict)
            
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Analysis report exported to: {output_path}")


# Example usage and testing
if __name__ == "__main__":
    parser = AdvancedNarrativeParser()
    
    # Test with sample content
    sample_script = """
## Introduction
Hey everyone, ever wondered how we can find hidden relationships within data? [MEDIUM PAUSE] 
This powerful statistical tool helps us understand linear relationships. [DISPLAY IMAGE: intro_graph.png]

## Core Concepts  
Linear regression explores the relationship between variables. [SHORT PAUSE]
The regression line Y = a + bx is fundamental. [SHOW EQUATION: Y = a + bx]
"""
    
    result = parser.parse_narrative_script(sample_script)
    parser.export_analysis_report(result)
    
    print("✅ Advanced Narrative Parser test completed!")

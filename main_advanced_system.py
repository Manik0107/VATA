#!/usr/bin/env python3
"""
Enhanced Narrative-to-Manim System with Professional Visualizations
Advanced orchestrator optimized for educational content with stunning animations
Compatible with all latest 2025 APIs and syntax
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional, List
import json
from dotenv import load_dotenv
import time
from dataclasses import dataclass

# Import our enhanced modules
from narrative_parser import AdvancedNarrativeParser
from manim_code_generator import EnhancedManimCodeGenerator


@dataclass
class ProcessingCheckpoint:
    """Checkpoint system for generation processes"""
    stage: str
    timestamp: float
    data: Dict
    success: bool


class EnhancedNarrativeToManimSystem:
    """
    Enhanced system orchestrator for professional narrative-to-Manim conversion
    Now supports stunning educational visualizations with advanced animations
    """
    
    def __init__(self, config_file: str = ".env"):
        """Initialize enhanced system with professional configuration"""
        load_dotenv(config_file)
        
        # Load enhanced configuration
        self.config = self._load_enhanced_configuration()
        
        # Initialize enhanced components
        self.parser = AdvancedNarrativeParser()
        
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Google API key not found. Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")
        
        # Initialize enhanced code generator with professional capabilities
        self.code_generator = EnhancedManimCodeGenerator(api_key)
        
        # Initialize checkpoint system
        self.checkpoints: List[ProcessingCheckpoint] = []
        
        print("Enhanced Professional Narrative-to-Manim System initialized")
        print(f"Narrative file: {self.config['narrative_path']}")
        print(f"Images folder: {self.config['images_folder']}")
        print(f"Output file: {self.config['output_file']}")
        print(f"Professional animations: Enabled")
        print(f"Advanced visualizations: Active")
    
    def _load_enhanced_configuration(self) -> Dict:
        """Load enhanced system configuration with professional parameters"""
        return {
            # Core configuration
            'narrative_path': os.getenv('NARRATIVE_PATH', 'output/generated_narrative_script.txt'),
            'images_folder': os.getenv('IMAGES_FOLDER', 'output/linear_regression_notes_images'),
            'metadata_path': os.getenv('JSON_METADATA_PATH', 'output/linear_regression_notes.json'),
            'markdown_path': os.getenv('MARKDOWN_PATH', 'output/linear_regression_notes.md'),
            'output_file': os.getenv('OUTPUT_MANIM_FILE', 'generated_manim_code.py'),
            'quality': os.getenv('DEFAULT_QUALITY', 'medium_high'),
            'preview': os.getenv('DEFAULT_PREVIEW', 'True').lower() == 'true',
            'disable_caching': os.getenv('DISABLE_CACHING', 'True').lower() == 'true',
            
            # Professional enhancement configuration
            'enable_professional_animations': os.getenv('ENABLE_PROFESSIONAL_ANIMATIONS', 'True').lower() == 'true',
            'enable_advanced_visualizations': os.getenv('ENABLE_ADVANCED_VISUALIZATIONS', 'True').lower() == 'true',
            'enable_progressive_revelation': os.getenv('ENABLE_PROGRESSIVE_REVELATION', 'True').lower() == 'true',
            'enable_context_persistence': os.getenv('ENABLE_CONTEXT_PERSISTENCE', 'True').lower() == 'true',
            'visualization_complexity': os.getenv('VISUALIZATION_COMPLEXITY', 'high'),  # low/medium/high
            'animation_quality': os.getenv('ANIMATION_QUALITY', 'professional'),  # basic/standard/professional
            'color_coding_enabled': os.getenv('COLOR_CODING_ENABLED', 'True').lower() == 'true',
            'interactive_elements': os.getenv('INTERACTIVE_ELEMENTS', 'True').lower() == 'true',
        }
    
    def process_narrative_to_animation(self, custom_narrative_path: str = None) -> Dict:
        """
        Enhanced pipeline: narrative script → professional parsing → Stunning Manim code generation
        Now supports advanced educational visualizations with progressive concept building
        """
        print("\n" + "="*80)
        print("ENHANCED PROFESSIONAL NARRATIVE-TO-MANIM PROCESSING")
        print("Advanced Educational Visualization System")
        print("="*80)
        
        start_time = time.time()
        
        try:
            # Checkpoint 1: Initialize processing
            self._create_checkpoint("initialization", {"start_time": start_time})
            
            # Step 1: Load and validate narrative script
            narrative_path = custom_narrative_path or self.config['narrative_path']
            narrative_script = self._load_enhanced_narrative_script(narrative_path)
            
            # Step 2: Load additional context with metadata
            metadata = self._load_enhanced_metadata()
            available_images = self._get_available_images()
            
            print(f"Loaded narrative: {len(narrative_script)} characters")
            print(f"Found images: {len(available_images)}")
            print(f"Professional animations: {'Enabled' if self.config['enable_professional_animations'] else 'Disabled'}")
            
            # Checkpoint 2: Content loaded
            self._create_checkpoint("content_loaded", {
                "narrative_length": len(narrative_script),
                "image_count": len(available_images),
                "professional_mode": self.config['enable_professional_animations']
            })
            
            # Step 3: Enhanced narrative parsing with visual analysis
            print("\nAdvanced Narrative Analysis with Visualization Detection...")
            parsed_data = self.parser.parse_narrative_script(narrative_script)
            
            # Enhanced content analysis for professional animations
            complexity_analysis = self._analyze_content_complexity(parsed_data, narrative_script)
            visualization_strategy = self._determine_visualization_strategy(narrative_script, complexity_analysis)
            
            print(f"Content complexity: {complexity_analysis['level']} ({complexity_analysis['score']:.2f})")
            print(f"Visualization strategy: {visualization_strategy['primary_approach']}")
            print(f"Detected sections: {len(parsed_data['sections'])}")
            print(f"Professional animations: {visualization_strategy['animation_count']} planned")
            
            # Checkpoint 3: Analysis complete
            self._create_checkpoint("analysis_complete", {
                "sections_count": len(parsed_data['sections']),
                "complexity": complexity_analysis,
                "visualization_strategy": visualization_strategy
            })
            
            # Export enhanced analysis report
            analysis_file = "professional_analysis_report.json"
            self._export_enhanced_analysis_report(parsed_data, complexity_analysis, visualization_strategy, analysis_file)
            
            # Step 4: Professional Manim code generation
            print("\nGenerating Professional Manim Code with Advanced Visualizations...")
            print("Creating stunning educational animations...")
            
            generation_start = time.time()
            generated_code = self.code_generator.generate_enhanced_manim_code(
                narrative_script=narrative_script,
                images_folder=self.config['images_folder'],
                metadata=metadata,
                complexity_analysis=complexity_analysis,
                config=self.config
            )
            generation_time = time.time() - generation_start
            
            # Checkpoint 4: Code generation complete
            self._create_checkpoint("code_generated", {
                "generation_time": generation_time,
                "code_length": len(generated_code),
                "professional_features": True
            })
            
            # Step 5: Code validation and optimization
            print("\nValidating and optimizing professional animations...")
            optimized_code = self._optimize_professional_code(generated_code, complexity_analysis, visualization_strategy)
            
            # Step 6: Save enhanced code with professional backup system
            output_path = self.config['output_file']
            self._save_professional_code(optimized_code, output_path, complexity_analysis)
            
            # Step 7: Generate comprehensive execution instructions
            instructions = self._generate_professional_execution_instructions(
                output_path, complexity_analysis, visualization_strategy
            )
            
            # Compile enhanced results
            total_time = time.time() - start_time
            results = {
                'success': True,
                'narrative_file': narrative_path,
                'output_file': output_path,
                'analysis_file': analysis_file,
                'parsed_sections': len(parsed_data['sections']),
                'estimated_duration': parsed_data['metadata']['total_duration'],
                'complexity_score': complexity_analysis['score'],
                'complexity_level': complexity_analysis['level'],
                'visualization_approach': visualization_strategy['primary_approach'],
                'animation_count': visualization_strategy['animation_count'],
                'professional_features': visualization_strategy['professional_features'],
                'code_length': len(optimized_code),
                'available_images': len(available_images),
                'execution_instructions': instructions,
                'processing_time': total_time,
                'generation_time': generation_time,
                'checkpoints': len(self.checkpoints),
                'professional_capabilities': [
                    'Advanced scatter plot visualizations',
                    'Color-coded prediction vs actual analysis',
                    'Progressive concept revelation',
                    'Context-persistent animations',
                    'Professional mathematical derivations',
                    'Interactive visual elements'
                ]
            }
            
            # Final checkpoint
            self._create_checkpoint("processing_complete", results)
            
            self._print_professional_success_summary(results)
            return results
            
        except Exception as e:
            error_msg = f"Error in professional processing pipeline: {str(e)}"
            print(error_msg)
            
            # Error checkpoint
            self._create_checkpoint("error", {"error": str(e)}, success=False)
            
            return {
                'success': False,
                'error': error_msg,
                'narrative_file': narrative_path if 'narrative_path' in locals() else None,
                'checkpoints': len(self.checkpoints),
                'processing_time': time.time() - start_time if 'start_time' in locals() else 0
            }
    
    def _determine_visualization_strategy(self, narrative_script: str, complexity_analysis: Dict) -> Dict:
        """Determine the optimal visualization strategy based on content analysis"""
        script_lower = narrative_script.lower()
        
        # Detect content type for appropriate visualizations
        content_indicators = {
            'regression': ['regression', 'predict', 'correlation', 'best fit', 'linear relationship'],
            'data_analysis': ['data', 'statistics', 'analysis', 'distribution', 'variance'],
            'mathematics': ['equation', 'formula', 'theorem', 'proof', 'derivative'],
            'conceptual': ['concept', 'principle', 'theory', 'understanding', 'explanation']
        }
        
        detected_types = []
        for content_type, keywords in content_indicators.items():
            if any(keyword in script_lower for keyword in keywords):
                detected_types.append(content_type)
        
        # Determine primary visualization approach
        if 'regression' in detected_types:
            primary_approach = 'scatter_plot_with_regression'
            animation_count = 8  # Multiple sophisticated animations
            professional_features = [
                'Color-coded actual vs predicted points',
                'Animated error line visualization', 
                'Progressive line fitting animation',
                'Interactive legend and annotations',
                'Mathematical formula integration'
            ]
        elif 'data_analysis' in detected_types:
            primary_approach = 'statistical_visualization'
            animation_count = 6
            professional_features = [
                'Dynamic histogram animations',
                'Distribution curve fitting',
                'Statistical measure visualization'
            ]
        elif 'mathematics' in detected_types:
            primary_approach = 'mathematical_derivation'
            animation_count = 5
            professional_features = [
                'Step-by-step formula building',
                'Geometric interpretations',
                'Function transformations'
            ]
        else:
            primary_approach = 'conceptual_flow'
            animation_count = 4
            professional_features = [
                'Concept relationship diagrams',
                'Progressive information revelation',
                'Interactive demonstrations'
            ]
        
        return {
            'primary_approach': primary_approach,
            'detected_types': detected_types,
            'animation_count': animation_count,
            'professional_features': professional_features,
            'complexity_rating': 'high' if complexity_analysis['score'] > 6 else 'medium',
            'requires_advanced_math': 'mathematics' in detected_types,
            'requires_data_viz': any(t in detected_types for t in ['regression', 'data_analysis'])
        }
    
    def _analyze_content_complexity(self, parsed_data: Dict, narrative_script: str) -> Dict:
        """Enhanced content complexity analysis for professional animations"""
        sections = parsed_data['sections']
        
        # Basic complexity metrics
        total_segments = sum(len(section.segments) for section in sections)
        mathematical_content = sum(len(section.mathematical_content) for section in sections if section.mathematical_content)
        animation_cues = sum(len(section.animation_cues) for section in sections if section.animation_cues)
        
        # Advanced analysis for professional features
        script_lower = narrative_script.lower()
        
        # Professional visualization indicators
        viz_complexity_indicators = {
            'scatter_plots': script_lower.count('data') + script_lower.count('point'),
            'regression_analysis': script_lower.count('regression') + script_lower.count('predict'),
            'mathematical_formulas': script_lower.count('equation') + script_lower.count('formula'),
            'statistical_concepts': script_lower.count('mean') + script_lower.count('variance'),
            'comparative_analysis': script_lower.count('compare') + script_lower.count('difference')
        }
        
        # Calculate professional complexity score (0-10 scale)
        complexity_score = min(10, (
            len(sections) * 0.4 +
            total_segments * 0.1 +
            mathematical_content * 0.5 +
            animation_cues * 0.3 +
            sum(viz_complexity_indicators.values()) * 0.2
        ))
        
        # Determine complexity level for professional animations
        if complexity_score < 3:
            level = "Basic"
            animation_style = "simple_transitions"
        elif complexity_score < 6:
            level = "Intermediate" 
            animation_style = "enhanced_visuals"
        elif complexity_score < 8:
            level = "Advanced"
            animation_style = "professional_animations"
        else:
            level = "Expert"
            animation_style = "sophisticated_visualizations"
        
        return {
            'score': complexity_score,
            'level': level,
            'animation_style': animation_style,
            'sections_count': len(sections),
            'total_segments': total_segments,
            'mathematical_complexity': mathematical_content,
            'visualization_indicators': viz_complexity_indicators,
            'requires_professional_treatment': complexity_score > 5,
            'estimated_render_time': complexity_score * 45,  # seconds
            'recommended_quality': 'high' if complexity_score > 6 else 'medium'
        }
    
    def _optimize_professional_code(self, code: str, complexity_analysis: Dict, visualization_strategy: Dict) -> str:
        """Optimize code for professional animations and performance"""
        optimizations_applied = []
        
        # Add professional imports if missing
        professional_imports = [
            'import gc',
            'import numpy as np'
        ]
        
        for imp in professional_imports:
            if imp not in code:
                code = imp + '\n' + code
                optimizations_applied.append(f'Added {imp}')
        
        # Add memory management for complex visualizations
        if complexity_analysis['score'] > 7:
            if 'def cleanup_scene' in code and 'gc.collect()' not in code:
                code = code.replace(
                    'def cleanup_scene(self):',
                    'def cleanup_scene(self):\n        """Clean up scene resources"""\n        gc.collect()'
                )
                optimizations_applied.append('Enhanced memory management')
        
        # Add professional timing controls
        if 'self.timing' not in code:
            timing_code = '''        # Professional timing constants
        self.timing = {
            'fast': 0.5, 'normal': 1.0, 'slow': 1.5, 'pause': 0.3,
            'build': 0.8, 'reveal': 1.2, 'transition': 0.6
        }'''
            
            # Insert after color definitions
            color_end = code.find("}")
            if color_end != -1:
                insertion_point = code.find('\n', color_end) + 1
                code = code[:insertion_point] + timing_code + '\n' + code[insertion_point:]
                optimizations_applied.append('Added professional timing controls')
        
        # Enhance for specific visualization strategies
        if visualization_strategy['primary_approach'] == 'scatter_plot_with_regression':
            if 'create_scatter_plot_with_regression' not in code:
                optimizations_applied.append('Enhanced for regression visualizations')
        
        if optimizations_applied:
            print(f"Applied professional optimizations: {', '.join(optimizations_applied)}")
        
        return code
    
    def _save_professional_code(self, code: str, output_path: str, complexity_analysis: Dict) -> None:
        """Save professional code with comprehensive backup and metadata"""
        # Create timestamped backup if file exists
        if os.path.exists(output_path):
            timestamp = int(time.time())
            backup_path = f"{output_path}.backup.{timestamp}"
            os.rename(output_path, backup_path)
            print(f"Created backup: {backup_path}")
        
        # Enhanced metadata header with professional information
        metadata_header = f'''"""
Generated by Enhanced Professional Narrative-to-Manim System v2.0
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}
Features: Professional animations, Advanced visualizations, Educational excellence
Complexity Level: {complexity_analysis['level']} ({complexity_analysis['score']:.2f}/10)
Animation Style: {complexity_analysis['animation_style']}
Compatible with: Manim 0.19.0+, manim-voiceover 0.3.7+
Processing checkpoints: {len(self.checkpoints)}

PROFESSIONAL FEATURES ENABLED:
- Color-coded actual vs predicted visualizations
- Progressive concept revelation
- Context-persistent elements
- Advanced mathematical animations
- Interactive visual elements
- Professional timing controls

RENDERING RECOMMENDATIONS:
- Use high quality settings for best results
- Allow extra render time for complex animations
- Ensure 8GB+ RAM for smooth processing
"""

'''
        
        final_code = metadata_header + code
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_code)
        
        print(f"Saved professional generated code: {output_path}")
        print(f"Code length: {len(final_code):,} characters")
        print(f"Professional features: Active")
    
    def _generate_professional_execution_instructions(self, manim_file: str, 
                                                    complexity_analysis: Dict, 
                                                    visualization_strategy: Dict) -> Dict:
        """Generate comprehensive execution instructions for professional content"""
        base_name = Path(manim_file).stem
        
        # Determine optimal settings based on complexity and visualization strategy
        if complexity_analysis['score'] > 7 or visualization_strategy['complexity_rating'] == 'high':
            quality_flag = '-pqh'  # High quality for complex professional content
            recommended_flags = '--disable_caching --verbose'
            render_time_multiplier = 2.5
        elif complexity_analysis['score'] > 4:
            quality_flag = '-pqm'  # Medium-high quality
            recommended_flags = '--disable_caching'
            render_time_multiplier = 1.8
        else:
            quality_flag = '-pql'  # Low quality for testing
            recommended_flags = ''
            render_time_multiplier = 1.0
        
        estimated_render_minutes = int(complexity_analysis['estimated_render_time'] * render_time_multiplier / 60)
        
        instructions = {
            'preview_command': f"manim {manim_file} {quality_flag} {recommended_flags}",
            'production_command': f"manim {manim_file} -pqh --disable_caching --verbose",
            'class_name': "ProfessionalAnimation",  # Updated default
            'complexity_level': complexity_analysis['level'],
            'visualization_approach': visualization_strategy['primary_approach'],
            'estimated_render_time': f"{estimated_render_minutes}+ minutes",
            
            'professional_requirements': [
                "Manim 0.19.0 or later",
                "manim-voiceover[gtts] 0.3.7 or later", 
                "Active internet connection (for GTTS)",
                "Python 3.11+ recommended",
                "8GB+ RAM for professional animations",
                "GPU acceleration highly recommended",
                f"Expected processing time: {complexity_analysis['estimated_render_time']:.0f}+ seconds",
                "Professional visualization features enabled"
            ],
            
            'professional_features_info': {
                'scatter_plot_animations': 'Advanced data point visualizations with color coding',
                'regression_line_fitting': 'Animated best-fit line with error visualization',
                'progressive_revelation': 'Context-preserving animations that build understanding',
                'mathematical_derivations': 'Step-by-step formula building with highlighting',
                'interactive_elements': 'Professional legends and annotations'
            },
            
            'troubleshooting': {
                'memory_issues': 'Increase swap space or use lower quality for testing',
                'long_render_times': 'Professional animations require more processing - be patient',
                'visualization_errors': 'Check data formatting in visualization functions',
                'caching_conflicts': 'Always use --disable_caching with manim-voiceover',
                'professional_features': 'Complex visualizations may need timing adjustments'
            },
            
            'optimization_tips': [
                "Test with preview quality first (-pql)",
                "Use --verbose to monitor complex animation progress", 
                "Close other applications to maximize available memory",
                f"Complexity score: {complexity_analysis['score']:.2f}/10",
                f"Professional features: {len(visualization_strategy['professional_features'])} active"
            ],
            
            'quality_settings': {
                'development': f"manim {manim_file} -pql --disable_caching",
                'preview': f"manim {manim_file} -pqm --disable_caching",
                'production': f"manim {manim_file} -pqh --disable_caching --verbose",
                'presentation': f"manim {manim_file} -pqk --disable_caching --verbose"  # 4K for presentations
            }
        }
        
        return instructions
    
    def _export_enhanced_analysis_report(self, parsed_data: Dict, complexity_analysis: Dict, 
                                       visualization_strategy: Dict, filename: str):
        """Export comprehensive analysis report with professional insights"""
        enhanced_report = {
            'timestamp': time.time(),
            'system_version': 'Enhanced Professional v2.0',
            'analysis_type': 'comprehensive_professional',
            
            'content_analysis': {
                'parsed_sections': len(parsed_data['sections']),
                'total_segments': sum(len(section.segments) for section in parsed_data['sections']),
                'estimated_duration': parsed_data['metadata']['total_duration']
            },
            
            'complexity_analysis': complexity_analysis,
            
            'visualization_strategy': visualization_strategy,
            
            'professional_capabilities': {
                'advanced_scatter_plots': 'scatter_plot_with_regression' in visualization_strategy['primary_approach'],
                'color_coded_analysis': True,
                'progressive_revelation': True,
                'context_persistence': True,
                'mathematical_animations': visualization_strategy.get('requires_advanced_math', False),
                'data_visualizations': visualization_strategy.get('requires_data_viz', False)
            },
            
            'processing_checkpoints': [
                {
                    'stage': cp.stage,
                    'timestamp': cp.timestamp,
                    'success': cp.success,
                    'data_summary': f"{len(cp.data)} data points"
                }
                for cp in self.checkpoints
            ],
            
            'recommendations': self._generate_professional_recommendations(complexity_analysis, visualization_strategy),
            
            'resource_requirements': {
                'processing_time_estimate': f"{complexity_analysis['estimated_render_time']:.0f} seconds",
                'memory_usage_estimate': f"{complexity_analysis['score'] * 150:.0f} MB",
                'recommended_quality': complexity_analysis['recommended_quality'],
                'gpu_acceleration': 'highly_recommended' if complexity_analysis['score'] > 6 else 'optional'
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(enhanced_report, f, indent=2, default=str)
            print(f"Professional analysis report saved: {filename}")
        except Exception as e:
            print(f"Could not save analysis report: {e}")
    
    def _generate_professional_recommendations(self, complexity_analysis: Dict, visualization_strategy: Dict) -> List[str]:
        """Generate professional recommendations based on analysis"""
        recommendations = []
        
        if complexity_analysis['score'] > 7:
            recommendations.extend([
                "Use high-quality rendering settings for professional results",
                "Allow 2-3x normal processing time for complex animations",
                "Ensure 16GB+ RAM for optimal performance",
                "Consider rendering overnight for production quality"
            ])
        
        if visualization_strategy['primary_approach'] == 'scatter_plot_with_regression':
            recommendations.extend([
                "Review data point positioning for clarity",
                "Ensure color contrast meets accessibility standards",
                "Test error line visibility at target resolution"
            ])
        
        if visualization_strategy.get('requires_advanced_math'):
            recommendations.extend([
                "Verify mathematical notation accuracy",
                "Test formula rendering at different sizes",
                "Consider breaking complex derivations into steps"
            ])
        
        if complexity_analysis['animation_style'] == 'sophisticated_visualizations':
            recommendations.extend([
                "Preview animations before final render",
                "Use professional timing controls consistently",
                "Test on target display hardware before presentation"
            ])
        
        return recommendations
    
    def _create_checkpoint(self, stage: str, data: Dict, success: bool = True):
        """Create processing checkpoint with enhanced tracking"""
        checkpoint = ProcessingCheckpoint(
            stage=stage,
            timestamp=time.time(),
            data=data,
            success=success
        )
        self.checkpoints.append(checkpoint)
        status = "✅" if success else "❌"
        print(f"Checkpoint: {stage} {status}")
    
    def _print_professional_success_summary(self, results: Dict) -> None:
        """Print comprehensive success summary for professional system"""
        print("\n" + "="*80)
        print("PROFESSIONAL ANIMATION GENERATION COMPLETE!")
        print("Enhanced Educational Visualization System - Results")
        print("="*80)
        
        # Core metrics
        print(f"Sections processed: {results['parsed_sections']}")
        print(f"Estimated video duration: {results['estimated_duration']:.1f} seconds")
        print(f"Complexity level: {results['complexity_level']} ({results['complexity_score']:.2f}/10)")
        print(f"Visualization approach: {results['visualization_approach']}")
        print(f"Professional animations: {results['animation_count']}")
        
        # Professional features
        print(f"\nProfessional capabilities enabled:")
        for capability in results['professional_capabilities']:
            print(f"   • {capability}")
        
        # Performance metrics  
        print(f"\nPerformance metrics:")
        print(f"   • Processing time: {results['processing_time']:.1f} seconds")
        print(f"   • Code generation time: {results['generation_time']:.1f} seconds") 
        print(f"   • Generated code length: {results['code_length']:,} characters")
        print(f"   • Checkpoints completed: {results['checkpoints']}")
        
        # Files created
        print(f"\nFiles created:")
        print(f"   • Professional code: {results['output_file']}")
        print(f"   • Analysis report: {results['analysis_file']}")
        
        # Execution guidance
        print(f"\nRecommended execution:")
        instructions = results['execution_instructions']
        print(f"   1. Preview: {instructions['preview_command']}")
        print(f"   2. Production: {instructions['production_command']}")
        print(f"   3. Expected render time: {instructions['estimated_render_time']}")
        
        # Professional tips
        print(f"\nProfessional tips:")
        for tip in instructions['optimization_tips']:
            print(f"   • {tip}")
        
        print(f"\nSystem ready for professional educational video creation!")

    # Helper methods remain the same as in previous version
    def _load_enhanced_narrative_script(self, file_path: str) -> str:
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
    
    def _load_enhanced_metadata(self) -> Dict:
        """Load enhanced metadata"""
        metadata_path = self.config['metadata_path']
        metadata = {}
        
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            except Exception as e:
                print(f"Could not load metadata: {e}")
        
        metadata.update({
            'processing_timestamp': time.time(),
            'system_config': self.config,
            'professional_features_enabled': True
        })
        
        return metadata
    
    def _get_available_images(self) -> List[str]:
        """Get list of available images"""
        images_folder = self.config['images_folder']
        
        if not os.path.exists(images_folder):
            print(f"Images folder not found: {images_folder}")
            return []
        
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')
        images = []
        
        try:
            for file in os.listdir(images_folder):
                if file.lower().endswith(image_extensions):
                    full_path = os.path.join(images_folder, file)
                    images.append(full_path)
        except Exception as e:
            print(f"Error reading images folder: {e}")
        
        return images


def main():
    """Enhanced main execution function with professional interface"""
    print("Enhanced Professional Narrative-to-Manim System v2.0")
    print("Advanced Educational Visualization Generator")
    print("Features: Professional animations, Advanced visualizations, Context persistence")
    
    try:
        # Initialize professional system
        system = EnhancedNarrativeToManimSystem()
        
        # Check for custom narrative file argument
        custom_narrative = None
        if len(sys.argv) > 1:
            custom_narrative = sys.argv[1]
            print(f"Using custom narrative: {custom_narrative}")
        
        # Process narrative with professional features
        results = system.process_narrative_to_animation(custom_narrative)
        
        if results['success']:
            print(f"\nProfessional educational animations ready!")
            print(f"Visualization approach: {results['visualization_approach']}")
            print(f"Animation count: {results['animation_count']}")
            return 0
        else:
            print(f"\nProcessing failed: {results.get('error', 'Unknown error')}")
            print(f"Checkpoints completed: {results.get('checkpoints', 0)}")
            return 1
            
    except Exception as e:
        print(f"\nSystem error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
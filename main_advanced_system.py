#!/usr/bin/env python3
"""
Complete Advanced Narrative-to-Manim System
Main orchestrator with error handling and progress tracking
Compatible with all latest 2025 APIs and syntax
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional
import json
from dotenv import load_dotenv

# Import our custom modules
from narrative_parser import AdvancedNarrativeParser
from manim_code_generator import ManimCodeGenerator


class AdvancedNarrativeToManimSystem:
    """
    Complete system orchestrator for advanced narrative-to-Manim conversion
    """
    
    def __init__(self, config_file: str = ".env"):
        """Initialize system with configuration"""
        load_dotenv(config_file)
        
        # Load configuration
        self.config = self._load_configuration()
        
        # Initialize components
        self.parser = AdvancedNarrativeParser()
        
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ Google API key not found. Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable.")
        
        self.code_generator = ManimCodeGenerator(api_key)
        
        print("✅ Advanced Narrative-to-Manim System initialized")
        print(f"📁 Narrative file: {self.config['narrative_path']}")
        print(f"🖼️ Images folder: {self.config['images_folder']}")
        print(f"💾 Output file: {self.config['output_file']}")
    
    def _load_configuration(self) -> Dict:
        """Load system configuration from environment variables"""
        return {
            'narrative_path': os.getenv('NARRATIVE_PATH', 'output/generated_narrative_script.txt'),
            'images_folder': os.getenv('IMAGES_FOLDER', 'output/linear_regression_notes_images'),
            'metadata_path': os.getenv('JSON_METADATA_PATH', 'output/linear_regression_notes.json'),
            'markdown_path': os.getenv('MARKDOWN_PATH', 'output/linear_regression_notes.md'),
            'output_file': os.getenv('OUTPUT_MANIM_FILE', 'generated_manim_code.py'),
            'quality': os.getenv('DEFAULT_QUALITY', 'medium'),
            'preview': os.getenv('DEFAULT_PREVIEW', 'True').lower() == 'true',
            'disable_caching': os.getenv('DISABLE_CACHING', 'True').lower() == 'true'
        }
    
    def process_narrative_to_animation(self, custom_narrative_path: str = None) -> Dict:
        """
        Complete pipeline: narrative script → advanced parsing → Manim code generation
        """
        print("\n" + "="*60)
        print("🎬 ADVANCED NARRATIVE-TO-MANIM PROCESSING")
        print("="*60)
        
        try:
            # Step 1: Load and validate narrative script
            narrative_path = custom_narrative_path or self.config['narrative_path']
            narrative_script = self._load_narrative_script(narrative_path)
            
            # Step 2: Load additional context (metadata, images)
            metadata = self._load_metadata()
            available_images = self._get_available_images()
            
            print(f"📊 Loaded narrative: {len(narrative_script)} characters")
            print(f"🖼️ Found images: {len(available_images)}")
            
            # Step 3: Advanced narrative parsing
            print("\n🔍 Advanced Narrative Analysis...")
            parsed_data = self.parser.parse_narrative_script(narrative_script)
            
            # Export analysis report
            analysis_file = "narrative_analysis_report.json"
            self.parser.export_analysis_report(parsed_data, analysis_file)
            
            # Step 4: Generate Manim code
            print("\n🤖 Generating Manim Code...")
            generated_code = self.code_generator.generate_manim_code(
                narrative_script=narrative_script,
                images_folder=self.config['images_folder'],
                metadata=metadata
            )
            
            # Step 5: Save generated code
            output_path = self.config['output_file']
            self._save_generated_code(generated_code, output_path)
            
            # Step 6: Generate execution instructions
            instructions = self._generate_execution_instructions(output_path)
            
            # Compile results
            results = {
                'success': True,
                'narrative_file': narrative_path,
                'output_file': output_path,
                'analysis_file': analysis_file,
                'parsed_sections': len(parsed_data['sections']),
                'estimated_duration': parsed_data['metadata']['total_duration'],
                'complexity_score': parsed_data['metadata']['complexity_score'],
                'code_length': len(generated_code),
                'available_images': len(available_images),
                'execution_instructions': instructions
            }
            
            self._print_success_summary(results)
            return results
            
        except Exception as e:
            error_msg = f"❌ Error in processing pipeline: {str(e)}"
            print(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'narrative_file': narrative_path if 'narrative_path' in locals() else None
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
    
    def _load_metadata(self) -> Dict:
        """Load additional metadata if available"""
        metadata_path = self.config['metadata_path']
        
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load metadata: {e}")
        
        return {}
    
    def _get_available_images(self) -> list:
        """Get list of available images"""
        images_folder = self.config['images_folder']
        
        if not os.path.exists(images_folder):
            print(f"⚠️ Images folder not found: {images_folder}")
            return []
        
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        images = []
        
        for file in os.listdir(images_folder):
            if file.lower().endswith(image_extensions):
                images.append(file)
        
        return images
    
    def _save_generated_code(self, code: str, output_path: str) -> None:
        """Save generated Manim code with backup"""
        # Create backup if file exists
        if os.path.exists(output_path):
            backup_path = f"{output_path}.backup"
            os.rename(output_path, backup_path)
            print(f"📋 Created backup: {backup_path}")
        
        # Save new code
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"💾 Saved generated code: {output_path}")
    
    def _generate_execution_instructions(self, manim_file: str) -> Dict:
        """Generate instructions for running the generated code"""
        base_name = Path(manim_file).stem
        
        instructions = {
            'preview_command': f"manim {manim_file} -pql --disable_caching",
            'high_quality_command': f"manim {manim_file} -pqh --disable_caching",
            'class_name': "NarrativeEducationalAnimation",
            'requirements': [
                "Manim 0.19.0 or later",
                "manim-voiceover[gtts] 0.3.7 or later", 
                "Active internet connection (for GTTS)",
                "Python 3.11+ recommended"
            ],
            'troubleshooting': {
                'caching_issue': "Always use --disable_caching flag with manim-voiceover",
                'import_error': "Check that all dependencies are installed correctly",
                'tts_error': "Ensure internet connection for Google TTS service",
                'image_error': "Check that image paths are correct and files exist"
            }
        }
        
        return instructions
    
    def _print_success_summary(self, results: Dict) -> None:
        """Print detailed success summary"""
        print("\n" + "="*60)
        print("🎉 GENERATION COMPLETE!")
        print("="*60)
        
        print(f"📊 Sections processed: {results['parsed_sections']}")
        print(f"⏱️ Estimated video duration: {results['estimated_duration']:.1f} seconds")
        print(f"🎯 Complexity score: {results['complexity_score']:.2f}")
        print(f"📝 Generated code length: {results['code_length']:,} characters")
        print(f"🖼️ Images available: {results['available_images']}")
        
        print(f"\n📁 Files created:")
        print(f"   • Main code: {results['output_file']}")
        print(f"   • Analysis: {results['analysis_file']}")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Review: {results['output_file']}")
        print(f"   2. Test run: {results['execution_instructions']['preview_command']}")
        print(f"   3. High quality: {results['execution_instructions']['high_quality_command']}")
        
        print(f"\n💡 Tips:")
        for tip in results['execution_instructions']['requirements']:
            print(f"   • {tip}")


def main():
    """Main execution function with command line interface"""
    print("🎥 Advanced Narrative-to-Manim System")
    print("🔬 Powered by advanced parsing & latest AI models")
    
    try:
        # Initialize system
        system = AdvancedNarrativeToManimSystem()
        
        # Check for custom narrative file argument
        custom_narrative = None
        if len(sys.argv) > 1:
            custom_narrative = sys.argv[1]
            print(f"📖 Using custom narrative: {custom_narrative}")
        
        # Process narrative to animation
        results = system.process_narrative_to_animation(custom_narrative)
        
        if results['success']:
            print("\n✨ Ready to create amazing educational videos!")
            return 0
        else:
            print(f"\n❌ Processing failed: {results.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"\n💥 System error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

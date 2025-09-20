#!/usr/bin/env python3
"""
Professional Educational Script Generator
Compatible with Google GenAI SDK 1.19.0+ (2025)
Generates engaging, child-friendly educational narratives
"""

import os
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Updated Google GenAI SDK imports
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

class EducationalScriptGenerator:
    """
    Professional educational script generator with enhanced capabilities
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        
        # Configuration paths with fallbacks
        self.config = {
            'json_metadata_path': os.getenv('JSON_METADATA_PATH', 'output/metadata.json'),
            'markdown_path': os.getenv('MARKDOWN_PATH', 'output/content.md'),
            'prompt_file_path': os.getenv('PROMPT_FILE_PATH', 'prompts/script_prompt.txt'),
            'output_script_path': os.getenv('OUTPUT_SCRIPT_PATH', 'output/generated_narrative_script.txt'),
            'output_dir': os.getenv('OUTPUT_DIR', 'output')
        }
        
        # Ensure output directory exists
        Path(self.config['output_dir']).mkdir(parents=True, exist_ok=True)
    
    def generate_educational_script(self, user_query: str, 
                                  custom_markdown_path: Optional[str] = None,
                                  custom_metadata_path: Optional[str] = None) -> Dict:
        """
        Generate professional educational script from user query and content
        """
        print("🎬 Starting Educational Script Generation")
        print("="*60)
        
        try:
            # Load content and metadata
            content_result = self._load_content(custom_markdown_path, custom_metadata_path)
            
            if not content_result['success']:
                return content_result
            
            # Create comprehensive prompt
            prompt = self._create_educational_prompt(
                user_query=user_query,
                markdown_content=content_result['markdown_content'],
                metadata=content_result['metadata']
            )
            
            print(f"📝 Query: {user_query}")
            print(f"📄 Content: {len(content_result['markdown_content'])} characters")
            print(f"🎯 Generating professional educational script...")
            
            # Generate script with Gemini
            generated_script = self._generate_with_gemini(prompt)
            
            if not generated_script:
                return {'success': False, 'error': 'Failed to generate script content'}
            
            # Enhance and validate the script
            enhanced_script = self._enhance_script_quality(generated_script, user_query)
            
            # Save the script
            output_path = self._save_script(enhanced_script)
            
            # Generate analysis report
            analysis = self._analyze_generated_script(enhanced_script)
            
            result = {
                'success': True,
                'script_path': output_path,
                'script_length': len(enhanced_script),
                'estimated_duration': analysis['estimated_duration'],
                'section_count': analysis['section_count'],
                'word_count': analysis['word_count'],
                'visual_cues': analysis['visual_cues'],
                'query': user_query
            }
            
            self._print_success_summary(result)
            return result
            
        except Exception as e:
            error_msg = f"❌ Script generation failed: {str(e)}"
            print(error_msg)
            return {'success': False, 'error': error_msg}
    
    def _load_content(self, custom_markdown_path: Optional[str] = None,
                     custom_metadata_path: Optional[str] = None) -> Dict:
        """Load and process content files"""
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
            
            # Load metadata
            metadata_path = custom_metadata_path or self.config['json_metadata_path']
            metadata = self._load_and_process_metadata(metadata_path)
            
            print(f"✅ Content loaded successfully")
            print(f"   📄 Markdown: {len(markdown_content)} characters")
            print(f"   📊 Metadata: {len(json.dumps(metadata))} characters")
            
            return {
                'success': True,
                'markdown_content': markdown_content,
                'metadata': metadata
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error loading content: {str(e)}'
            }
    
    def _load_and_process_metadata(self, metadata_path: str) -> Dict:
        """Load and enhance metadata with visual summaries"""
        try:
            if not os.path.exists(metadata_path):
                print(f"⚠️ Metadata file not found: {metadata_path}")
                return {"image_summary_for_llm": "No metadata file available."}
            
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Enhance metadata with image summary
            if "images" in metadata and isinstance(metadata["images"], list):
                image_summaries = []
                image_summaries.append(f"📸 Document contains {len(metadata['images'])} visual elements:")
                
                for img in metadata["images"]:
                    img_name = img.get("image_name", "Unknown")
                    context = img.get("context_type", "general")
                    keywords = ", ".join(img.get("keywords", []))
                    description = img.get("description", "No description")
                    
                    image_summaries.append(
                        f"  • {img_name} ({context}): {description}"
                        f"{' [Keywords: ' + keywords + ']' if keywords else ''}"
                    )
                
                metadata["image_summary_for_llm"] = "\n".join(image_summaries)
            else:
                metadata["image_summary_for_llm"] = "No visual elements metadata available."
            
            return metadata
            
        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON in metadata file: {metadata_path}")
            return {"image_summary_for_llm": "Invalid metadata file format."}
        except Exception as e:
            print(f"⚠️ Error processing metadata: {e}")
            return {"image_summary_for_llm": f"Error loading metadata: {e}"}
    
    def _create_educational_prompt(self, user_query: str, markdown_content: str, metadata: Dict) -> str:
        """Create comprehensive educational script generation prompt"""
        
        prompt = f"""# PROFESSIONAL EDUCATIONAL SCRIPT GENERATOR

## MISSION
Create a compelling, child-friendly educational narrative script for a professional animated video that explains "{user_query}" in an engaging and comprehensive way.

## CRITICAL REQUIREMENTS

### 1. AUDIENCE & TONE
- **Target audience**: Students aged 10-16 (child-friendly language)
- **Tone**: Enthusiastic, encouraging, and accessible
- **Style**: Conversational yet informative
- **Language**: Clear, simple sentences with technical terms explained

### 2. SCRIPT STRUCTURE
Use this EXACT section format:

```
## Introduction
[Engaging hook, welcome, topic overview - 30-45 seconds]

## Core Concepts  
[Main theoretical explanations - 60-90 seconds]

## Mathematical Derivations
[Step-by-step math explanations if applicable - 45-75 seconds]

## Examples
[Practical examples and demonstrations - 45-60 seconds]

## Applications
[Real-world uses and importance - 60-90 seconds]

## Conclusion
[Summary and call to action - 30-45 seconds]
```

### 3. VISUAL CUE INTEGRATION
Include these visual cues throughout the script:

**Image cues**: `[DISPLAY IMAGE: description.png]`
**Diagram cues**: `[DISPLAY DIAGRAM: Graph of equation]`
**Animation cues**: `[ANIMATE: process or concept]`
**Emphasis cues**: `[HIGHLIGHT: important term]`
**Pause cues**: `[SHORT PAUSE]`, `[MEDIUM PAUSE]`, `[LONG PAUSE]`

### 4. MATHEMATICAL CONTENT (if applicable)
- Write all equations clearly: "y equals m x plus b"
- Explain each variable: "where y is the output, x is the input..."
- Break complex formulas into steps
- Use analogies for difficult concepts

### 5. ENGAGEMENT TECHNIQUES
- Start with relatable questions or scenarios
- Use analogies and metaphors
- Include "imagine" scenarios  
- Ask rhetorical questions
- Build excitement about the topic

### 6. TECHNICAL REQUIREMENTS
- **Duration**: Aim for 5-8 minutes total (approximately 750-1200 words)
- **Pacing**: Vary sentence length and complexity
- **Transitions**: Smooth flow between sections
- **Clarity**: Each concept explained before building on it

## CONTENT TO WORK WITH

### User Query/Focus:
"{user_query}"

### Source Content:
{markdown_content}

### Available Visual Elements:
{metadata.get('image_summary_for_llm', 'No visual elements available')}

## EXAMPLE OUTPUT FORMAT

```
## Introduction

(Upbeat intro music with animated graphics)

Hey everyone, and welcome to our exciting journey into [topic]! Have you ever wondered how [relatable scenario]? Well, today we're going to unlock the secrets behind [main concept]. [SHORT PAUSE]

By the end of this video, you'll understand not just what [topic] is, but how it works and why it's so important in our daily lives. Get ready to have your mind blown! [MEDIUM PAUSE]

## Core Concepts

So, what exactly is [main concept]? [DISPLAY DIAGRAM: Basic concept illustration] Think of it like [analogy]. [SHORT PAUSE]

The fundamental idea is that [explanation]. This means [practical meaning]. [HIGHLIGHT: key term] [MEDIUM PAUSE]

Let's break this down step by step...

[Continue with detailed explanations]

## [Continue with other sections...]
```

## OUTPUT REQUIREMENTS

Generate ONLY the complete narrative script that:
✅ Follows the exact section structure
✅ Uses child-friendly, engaging language
✅ Includes appropriate visual cues
✅ Explains complex concepts clearly
✅ Maintains consistent enthusiasm
✅ Provides comprehensive topic coverage
✅ Is perfectly suited for Manim animation

Do NOT include explanations or meta-commentary. Start directly with "## Introduction".
"""

        return prompt
    
    def _generate_with_gemini(self, prompt: str) -> Optional[str]:
        """Generate script using Gemini 2.0 with robust error handling"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
                config=types.GenerateContentConfig(
                    temperature=0.8,  # Higher creativity for engaging content
                    max_output_tokens=8192,
                    top_k=40,
                    top_p=0.9,
                ),
            )
            
            if response.candidates and response.candidates[0].content.parts:
                generated_text = response.candidates[0].content.parts[0].text
                print("✅ Script generated successfully with Gemini 2.0")
                return generated_text
            else:
                print("⚠️ Gemini returned empty response")
                return None
                
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return None
    
    def _enhance_script_quality(self, script: str, user_query: str) -> str:
        """Enhance the generated script for better quality"""
        enhancements = []
        
        # Ensure proper section structure
        sections = ['Introduction', 'Core Concepts', 'Mathematical Derivations', 
                   'Examples', 'Applications', 'Conclusion']
        
        for section in sections:
            if f'## {section}' not in script:
                # Add missing section
                if section == 'Mathematical Derivations' and 'math' not in user_query.lower():
                    continue  # Skip math section for non-mathematical topics
                
                script += f'\n\n## {section}\n\n[This section needs content about {section.lower()} for {user_query}]\n'
                enhancements.append(f'Added missing {section} section')
        
        # Ensure proper pause formatting
        script = re.sub(r'\[PAUSE\]', '[MEDIUM PAUSE]', script)
        script = re.sub(r'\[pause\]', '[MEDIUM PAUSE]', script)
        
        # Enhance visual cues formatting
        script = re.sub(r'\[SHOW:', '[DISPLAY IMAGE:', script)
        script = re.sub(r'\[DIAGRAM:', '[DISPLAY DIAGRAM:', script)
        
        # Add engagement elements if missing
        if 'Hey everyone' not in script and 'Welcome' not in script:
            script = script.replace('## Introduction', 
                                  '## Introduction\n\nHey everyone, and welcome! ')
            enhancements.append('Added engaging introduction')
        
        if enhancements:
            print(f"🔧 Script enhancements: {', '.join(enhancements)}")
        
        return script
    
    def _save_script(self, script: str) -> str:
        """Save the generated script to file"""
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
    
    def _analyze_generated_script(self, script: str) -> Dict:
        """Analyze the generated script for quality metrics"""
        lines = script.split('\n')
        
        # Count sections
        sections = [line for line in lines if line.startswith('## ')]
        
        # Count words (approximate duration: ~150 words per minute for narration)
        words = len(script.split())
        estimated_duration = words / 150 * 60  # Convert to seconds
        
        # Count visual cues
        visual_cues = {
            'images': len(re.findall(r'\[DISPLAY IMAGE:', script)),
            'diagrams': len(re.findall(r'\[DISPLAY DIAGRAM:', script)),
            'animations': len(re.findall(r'\[ANIMATE:', script)),
            'highlights': len(re.findall(r'\[HIGHLIGHT:', script)),
            'pauses': len(re.findall(r'\[(SHORT|MEDIUM|LONG) PAUSE\]', script))
        }
        
        return {
            'section_count': len(sections),
            'word_count': words,
            'estimated_duration': estimated_duration,
            'visual_cues': visual_cues,
            'sections': [s.replace('## ', '') for s in sections]
        }
    
    def _print_success_summary(self, result: Dict):
        """Print comprehensive success summary"""
        print("\n" + "="*60)
        print("🎉 EDUCATIONAL SCRIPT GENERATION COMPLETE!")
        print("="*60)
        
        print(f"📝 Topic: {result['query']}")
        print(f"📄 Script length: {result['script_length']:,} characters")
        print(f"📊 Word count: {result['word_count']} words")
        print(f"⏱️ Estimated duration: {result['estimated_duration']:.1f} seconds")
        print(f"📚 Sections: {result['section_count']}")
        
        print(f"\n🎨 Visual elements:")
        for cue_type, count in result['visual_cues'].items():
            if count > 0:
                print(f"   • {cue_type.title()}: {count}")
        
        print(f"\n📁 Output file: {result['script_path']}")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Review the generated script")
        print(f"   2. Run the Manim code generator")
        print(f"   3. Generate your educational video!")
        
        print(f"\n💡 The script is ready for professional animation!")


def main():
    """Main execution function with enhanced CLI"""
    print("🎬 Professional Educational Script Generator")
    print("🚀 Powered by Google Gemini 2.0 Flash")
    print("="*60)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: Google API key not found!")
        print("   Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
        print("   Example: export GOOGLE_API_KEY='your_api_key_here'")
        return 1
    
    try:
        # Initialize generator
        generator = EducationalScriptGenerator(api_key)
        
        # Get user input
        if len(sys.argv) > 1:
            user_query = ' '.join(sys.argv[1:])
            print(f"📖 Using command line topic: {user_query}")
        else:
            user_query = input("🎯 Enter the educational topic/concept to explain: ").strip()
        
        if not user_query:
            print("❌ Error: Topic cannot be empty!")
            return 1
        
        # Optional custom paths
        custom_markdown = input("📄 Custom markdown file path (press Enter for default): ").strip() or None
        custom_metadata = input("📊 Custom metadata file path (press Enter for default): ").strip() or None
        
        # Generate the script
        result = generator.generate_educational_script(
            user_query=user_query,
            custom_markdown_path=custom_markdown,
            custom_metadata_path=custom_metadata
        )
        
        if result['success']:
            print("\n✨ Ready to create amazing educational videos!")
            return 0
        else:
            print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n👋 Script generation cancelled by user")
        return 0
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
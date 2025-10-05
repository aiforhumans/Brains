"""
Smart Prompt Helper — Beginner-friendly prompt enhancement node.

This node transforms simple prompts into detailed, high-quality prompts using
the knowledge stored in BRAIN memory.
"""
from typing import Any, Dict, Tuple

# Import the advanced BRAIN suggest node
try:
    from .brain_datatype import BrainData, BrainsXDEV_PromptBrainSuggestDirect
    BRAIN_AVAILABLE = True
except ImportError:
    BRAIN_AVAILABLE = False
    BrainData = None


class BrainsXDEV_SmartPromptHelper:
    """
    Smart Prompt Helper - Transform simple prompts into detailed ones.
    
    Uses AI learning from your BRAIN memory to suggest relevant keywords
    and create high-quality prompt variations.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "smart_memory": ("BRAIN",),
                "basic_prompt": ("STRING", {
                    "default": "a beautiful landscape",
                    "multiline": True,
                }),
                "creativity_level": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "display": "slider",
                }),
            },
            "optional": {
                "preferred_style": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("improved_prompt_1", "improved_prompt_2", "improved_prompt_3", "explanation")
    FUNCTION = "enhance_prompt"
    CATEGORY = "Brains-XDEV/Beginner"
    NODE_NAME = "SmartPromptHelper"
    
    def enhance_prompt(
        self,
        smart_memory: Any,
        basic_prompt: str,
        creativity_level: float,
        preferred_style: str = "",
    ) -> Tuple[str, str, str, str]:
        """
        Transform a basic prompt into multiple enhanced versions.
        
        Args:
            smart_memory: BrainData object with learned knowledge
            basic_prompt: Simple prompt to enhance
            creativity_level: 0.0-1.0, controls variation
            preferred_style: Optional style preference
            
        Returns:
            Tuple of (improved_prompt_1, improved_prompt_2, improved_prompt_3, explanation)
        """
        if not BRAIN_AVAILABLE:
            error_msg = "❌ BRAIN system not available"
            return (basic_prompt, basic_prompt, basic_prompt, error_msg)
        
        if smart_memory is None:
            error_msg = "❌ No Smart Memory provided. Connect a Smart Memory Loader."
            return (basic_prompt, basic_prompt, basic_prompt, error_msg)
        
        try:
            # Use the advanced PromptBrainSuggestDirect node
            suggest_node = BrainsXDEV_PromptBrainSuggestDirect()
            
            # Get suggestions
            result = suggest_node.suggest_direct(
                brain_data=smart_memory,
                base_prompt=basic_prompt,
                suggestion_count=3,
                creativity=creativity_level,
                target_style=preferred_style if preferred_style != "any" else "none",
                quality_threshold=0.3,
            )
            
            # Unpack result (brain_data, suggestion_1, suggestion_2, suggestion_3)
            _, s1, s2, s3 = result
            
            # Generate explanation
            explanation = self._generate_explanation(
                basic_prompt,
                creativity_level,
                preferred_style
            )
            
            print(f"[Brains-XDEV] ✨ Generated 3 enhanced prompts")
            
            return (s1, s2, s3, explanation)
            
        except Exception as e:
            print(f"[Brains-XDEV] ❌ Error enhancing prompt: {e}")
            import traceback
            traceback.print_exc()
            error_msg = f"❌ Error: {str(e)}"
            return (basic_prompt, basic_prompt, basic_prompt, error_msg)
    
    def _generate_explanation(self, basic_prompt, creativity, style):
        """Generate explanation for the suggestions."""
        explanation = f"""✨ Smart Prompt Enhancement

Original: "{basic_prompt}"

Settings:
• Creativity Level: {creativity:.1f}/1.0 """
        
        if creativity < 0.3:
            explanation += "(Conservative - safe, proven keywords)"
        elif creativity < 0.7:
            explanation += "(Balanced - mix of proven + creative)"
        else:
            explanation += "(Experimental - bold, unique combinations)"
        
        if style:
            explanation += f"\n• Preferred Style: {style}"
        
        explanation += "\n\nThe AI analyzed your BRAIN memory and enhanced your prompt with:"
        explanation += "\n• Relevant keywords from successful past generations"
        explanation += "\n• Style-appropriate modifiers"
        explanation += "\n• Quality-enhancing terms"
        explanation += "\n\n💡 Tip: Try all three variations to see which works best!"
        
        return explanation


# Export for registration
__all__ = ["BrainsXDEV_SmartPromptHelper"]

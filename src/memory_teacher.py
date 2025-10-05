"""
Memory Teacher — Simple 1-5 star rating system for teaching your Smart Memory

A beginner-friendly wrapper for BrainsXDEV_PromptBrainLearnDirect that uses
an intuitive star rating system instead of technical scores.

How it works:
1. Connect your Smart Memory from the Smart Memory Loader
2. Type or paste your prompt
3. Give it a star rating (1-5 stars)
4. Optional: Pick the art style category
5. The Smart Memory learns from your rating!

Example workflow:
- Smart Memory Loader → Memory Teacher → updated Smart Memory
- Rate different prompts with 1-5 stars to teach preferences
"""
from typing import Tuple

# Import the advanced node we're wrapping
try:
    from .brain_datatype import BrainsXDEV_PromptBrainLearnDirect, BrainData
except ImportError:
    print("[Brains-XDEV] Warning: brain_datatype not found for Memory Teacher")
    BrainsXDEV_PromptBrainLearnDirect = None
    BrainData = None


class BrainsXDEV_MemoryTeacher:
    """
    Beginner-friendly learning node with 1-5 star ratings
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "smart_memory": ("BRAIN", {
                    "tooltip": "The Smart Memory to teach (from Smart Memory Loader)"
                }),
                "prompt_to_rate": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "The prompt you want to rate and teach"
                }),
                "star_rating": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "tooltip": "⭐ 1=Poor, 2=Fair, 3=Good, 4=Great, 5=Excellent"
                }),
            },
            "optional": {
                "art_style": (["any", "photorealistic", "artistic", "anime", "fantasy", 
                             "portrait", "landscape", "cinematic", "vintage", "modern", 
                             "abstract", "minimalist"], {
                    "default": "any",
                    "tooltip": "What art style is this prompt for?"
                }),
            }
        }
    
    RETURN_TYPES = ("BRAIN", "STRING")
    RETURN_NAMES = ("updated_memory", "learning_report")
    FUNCTION = "teach"
    CATEGORY = "Brains-XDEV/Beginner"
    NODE_NAME = "BrainsXDEV_MemoryTeacher"
    DESCRIPTION = "Teach your Smart Memory with simple 1-5 star ratings"
    
    def teach(self, smart_memory, prompt_to_rate: str, star_rating: int, 
             art_style: str = "any") -> Tuple:
        """
        Teach the Smart Memory with a star rating
        
        Args:
            smart_memory: BRAIN data from Smart Memory Loader
            prompt_to_rate: The prompt text to rate
            star_rating: 1-5 stars
            art_style: Optional art style category
            
        Returns:
            (updated_memory, learning_report) tuple
        """
        
        # Check if advanced node is available
        if BrainsXDEV_PromptBrainLearnDirect is None:
            error_msg = "❌ Memory Teacher unavailable. Check brain_datatype.py installation."
            return (smart_memory, error_msg)
        
        # Validate inputs
        if smart_memory is None:
            error_msg = "❌ No Smart Memory provided. Connect a Smart Memory Loader."
            return (None, error_msg)
        
        if not prompt_to_rate or prompt_to_rate.strip() == "":
            error_msg = "❌ Please enter a prompt to rate."
            return (smart_memory, error_msg)
        
        # Validate star rating
        if star_rating < 1 or star_rating > 5:
            error_msg = f"❌ Star rating must be 1-5. Got: {star_rating}"
            return (smart_memory, error_msg)
        
        try:
            # Convert star rating to score (0.0-1.0 scale)
            # 1 star = 0.1, 2 stars = 0.3, 3 stars = 0.5, 4 stars = 0.7, 5 stars = 0.9
            star_to_score = {
                1: 0.1,  # Poor
                2: 0.3,  # Fair
                3: 0.5,  # Good
                4: 0.7,  # Great
                5: 0.9   # Excellent
            }
            score = star_to_score[star_rating]
            
            # Use the advanced PromptBrainLearnDirect node
            learn_node = BrainsXDEV_PromptBrainLearnDirect()
            
            # Call the learning function
            result = learn_node.learn_direct(
                brain_data=smart_memory,
                prompt=prompt_to_rate,
                score=score,
                style_category=art_style if art_style != "any" else "none",
                feature_emphasis="none",
                learning_rate=1.0
            )
            
            # Unpack result (brain_data, status)
            updated_brain, status = result
            
            # Create beginner-friendly report
            stars_display = "⭐" * star_rating
            report = f"""🎓 Learning Complete!

Rating: {stars_display} ({star_rating} stars)
Score: {score:.1f}/1.0

Prompt: {prompt_to_rate[:100]}{'...' if len(prompt_to_rate) > 100 else ''}

Style: {art_style if art_style != "any" else "General"}

Status: {status}

Your Smart Memory has learned from this rating!
Keep rating more prompts to improve suggestions.
"""
            
            print(f"[Brains-XDEV] 🎓 Memory Teacher: {stars_display} rating recorded")
            
            return (updated_brain, report)
            
        except Exception as e:
            error_msg = f"❌ Error during learning: {str(e)}"
            print(f"[Brains-XDEV] {error_msg}")
            return (smart_memory, error_msg)


# Export for registration
NODE_CLASS_MAPPINGS = {
    "BrainsXDEV_MemoryTeacher": BrainsXDEV_MemoryTeacher,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BrainsXDEV_MemoryTeacher": "Brains-XDEV • Memory Teacher (beginner)",
}

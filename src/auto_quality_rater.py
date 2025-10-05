"""
Auto Quality Rater — Automatic image quality scoring using AI

A beginner-friendly wrapper for BrainsXDEV_PromptBrainQualityScore that provides
simple automatic quality ratings for generated images.

How it works:
1. Connect your generated image
2. Add the prompt that created it
3. Choose what type of rating you want (overall quality, artistic merit, technical quality)
4. Get an automatic 0-10 quality score!

Example workflow:
- KSampler → Image → Auto Quality Rater → quality score + report
- Use the score to filter good vs bad generations
- Feed scores back to Memory Teacher for automated learning
"""
from typing import Tuple, Any

# Import the advanced node we're wrapping
try:
    from .brain_datatype import BrainsXDEV_PromptBrainQualityScore
except ImportError:
    print("[Brains-XDEV] Warning: brain_datatype not found for Auto Quality Rater")
    BrainsXDEV_PromptBrainQualityScore = None


class BrainsXDEV_AutoQualityRater:
    """
    Beginner-friendly automatic image quality rating
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "generated_image": ("IMAGE", {
                    "tooltip": "The image you want to rate"
                }),
                "image_description": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "The prompt that created this image (helps AI understand what you wanted)"
                }),
            },
            "optional": {
                "rating_focus": (["overall_quality", "artistic_merit", "technical_quality", 
                                "prompt_adherence", "creativity", "composition"], {
                    "default": "overall_quality",
                    "tooltip": "What should the AI focus on when rating?"
                }),
                "strict_mode": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "True = stricter ratings, False = more forgiving"
                }),
            }
        }
    
    RETURN_TYPES = ("FLOAT", "STRING", "STRING")
    RETURN_NAMES = ("quality_score", "rating_report", "quality_grade")
    FUNCTION = "rate_image"
    CATEGORY = "Brains-XDEV/Beginner"
    NODE_NAME = "BrainsXDEV_AutoQualityRater"
    DESCRIPTION = "Automatically rate image quality with AI (0-10 scale)"
    
    def rate_image(self, generated_image, image_description: str, 
                  rating_focus: str = "overall_quality",
                  strict_mode: bool = False) -> Tuple:
        """
        Automatically rate image quality
        
        Args:
            generated_image: IMAGE tensor from generation
            image_description: Prompt that created the image
            rating_focus: What aspect to focus rating on
            strict_mode: Use stricter or more forgiving scoring
            
        Returns:
            (quality_score, rating_report, quality_grade) tuple
        """
        
        # Check if advanced node is available
        if BrainsXDEV_PromptBrainQualityScore is None:
            error_msg = "❌ Auto Quality Rater unavailable. Check brain_datatype.py installation."
            return (0.0, error_msg, "ERROR")
        
        # Validate inputs
        if generated_image is None:
            error_msg = "❌ No image provided. Connect an image output."
            return (0.0, error_msg, "ERROR")
        
        try:
            # Use the advanced PromptBrainQualityScore node
            quality_node = BrainsXDEV_PromptBrainQualityScore()
            
            # Set scoring model based on strict mode
            scoring_model = "conservative" if strict_mode else "balanced"
            
            # Call the quality analysis function
            result = quality_node.analyze_quality(
                image=generated_image,
                caption=image_description,
                scoring_criteria=rating_focus,
                analysis_depth="standard",
                scoring_model=scoring_model,
                score_boost=0.0,
                minimum_score=0.0,
                enable_histogram_analysis=True,
                enable_composition_analysis=True,
                enable_noise_detection=True,
                enable_semantic_analysis=bool(image_description.strip())
            )
            
            # Unpack result (quality_score, detailed_analysis, quality_grade, technical_score, artistic_score, semantic_score)
            raw_score, detailed_analysis, grade, tech_score, art_score, sem_score = result
            
            # Convert 0.0-1.0 score to 0-10 scale for beginners
            score_0_to_10 = raw_score * 10.0
            
            # Create beginner-friendly report
            grade_emoji = {
                "F": "💔",
                "D": "😞",
                "C": "😐",
                "B": "🙂",
                "A": "😊",
                "S": "🌟"
            }
            emoji = grade_emoji.get(grade, "❓")
            
            report = f"""🎯 Auto Quality Rating

Overall Score: {score_0_to_10:.1f}/10 {emoji}
Grade: {grade}

📊 Detailed Scores:
• Technical Quality: {tech_score * 10:.1f}/10
• Artistic Merit: {art_score * 10:.1f}/10
• Prompt Match: {sem_score * 10:.1f}/10

Rating Focus: {rating_focus.replace('_', ' ').title()}
Mode: {'Strict' if strict_mode else 'Balanced'}

{detailed_analysis[:500]}{'...' if len(detailed_analysis) > 500 else ''}

💡 Tip: Scores 7+ are excellent, 4-7 are good, below 4 need work.
"""
            
            print(f"[Brains-XDEV] 🎯 Auto Quality Rater: {score_0_to_10:.1f}/10 ({grade})")
            
            return (score_0_to_10, report, grade)
            
        except Exception as e:
            error_msg = f"❌ Error during quality rating: {str(e)}"
            print(f"[Brains-XDEV] {error_msg}")
            import traceback
            traceback.print_exc()
            return (0.0, error_msg, "ERROR")


# Export for registration
NODE_CLASS_MAPPINGS = {
    "BrainsXDEV_AutoQualityRater": BrainsXDEV_AutoQualityRater,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BrainsXDEV_AutoQualityRater": "Brains-XDEV • Auto Quality Rater (beginner)",
}

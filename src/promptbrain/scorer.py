"""
Brains-XDEV PromptBrain — Scorer (manual)

Provides a manual score for feedback learning (0..1). 
Could be replaced by a UI widget or external rating source.

Migrated from BRAIN project with Brains-XDEV naming conventions.
"""
from typing import Any, Dict, Tuple

print("[Brains-XDEV] scorer import")

class BrainsXDEV_Scorer:
    """
    Manual scoring node for feedback learning.
    Allows users to provide numerical scores and notes for quality assessment.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "score": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "notes": ("STRING", {"default": ""}),
            },
            "optional": {},
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("FLOAT", "STRING")
    RETURN_NAMES = ("score", "notes")
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_Scorer"
    
    def run(self, score: float, notes: str, 
            prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[float, str]:
        """
        Return the manually provided score and notes.
        This allows human feedback to be incorporated into the PromptBrain system.
        """
        return (float(score), notes)
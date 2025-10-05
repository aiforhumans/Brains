"""
PromptBrain — Scorer (manual)
Provides a manual score for feedback learning (0..1). Could be replaced by a UI widget or external rating source.
"""
from typing import Any, Dict, Tuple
class PB_Scorer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "score": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "notes": ("STRING", {"default": ""}),
            },
            "optional": {},
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
    RETURN_TYPES = ("FLOAT","STRING")
    RETURN_NAMES = ("score","notes")
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_Scorer"
    def run(self, score: float, notes: str, unique_id=None):
        return float(score), notes

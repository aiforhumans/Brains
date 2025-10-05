"""
PromptBrain — Captioner (stub)
References:
- BLIP captioning: https://huggingface.co/Salesforce/blip-image-captioning-base
- Florence-2 tasks: https://huggingface.co/microsoft/Florence-2-base
"""
from typing import Any, Dict, Tuple, List
import numpy as np

class PB_Captioner:
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "image": ("IMAGE", {}),
                "model_hint": (["florence2","blip","external"],),
            },
            "optional": {
                "prompt": ("STRING", {"default": "Describe the image"}),
            },
            "hidden": {"unique_id": "UNIQUE_ID"}
        }

    RETURN_TYPES = ("STRING", "DICT")
    RETURN_NAMES = ("caption", "metadata")
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_Captioner"

    def run(self, image, model_hint: str, prompt: str = "Describe the image", unique_id=None):
        # Stub: return deterministic placeholder caption for wiring/tests.
        caption = f"[{model_hint}] {prompt}."
        meta = {"model_hint": model_hint, "uid": unique_id}
        return (caption, meta)

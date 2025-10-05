"""
Brains-XDEV PromptBrain — Captioner (stub)

Stub implementation for image captioning. This version provides the interface
but returns placeholder captions for testing and workflow design purposes.

Migrated from BRAIN project with Brains-XDEV naming conventions.

References:
- BLIP captioning: https://huggingface.co/Salesforce/blip-image-captioning-base
- Florence-2 tasks: https://huggingface.co/microsoft/Florence-2-base
"""
from typing import Any, Dict, Tuple, List
import numpy as np

print("[Brains-XDEV] captioner stub import")

class BrainsXDEV_Captioner:
    """
    Image captioning stub node that provides interface compatibility.
    Returns placeholder captions for workflow design and testing.
    Replace with actual model inference for production use.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "image": ("IMAGE", {}),
                "model_hint": (["florence2", "blip", "external", "mock"], {"default": "mock"}),
            },
            "optional": {
                "caption_prompt": ("STRING", {"default": "Describe the image"}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("STRING", "DICT")
    RETURN_NAMES = ("caption", "metadata")
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_Captioner"

    def run(self, image, model_hint: str, caption_prompt: str = "Describe the image", 
            prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[str, Dict]:
        """
        Stub implementation: return placeholder caption.
        Replace with actual model inference for production.
        """
        
        # Generate mock captions based on model hint
        if model_hint == "mock":
            caption = "A placeholder image caption for testing workflow design"
        elif model_hint == "florence2":
            caption = f"[Florence2] {caption_prompt}: A detailed scene analysis would appear here"
        elif model_hint == "blip":
            caption = f"[BLIP] A photo that shows {caption_prompt.lower()}"
        elif model_hint == "external":
            caption = f"[External] Caption from external model: {caption_prompt}"
        else:
            caption = f"[{model_hint}] {caption_prompt}"
        
        # Create metadata
        metadata = {
            "model_hint": model_hint,
            "prompt": caption_prompt,
            "uid": unique_id,
            "stub": True,
            "status": "placeholder"
        }
        
        return (caption, metadata)
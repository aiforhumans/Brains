"""
Brains-XDEV PromptBrain — WD14 Tagger (stub)

Stub implementation for WD14 image tagging. This version provides the interface
but returns empty results for testing and workflow design purposes.

Migrated from BRAIN project with Brains-XDEV naming conventions.

References:
- WD14 ComfyUI node: https://github.com/pythongosssss/ComfyUI-WD14-Tagger
- Hidden inputs & server props: https://docs.comfy.org/custom-nodes/backend/more_on_inputs
"""
from typing import Any, Dict, Tuple, List
import numpy as np

print("[Brains-XDEV] tagger stub import")

class BrainsXDEV_Tagger:
    """
    Emits a dict of tags -> scores (float 0..1) and a filtered, comma-joined string.
    This stub does not run a model; it passes through supplied tags (for unit tests & wiring).
    Replace with calls to ComfyUI-WD14-Tagger node or integrate ONNX runtime.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "image": ("IMAGE", {}),
                "min_conf": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
                "allow_list": ("STRING", {"default": ""}),  # optional whitelist (comma sep)
                "deny_list": ("STRING", {"default": ""}),   # optional blacklist (comma sep)
            },
            "optional": {},
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("STRING", "DICT")
    RETURN_NAMES = ("tags_text", "tags_dict")
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_Tagger"

    def run(self, image, min_conf: float, allow_list: str, deny_list: str, 
            prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[str, Dict]:
        """
        Stub implementation: return empty tags to keep workflow valid.
        Replace this with actual WD14 model inference.
        """
        
        # For debugging/testing, we can return some mock tags
        mock_tags = {
            "1girl": 0.95,
            "solo": 0.89,
            "simple_background": 0.75,
        } if allow_list == "mock" else {}
        
        # Filter tags based on confidence and allow/deny lists
        filtered_tags = {}
        for tag, score in mock_tags.items():
            if score < min_conf:
                continue
            if deny_list and tag in deny_list.split(","):
                continue
            if allow_list and allow_list != "mock" and tag not in allow_list.split(","):
                continue
            filtered_tags[tag] = score
        
        # Create comma-separated string
        tags_text = ", ".join(filtered_tags.keys())
        
        # Create result dict with metadata
        tags_dict = {
            "tags": filtered_tags,
            "min_conf": float(min_conf),
            "allow": allow_list,
            "deny": deny_list,
            "stub": True
        }
        
        return (tags_text, tags_dict)
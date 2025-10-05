"""
PromptBrain — WD14 Tagger (stub)
References:
- WD14 ComfyUI node: https://github.com/pythongosssss/ComfyUI-WD14-Tagger
- Hidden inputs & server props: https://docs.comfy.org/custom-nodes/backend/more_on_inputs
"""
from typing import Any, Dict, Tuple, List
import numpy as np

class PB_WD14Tagger:
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
            "hidden": {"unique_id": "UNIQUE_ID"}
        }

    RETURN_TYPES = ("STRING", "DICT")
    RETURN_NAMES = ("tags_text", "tags_dict")
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_WD14Tagger"

    def run(self, image, min_conf: float, allow_list: str, deny_list: str, unique_id=None):
        # Stub implementation: return empty tags to keep flow valid.
        return ("", {"tags": {}, "min_conf": float(min_conf), "allow": allow_list, "deny": deny_list})

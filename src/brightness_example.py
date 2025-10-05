"""
Brains-XDEV Brightness — minimal example custom node for ComfyUI.

Adjusted brightness of IMAGE inputs by adding a constant offset.
Adapted from the BRAIN project's basic_example.py following Brains-XDEV patterns.

Docs:
- Server properties (INPUT_TYPES/hidden/return types): https://docs.comfy.org/custom-nodes/backend/server_overview
- Hidden inputs (PROMPT/EXTRA_PNGINFO/UNIQUE_ID): https://docs.comfy.org/custom-nodes/backend/more_on_inputs
"""
from typing import Any, Dict, Tuple, List
import numpy as np

print("[Brains-XDEV] brightness example import")

class BrainsXDEV_Brightness:
    """
    Adjust brightness of an IMAGE (or batch of images) by adding a constant offset.
    The input IMAGE is expected to be a list of HxWxC float32 arrays in [0,1] (Comfy default).
    This implementation is intentionally simple and dependency-light.
    """

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "image": ("IMAGE", {}),
                "strength": ("FLOAT", {"default": 0.15, "min": -1.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {},
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/Examples"
    NODE_NAME = "BrainsXDEV_Brightness"

    def _apply(self, img: np.ndarray, strength: float) -> np.ndarray:
        """Apply brightness adjustment to a single image array."""
        # Ensure float32, preserve shape, clamp to [0,1]
        arr = img.astype(np.float32, copy=False)
        arr = np.clip(arr + strength, 0.0, 1.0)
        return arr

    def run(self, image, strength: float, prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[List[np.ndarray]]:
        """
        Process IMAGE input(s) and return brightness-adjusted version(s).
        Comfy passes IMAGE as a list of arrays; support both single and batch.
        """
        if isinstance(image, list):
            out = [self._apply(img, strength) for img in image]
        else:
            out = [self._apply(image, strength)]
        return (out,)
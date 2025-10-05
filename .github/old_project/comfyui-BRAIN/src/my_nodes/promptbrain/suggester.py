"""
PromptBrain — Prompt Suggester
Combines tags/captions and memory to build positive/negative prompt strings.
"""
from typing import Any, Dict, Tuple, List
import json

class PB_PromptSuggester:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tags_dict": ("DICT", {}),
                "captions": ("LIST", {}),  # from PB_MemoryRead
                "max_terms": ("INT", {"default": 16, "min": 4, "max": 128, "step": 1}),
            },
            "optional": {
                "negatives": ("STRING", {"default": "(watermark:1.2), (text:1.2)"}),
            },
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
    RETURN_TYPES = ("STRING","STRING")
    RETURN_NAMES = ("positive","negative")
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_PromptSuggester"

    def run(self, tags_dict, captions, max_terms: int, negatives: str, unique_id=None):
        # naive merge: take top-N tag keys by score (if present) + top captions
        tags = []
        if isinstance(tags_dict, dict) and "tags" in tags_dict:
            items = list(tags_dict["tags"].items())
            items.sort(key=lambda kv: kv[1], reverse=True)
            tags = [k for k,_ in items[:max_terms]]
        cap = ", ".join(captions[:3]) if isinstance(captions, list) else ""
        positive = ", ".join([*tags, cap]).strip(", ")
        return (positive, negatives)

"""
Brains-XDEV PromptBrain — Prompt Suggester

Combines tags/captions and memory to build positive/negative prompt strings.
Intelligently merges different sources of prompt information.

Migrated from BRAIN project with Brains-XDEV naming conventions.
"""
from typing import Any, Dict, Tuple, List
import json

print("[Brains-XDEV] suggester import")

class BrainsXDEV_PromptSuggester:
    """
    Intelligent prompt suggestion node that combines tags, captions, and memory.
    Builds positive and negative prompt strings for image generation.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "tags_dict": ("DICT", {}),
                "captions": ("LIST", {}),  # from BrainsXDEV_MemoryRead
                "max_terms": ("INT", {"default": 16, "min": 4, "max": 128, "step": 1}),
            },
            "optional": {
                "negatives": ("STRING", {"default": "(watermark:1.2), (text:1.2), low quality, blurry"}),
                "style_prefix": ("STRING", {"default": ""}),
                "quality_prefix": ("STRING", {"default": "masterpiece, best quality, "}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "DICT")
    RETURN_NAMES = ("positive", "negative", "metadata")
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_PromptSuggester"

    def run(self, tags_dict, captions, max_terms: int, negatives: str = "", 
            style_prefix: str = "", quality_prefix: str = "",
            prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[str, str, Dict]:
        """
        Build intelligent prompt suggestions from tags, captions, and memory.
        """
        
        # Extract and rank tags
        tags = []
        tag_count = 0
        if isinstance(tags_dict, dict) and "tags" in tags_dict:
            # Sort tags by score (highest first)
            items = list(tags_dict["tags"].items())
            items.sort(key=lambda kv: kv[1], reverse=True)
            tags = [k for k, score in items[:max_terms] if score > 0.3]  # Filter low-confidence tags
            tag_count = len(tags)
        
        # Process captions (take top 2-3 most relevant)
        caption_text = ""
        caption_count = 0
        if isinstance(captions, list) and captions:
            # Take first few captions, clean and combine
            selected_captions = [cap.strip() for cap in captions[:3] if cap.strip()]
            if selected_captions:
                caption_text = ", ".join(selected_captions)
                caption_count = len(selected_captions)
        
        # Build positive prompt
        positive_parts = []
        
        # Add quality prefix if specified
        if quality_prefix.strip():
            positive_parts.append(quality_prefix.strip())
        
        # Add style prefix if specified
        if style_prefix.strip():
            positive_parts.append(style_prefix.strip())
        
        # Add tags
        if tags:
            positive_parts.append(", ".join(tags))
        
        # Add captions
        if caption_text:
            positive_parts.append(caption_text)
        
        # Combine all parts
        positive = ", ".join(positive_parts).strip(", ")
        
        # Ensure we have something
        if not positive:
            positive = "high quality image"
        
        # Build metadata
        metadata = {
            "tag_count": tag_count,
            "caption_count": caption_count,
            "max_terms": max_terms,
            "has_style": bool(style_prefix.strip()),
            "has_quality": bool(quality_prefix.strip()),
            "uid": unique_id
        }
        
        return (positive, negatives, metadata)
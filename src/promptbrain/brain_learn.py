#!/usr/bin/env python3
"""
Brains-XDEV PromptBrain Learn Direct Node

Learn from prompts with quality scores using BRAIN datatype.
Imported from Comfyui-DEV and adapted for Brains-XDEV architecture.

References:
- ComfyUI Custom Datatypes: https://docs.comfy.org/custom-nodes/backend/custom_datatypes
- PromptBrain Learning: https://github.com/aiforhumans/Brains
"""

print("[Brains-XDEV] brain_learn import")

from typing import Any, Dict, Tuple, List
import re

from .brain_data import BrainData


class BrainsXDEV_PromptBrainLearnDirect:
    """
    Enhanced PromptBrainLearn that works with BRAIN datatype.
    Learns from text prompts with quality scores and style categorization.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "brain_data": ("BRAIN", {"forceInput": True}),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "The prompt to learn from"
                }),
                "score": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "Quality score (0.0=poor, 1.0=excellent)"
                }),
                "style_category": (["none", "photorealistic", "artistic", "anime", "fantasy", 
                                  "portrait", "landscape", "cinematic", "vintage", "modern", 
                                  "abstract", "minimalist"], {
                    "default": "none",
                    "tooltip": "Artistic style category"
                }),
                "feature_emphasis": (["none", "composition", "lighting", "color", "texture", 
                                    "mood", "character", "background", "clothing", "accessories"], {
                    "default": "none",
                    "tooltip": "Visual feature to emphasize"
                })
            },
            "optional": {
                "learning_rate": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "Learning intensity multiplier"
                })
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            }
        }
    
    RETURN_TYPES = ("BRAIN", "STRING")
    RETURN_NAMES = ("brain_data", "status")
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_PromptBrainLearnDirect"
    DESCRIPTION = "Learn from prompt using BRAIN datatype"
    
    def run(
        self, 
        brain_data: BrainData, 
        prompt: str, 
        score: float, 
        style_category: str = "none", 
        feature_emphasis: str = "none", 
        learning_rate: float = 1.0,
        prompt_param=None,
        extra_pnginfo=None,
        unique_id=None
    ) -> Tuple[BrainData, str]:
        """
        Learn from prompt using direct brain data.
        
        Args:
            brain_data: Input BRAIN datatype
            prompt: Text prompt to learn from
            score: Quality score (0.0-1.0)
            style_category: Artistic style category
            feature_emphasis: Visual feature to emphasize
            learning_rate: Learning intensity multiplier
            prompt_param: Hidden input - current workflow prompt
            extra_pnginfo: Hidden input - PNG metadata
            unique_id: Hidden input - node unique identifier
            
        Returns:
            Tuple containing (updated brain_data, status message)
        """
        # Validate inputs
        if not (0.0 <= score <= 1.0):
            return (brain_data, "âŒ Score must be between 0.0 and 1.0")
        
        # Extract tags from prompt
        tags = self.extract_tags(prompt)
        
        if not tags:
            return (brain_data, "âŒ No valid tags found in prompt")
        
        # Apply learning rate
        adjusted_score = score * learning_rate
        
        # Add learning event to brain
        brain_data.add_learning_event(
            prompt=prompt,
            score=adjusted_score,
            tags=tags,
            style_category=style_category,
            feature_emphasis=feature_emphasis
        )
        
        # Track node processing
        brain_data.add_node_to_chain("PromptBrainLearnDirect")
        
        # Generate status message
        status = f"âœ… Learned from {len(tags)} tags with score {score:.1f}"
        if style_category != "none":
            status += f" (Style: {style_category})"
        if feature_emphasis != "none":
            status += f" (Feature: {feature_emphasis})"
        
        return (brain_data, status)
    
    def extract_tags(self, prompt: str) -> List[str]:
        """
        Extract tags from prompt.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            List of extracted tags
        """
        # Clean and normalize
        cleaned = re.sub(r'[^\w\s,:-]', '', prompt.lower())
        
        # Split by commas and clean
        raw_tags = [tag.strip() for tag in cleaned.split(',')]
        
        # Filter valid tags
        valid_tags = []
        for tag in raw_tags:
            if tag and len(tag) > 1:
                valid_tags.append(tag)
        
        return valid_tags

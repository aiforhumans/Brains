"""
Brains-XDEV Custom Nodes for ComfyUI

This package contains nodes following the Brains-XDEV architecture patterns,
including basic examples and advanced PromptBrain AI functionality.
"""

print("[Brains-XDEV] Initializing custom nodes...")

# Import basic example nodes
from .brightness_example import BrainsXDEV_Brightness

# Map node class name to the class itself so ComfyUI can discover it
NODE_CLASS_MAPPINGS = {
    "BrainsXDEV_Brightness": BrainsXDEV_Brightness,
}

# Display names in the UI (following Brains-XDEV convention)
NODE_DISPLAY_NAME_MAPPINGS = {
    "BrainsXDEV_Brightness": "Brains-XDEV • Brightness (example)",
}

# Import PromptBrain nodes (AI/ML functionality)
try:
    from .promptbrain.memory import BrainsXDEV_MemoryWrite, BrainsXDEV_MemoryRead
    
    NODE_CLASS_MAPPINGS.update({
        "BrainsXDEV_MemoryWrite": BrainsXDEV_MemoryWrite,
        "BrainsXDEV_MemoryRead": BrainsXDEV_MemoryRead,
    })
    
    NODE_DISPLAY_NAME_MAPPINGS.update({
        "BrainsXDEV_MemoryWrite": "Brains-XDEV • Memory Write (SQLite)",
        "BrainsXDEV_MemoryRead": "Brains-XDEV • Memory Read (SQLite)",
    })
    
    print("[Brains-XDEV] PromptBrain memory nodes loaded")
    
except ImportError as e:
    print(f"[Brains-XDEV] PromptBrain memory nodes not available: {e}")

# Import AI adapter nodes (optional, requires additional dependencies)
try:
    from .promptbrain.florence2_adapter import BrainsXDEV_Florence2Adapter
    from .promptbrain.wd14_adapter import BrainsXDEV_WD14Adapter
    from .promptbrain.tagger import BrainsXDEV_Tagger
    from .promptbrain.captioner import BrainsXDEV_Captioner
    from .promptbrain.scorer import BrainsXDEV_Scorer
    from .promptbrain.suggester import BrainsXDEV_PromptSuggester
    from .promptbrain.ema_ranker import BrainsXDEV_EMARanker
    
    NODE_CLASS_MAPPINGS.update({
        "BrainsXDEV_Florence2Adapter": BrainsXDEV_Florence2Adapter,
        "BrainsXDEV_WD14Adapter": BrainsXDEV_WD14Adapter,
        "BrainsXDEV_Tagger": BrainsXDEV_Tagger,
        "BrainsXDEV_Captioner": BrainsXDEV_Captioner,
        "BrainsXDEV_Scorer": BrainsXDEV_Scorer,
        "BrainsXDEV_PromptSuggester": BrainsXDEV_PromptSuggester,
        "BrainsXDEV_EMARanker": BrainsXDEV_EMARanker,
    })
    
    NODE_DISPLAY_NAME_MAPPINGS.update({
        "BrainsXDEV_Florence2Adapter": "Brains-XDEV • Florence2 Adapter (Transformers)",
        "BrainsXDEV_WD14Adapter": "Brains-XDEV • WD14 Adapter (ONNX)",
        "BrainsXDEV_Tagger": "Brains-XDEV • Tagger (stub)",
        "BrainsXDEV_Captioner": "Brains-XDEV • Captioner (stub)",
        "BrainsXDEV_Scorer": "Brains-XDEV • Scorer (manual)",
        "BrainsXDEV_PromptSuggester": "Brains-XDEV • Prompt Suggester",
        "BrainsXDEV_EMARanker": "Brains-XDEV • EMA Ranker",
    })
    
    print("[Brains-XDEV] PromptBrain AI nodes loaded")
    
except ImportError as e:
    print(f"[Brains-XDEV] PromptBrain AI nodes not available: {e}")

# Import advanced BRAIN datatype nodes (imported from Comfyui-DEV)
try:
    from .brain_datatype import (
        BrainData,
        NODE_CLASS_MAPPINGS_BRAIN,
        NODE_DISPLAY_NAME_MAPPINGS_BRAIN
    )
    
    NODE_CLASS_MAPPINGS.update(NODE_CLASS_MAPPINGS_BRAIN)
    NODE_DISPLAY_NAME_MAPPINGS.update(NODE_DISPLAY_NAME_MAPPINGS_BRAIN)
    
    print("[Brains-XDEV] Advanced BRAIN datatype nodes loaded")
    
except ImportError as e:
    print(f"[Brains-XDEV] Advanced BRAIN datatype nodes not available: {e}")

# Import separate PromptBrain nodes (imported from Comfyui-DEV)
# Note: BrainData is a data class, not a node - do not register it
try:
    from .promptbrain.brain_learn import BrainsXDEV_PromptBrainLearnDirect as BrainLearn
    from .promptbrain.brain_source import BrainsXDEV_PromptBrainSource as BrainSource
    
    NODE_CLASS_MAPPINGS.update({
        "BrainsXDEV_BrainLearn": BrainLearn,
        "BrainsXDEV_BrainSource": BrainSource,
    })
    
    NODE_DISPLAY_NAME_MAPPINGS.update({
        "BrainsXDEV_BrainLearn": "Brains-XDEV • Brain Learn (direct)",
        "BrainsXDEV_BrainSource": "Brains-XDEV • Brain Source (direct)",
    })
    
    print("[Brains-XDEV] Separate PromptBrain nodes loaded")
    
except ImportError as e:
    print(f"[Brains-XDEV] Separate PromptBrain nodes not available: {e}")

print(f"[Brains-XDEV] Loaded {len(NODE_CLASS_MAPPINGS)} nodes total")

# Export for ComfyUI discovery
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
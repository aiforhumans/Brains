from .basic_example import XDEV_Brightness

# Map node class name to the class itself so ComfyUI can discover it.
NODE_CLASS_MAPPINGS = {
    "XDEV_Brightness": XDEV_Brightness,
}

# Optional: nicer display name in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "XDEV_Brightness": "XDEV • Brightness",
}

from .promptbrain.tagger import PB_WD14Tagger
from .promptbrain.captioner import PB_Captioner
from .promptbrain.scorer import PB_Scorer
from .promptbrain.memory import PB_MemoryWrite, PB_MemoryRead
from .promptbrain.suggester import PB_PromptSuggester

NODE_CLASS_MAPPINGS.update({
    "PB_WD14Tagger": PB_WD14Tagger,
    "PB_Captioner": PB_Captioner,
    "PB_Scorer": PB_Scorer,
    "PB_MemoryWrite": PB_MemoryWrite,
    "PB_MemoryRead": PB_MemoryRead,
    "PB_PromptSuggester": PB_PromptSuggester,
})

NODE_DISPLAY_NAME_MAPPINGS.update({
    "PB_WD14Tagger": "PromptBrain • WD14 Tagger (stub)",
    "PB_Captioner": "PromptBrain • Captioner (stub)",
    "PB_Scorer": "PromptBrain • Scorer (manual)",
    "PB_MemoryWrite": "PromptBrain • Memory Write (SQLite)",
    "PB_MemoryRead": "PromptBrain • Memory Read (SQLite)",
    "PB_PromptSuggester": "PromptBrain • Prompt Suggester",
})

from .promptbrain.wd14_adapter import PB_WD14Adapter
from .promptbrain.florence2_adapter import PB_Florence2Adapter
from .promptbrain.ema_ranker import PB_EMARanker

NODE_CLASS_MAPPINGS.update({
    "PB_WD14Adapter": PB_WD14Adapter,
    "PB_Florence2Adapter": PB_Florence2Adapter,
    "PB_EMARanker": PB_EMARanker,
})

NODE_DISPLAY_NAME_MAPPINGS.update({
    "PB_WD14Adapter": "PromptBrain • WD14 Adapter (ONNX)",
    "PB_Florence2Adapter": "PromptBrain • Florence2 Adapter",
    "PB_EMARanker": "PromptBrain • EMA Ranker",
})

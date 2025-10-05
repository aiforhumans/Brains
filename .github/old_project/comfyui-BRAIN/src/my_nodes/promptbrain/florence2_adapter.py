"""
PromptBrain — Florence-2 Captioner Adapter (Transformers)
Uses microsoft/Florence-2 model via Hugging Face transformers to produce captions.

Requirements:
- torch
- transformers >= 4.40
- pillow (optional, for robust preprocessing)

References:
- https://github.com/kijai/ComfyUI-Florence2 (ComfyUI node)
- https://huggingface.co/microsoft/Florence-2-base
"""
from typing import Any, Dict, Tuple, List
import numpy as np

try:
    import torch
    from transformers import AutoProcessor, AutoModelForCausalLM
except Exception:
    AutoProcessor = None
    AutoModelForCausalLM = None
    torch = None

class PB_Florence2Adapter:
    _processor = None
    _model = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "model_id": ("STRING", {"default": "microsoft/Florence-2-base"}),
                "task_prompt": ("STRING", {"default": "<CAPTION>"}),
                "max_new_tokens": ("INT", {"default": 64, "min": 8, "max": 256, "step": 1}),
            },
            "optional": {},
            "hidden": {"unique_id": "UNIQUE_ID"}
        }

    RETURN_TYPES = ("STRING","DICT")
    RETURN_NAMES = ("caption","metadata")
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_Florence2Adapter"

    def _ensure(self, model_id: str, device: str = None):
        if AutoProcessor is None or AutoModelForCausalLM is None:
            raise RuntimeError("Install torch and transformers to use Florence-2 adapter.")
        if self._processor is None or self._model is None:
            self._processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
            self._model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).eval()
            if torch.cuda.is_available():
                self._model.to("cuda")
        return self._processor, self._model

    def _to_pil(self, arr: np.ndarray):
        try:
            from PIL import Image
            img = (arr * 255.0).clip(0,255).astype("uint8")
            return Image.fromarray(img)
        except Exception:
            # Fallback: transformers can take numpy arrays in some processors
            return (arr * 255.0).clip(0,255).astype("uint8")

    def run(self, image, model_id: str, task_prompt: str, max_new_tokens: int, unique_id=None):
        if isinstance(image, list):
            img = image[0]
        else:
            img = image
        processor, model = self._ensure(model_id)
        pil = self._to_pil(img)
        inputs = processor(text=task_prompt, images=pil, return_tensors="pt")
        if hasattr(model, "device") and str(model.device) == "cuda":
            inputs = {k: v.to(model.device) for k,v in inputs.items()}
        generated_ids = model.generate(**inputs, max_new_tokens=int(max_new_tokens))
        output_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        # Florence-2 sometimes returns structured outputs; leave raw here.
        return (output_text, {"model_id": model_id, "task": task_prompt})

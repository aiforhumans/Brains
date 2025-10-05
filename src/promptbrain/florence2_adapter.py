"""
Brains-XDEV PromptBrain — Florence-2 Captioner Adapter (Transformers)

Uses microsoft/Florence-2 model via Hugging Face transformers to produce captions.
Migrated from BRAIN project with Brains-XDEV naming conventions.

Fixed compatibility issues with newer Transformers versions:
- SDPA (Scaled Dot Product Attention) compatibility by using eager attention
- Fallback model loading for older Transformers versions
- Proper pad_token_id handling for generation

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

print("[Brains-XDEV] florence2_adapter import")

try:
    import torch
    from transformers import AutoProcessor, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    AutoProcessor = None
    AutoModelForCausalLM = None
    torch = None
    TRANSFORMERS_AVAILABLE = False

class BrainsXDEV_Florence2Adapter:
    """
    Florence-2 model adapter for image captioning and vision-language tasks.
    Uses Hugging Face transformers to run Florence-2 models.
    """
    
    # Class-level model cache for efficiency
    _processor = None
    _model = None
    _current_model_id = None

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "image": ("IMAGE", {}),
                "model_id": ("STRING", {"default": "microsoft/Florence-2-base"}),
                "task_prompt": ("STRING", {"default": "<CAPTION>"}),
                "max_new_tokens": ("INT", {"default": 64, "min": 8, "max": 256, "step": 1}),
            },
            "optional": {},
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
    NODE_NAME = "BrainsXDEV_Florence2Adapter"

    def _ensure_model(self, model_id: str):
        """Load or reuse the Florence-2 model and processor."""
        if not TRANSFORMERS_AVAILABLE:
            raise RuntimeError("Install torch and transformers to use Florence-2 adapter: pip install torch transformers")
        
        # Load model if not cached or if model_id changed
        if (self._processor is None or self._model is None or 
            self._current_model_id != model_id):
            
            print(f"[Brains-XDEV] Loading Florence-2 model: {model_id}")
            
            try:
                # Load processor
                self._processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
                
                # Load model with explicit SDPA disable to avoid compatibility issues
                self._model = AutoModelForCausalLM.from_pretrained(
                    model_id, 
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    attn_implementation="eager",  # Use eager attention instead of SDPA
                    low_cpu_mem_usage=True
                ).eval()
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self._model = self._model.to("cuda")
                    print("[Brains-XDEV] Florence-2 model loaded on CUDA")
                else:
                    print("[Brains-XDEV] Florence-2 model loaded on CPU")
                
                self._current_model_id = model_id
                
            except Exception as e:
                print(f"[Brains-XDEV] Error loading Florence-2 model: {e}")
                # Fallback: try without attn_implementation parameter
                try:
                    print("[Brains-XDEV] Trying fallback model loading...")
                    self._processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
                    
                    self._model = AutoModelForCausalLM.from_pretrained(
                        model_id, 
                        trust_remote_code=True,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        low_cpu_mem_usage=True
                    ).eval()
                    
                    # Disable SDPA if the attribute exists (compatibility fix)
                    if hasattr(self._model, 'config') and hasattr(self._model.config, '_attn_implementation'):
                        self._model.config._attn_implementation = "eager"
                    
                    # Move to GPU if available
                    if torch.cuda.is_available():
                        self._model = self._model.to("cuda")
                        print("[Brains-XDEV] Florence-2 model loaded on CUDA (fallback)")
                    else:
                        print("[Brains-XDEV] Florence-2 model loaded on CPU (fallback)")
                    
                    self._current_model_id = model_id
                    
                except Exception as e2:
                    print(f"[Brains-XDEV] Fallback loading also failed: {e2}")
                    raise e2
        
        return self._processor, self._model

    def _to_pil(self, arr):
        """Convert numpy array or torch tensor to PIL Image for transformers processing."""
        try:
            from PIL import Image
            
            # Convert torch tensor to numpy if needed
            if hasattr(arr, 'cpu'):  # Check if it's a torch tensor
                arr = arr.cpu().numpy()
            
            # Ensure it's a numpy array
            if not isinstance(arr, np.ndarray):
                arr = np.array(arr)
            
            # Handle batch dimension: take first image if shape is [B,H,W,C]
            while len(arr.shape) > 3:
                print(f"[Brains-XDEV] Florence2 removing batch dimension: {arr.shape}")
                arr = arr[0]
            
            # Convert from [0,1] float to [0,255] uint8
            img = (arr * 255.0).clip(0, 255).astype(np.uint8)
            return Image.fromarray(img)
        except ImportError:
            # Fallback: some transformers processors can handle numpy arrays
            if hasattr(arr, 'cpu'):  # Convert torch tensor to numpy
                arr = arr.cpu().numpy()
            if not isinstance(arr, np.ndarray):
                arr = np.array(arr)
            return (arr * 255.0).clip(0, 255).astype(np.uint8)

    def run(self, image, model_id: str, task_prompt: str, max_new_tokens: int, 
            prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[str, Dict]:
        """
        Process image with Florence-2 model and return caption.
        """
        try:
            # Debug: Check input type
            print(f"[Brains-XDEV] Florence2 input type: {type(image)}")
            
            # Handle image input (single image or batch)
            if isinstance(image, list):
                img = image[0]  # Use first image from batch
            else:
                img = image
            
            print(f"[Brains-XDEV] Florence2 processing image type: {type(img)}, shape: {img.shape if hasattr(img, 'shape') else 'N/A'}")
            
            # Load model
            processor, model = self._ensure_model(model_id)
            
            # Convert to PIL Image
            pil_image = self._to_pil(img)
            print(f"[Brains-XDEV] Florence2 PIL image created: {type(pil_image)}, size: {pil_image.size if hasattr(pil_image, 'size') else 'N/A'}")
            
            # Prepare inputs
            inputs = processor(text=task_prompt, images=pil_image, return_tensors="pt")
            
            # Move inputs to same device and dtype as model
            if hasattr(model, "device"):
                device = model.device
                model_dtype = next(model.parameters()).dtype
                inputs = {
                    k: v.to(device=device, dtype=model_dtype) if hasattr(v, 'to') and v.dtype.is_floating_point else v.to(device) if hasattr(v, 'to') else v 
                    for k, v in inputs.items()
                }
                print(f"[Brains-XDEV] Florence2 inputs moved to {device} with dtype {model_dtype}")
            
            # Generate caption with compatible parameters
            with torch.no_grad():
                generated_ids = model.generate(
                    **inputs, 
                    max_new_tokens=int(max_new_tokens),
                    do_sample=False,
                    num_beams=1,
                    use_cache=False,  # Disable KV cache to avoid past_key_values issues
                    pad_token_id=processor.tokenizer.pad_token_id if hasattr(processor, 'tokenizer') else None
                )
            
            # Decode output
            output_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # Clean up output (Florence-2 sometimes includes the task prompt)
            if task_prompt in output_text:
                output_text = output_text.replace(task_prompt, "").strip()
            
            print(f"[Brains-XDEV] Florence2 caption generated: {output_text[:100]}...")
            
            # Prepare metadata
            metadata = {
                "model_id": model_id,
                "task": task_prompt,
                "max_tokens": max_new_tokens,
                "device": str(model.device) if hasattr(model, "device") else "unknown",
                "status": "success"
            }
            
            return (output_text, metadata)
            
        except Exception as e:
            import traceback
            error_msg = f"Florence-2 adapter error: {str(e)}"
            print(f"[Brains-XDEV] {error_msg}")
            print(f"[Brains-XDEV] Full traceback:\n{traceback.format_exc()}")
            
            metadata = {
                "model_id": model_id,
                "task": task_prompt,
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            
            return (error_msg, metadata)
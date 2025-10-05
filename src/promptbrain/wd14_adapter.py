"""
Brains-XDEV PromptBrain — WD14 Adapter (ONNX Runtime)

Runs SmilingWolf WD14 tagger ONNX models and returns {tags: {label: score}}.
Provides high-quality image tagging for the PromptBrain system.

Migrated from BRAIN project with Brains-XDEV naming conventions.

Requirements:
- onnxruntime (or onnxruntime-gpu)
- numpy
- Models: e.g. wd-v1-4-swinv2-tagger-v2.onnx and its labels.csv

References:
- SmilingWolf WD14 models: https://huggingface.co/SmilingWolf
"""
from typing import Any, Dict, Tuple, List
import os, csv
import numpy as np

print("[Brains-XDEV] wd14_adapter import")

try:
    import onnxruntime as ort
    ONNX_AVAILABLE = True
except ImportError:
    ort = None
    ONNX_AVAILABLE = False

class BrainsXDEV_WD14Adapter:
    """
    WD14 ONNX model adapter for high-quality image tagging.
    Uses SmilingWolf's WD14 models for anime/general image classification.
    """
    
    # Class-level session cache for efficiency
    _session_cache = {}
    _labels_cache = {}

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "image": ("IMAGE", {}),
                "onnx_model_path": ("STRING", {"default": "models/wd14/wd-v1-4-swinv2-tagger-v2.onnx"}),
                "labels_csv_path": ("STRING", {"default": "models/wd14/selected_tags.csv"}),
                "min_conf": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "max_tags": ("INT", {"default": 50, "min": 1, "max": 200, "step": 1}),
            },
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
    NODE_NAME = "BrainsXDEV_WD14Adapter"

    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        """
        Preprocess image for WD14 model inference.
        Expects float32 [0,1], converts to NCHW 224x224.
        """
        h, w, c = img.shape
        target = 224
        
        # Simple nearest-neighbor resize (can be improved with Pillow)
        y_idx = (np.linspace(0, h-1, target)).astype(np.int32)
        x_idx = (np.linspace(0, w-1, target)).astype(np.int32)
        
        # Create mesh grid and resize
        resized = img[y_idx][:, x_idx]
        
        # Convert to NCHW format (batch, channels, height, width)
        chw = np.transpose(resized, (2, 0, 1))[None, ...].astype(np.float32)
        
        return chw

    def _load_labels(self, path: str) -> List[str]:
        """Load labels from CSV file, with caching."""
        if path in self._labels_cache:
            return self._labels_cache[path]
        
        labels = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    # Skip comments and empty rows
                    if not row or row[0].startswith("#"):
                        continue
                    labels.append(row[0].strip())
            
            self._labels_cache[path] = labels
            print(f"[Brains-XDEV] Loaded {len(labels)} WD14 labels from {path}")
            
        except Exception as e:
            print(f"[Brains-XDEV] Error loading labels from {path}: {e}")
            labels = []
        
        return labels

    def _get_session(self, model_path: str):
        """Get or create ONNX runtime session with caching."""
        if model_path in self._session_cache:
            return self._session_cache[model_path]
        
        try:
            # Prefer CUDA if available, fallback to CPU
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
            sess = ort.InferenceSession(model_path, providers=providers)
            
            self._session_cache[model_path] = sess
            print(f"[Brains-XDEV] Loaded WD14 ONNX model: {os.path.basename(model_path)}")
            
            return sess
            
        except Exception as e:
            print(f"[Brains-XDEV] Error loading ONNX model {model_path}: {e}")
            raise

    def run(self, image, onnx_model_path: str, labels_csv_path: str, min_conf: float, 
            max_tags: int = 50, prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[str, Dict]:
        """
        Run WD14 inference on the input image.
        """
        try:
            if not ONNX_AVAILABLE:
                error_msg = "onnxruntime not installed. Install with: pip install onnxruntime"
                return ("", {"error": error_msg, "tags": {}})
            
            # Handle image input
            if isinstance(image, list):
                img = image[0]  # Use first image from batch
            else:
                img = image
            
            # Check if model files exist
            if not os.path.exists(onnx_model_path):
                error_msg = f"ONNX model not found: {onnx_model_path}"
                return ("", {"error": error_msg, "tags": {}})
            
            if not os.path.exists(labels_csv_path):
                error_msg = f"Labels file not found: {labels_csv_path}"
                return ("", {"error": error_msg, "tags": {}})
            
            # Preprocess image
            inp = self._preprocess(img)
            
            # Get ONNX session and run inference
            sess = self._get_session(onnx_model_path)
            input_name = sess.get_inputs()[0].name
            
            # Run inference
            scores = sess.run(None, {input_name: inp})[0].reshape(-1)
            
            # Load labels
            labels = self._load_labels(labels_csv_path)
            
            if not labels:
                return ("", {"error": "no_labels_loaded", "tags": {}})
            
            # Build tags dictionary
            tags = {}
            for i, score in enumerate(scores[:len(labels)]):
                if score >= float(min_conf):
                    tags[labels[i]] = float(score)
            
            # Sort tags by score and limit count
            sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:max_tags]
            
            # Create output
            tags_text = ", ".join([tag for tag, _ in sorted_tags])
            
            tags_dict = {
                "tags": dict(sorted_tags),
                "min_conf": float(min_conf),
                "max_tags": max_tags,
                "model": os.path.basename(onnx_model_path),
                "total_tags": len(tags),
                "uid": unique_id
            }
            
            return (tags_text, tags_dict)
            
        except Exception as e:
            error_msg = f"WD14 adapter error: {str(e)}"
            print(f"[Brains-XDEV] {error_msg}")
            return ("", {"error": error_msg, "tags": {}})
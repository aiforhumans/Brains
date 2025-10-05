"""
PromptBrain — WD14 Adapter (ONNX Runtime)
Runs SmilingWolf WD14 tagger ONNX and returns {tags: {label: score}}.

Requirements:
- onnxruntime (or onnxruntime-gpu)
- numpy
- Models: e.g. wd-v1-4-swinv2-tagger-v2.onnx and its labels.csv

References:
- SmilingWolf WD14 models: https://huggingface.co/SmilingWolf
"""
from typing import Any, Dict, Tuple
import os, csv
import numpy as np

try:
    import onnxruntime as ort
except Exception as e:
    ort = None

class PB_WD14Adapter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "onnx_model_path": ("STRING", {"default": "models/wd14/wd-v1-4-swinv2-tagger-v2.onnx"}),
                "labels_csv_path": ("STRING", {"default": "models/wd14/selected_tags.csv"}),
                "min_conf": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {},
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
    RETURN_TYPES = ("STRING","DICT")
    RETURN_NAMES = ("tags_text","tags_dict")
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_WD14Adapter"

    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        # Expect float32 [0,1], convert to NCHW 224x224 with simple resize (nearest) to avoid extra deps
        # If you have Pillow, replace with proper bilinear resize.
        h, w, c = img.shape
        target = 224
        y_idx = (np.linspace(0, h-1, target)).astype(np.int32)
        x_idx = (np.linspace(0, w-1, target)).astype(np.int32)
        grid = img[y_idx][:, x_idx]
        chw = np.transpose(grid, (2,0,1))[None, ...].astype(np.float32)
        return chw

    def _load_labels(self, path: str):
        labels = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].startswith("#"):
                    continue
                if row:
                    labels.append(row[0])
        return labels

    def run(self, image, onnx_model_path: str, labels_csv_path: str, min_conf: float, unique_id=None):
        if ort is None:
            return ("", {"error": "onnxruntime not installed", "tags": {}})
        if isinstance(image, list):
            img = image[0]
        else:
            img = image
        inp = self._preprocess(img)

        sess = ort.InferenceSession(onnx_model_path, providers=["CUDAExecutionProvider","CPUExecutionProvider"])
        input_name = sess.get_inputs()[0].name
        scores = sess.run(None, {input_name: inp})[0].reshape(-1)  # 1 x N
        labels = self._load_labels(labels_csv_path)
        tags = {}
        for i, s in enumerate(scores[:len(labels)]):
            if s >= float(min_conf):
                tags[labels[i]] = float(s)
        text = ", ".join(sorted(tags.keys(), key=lambda k: -tags[k]))
        return (text, {"tags": tags, "min_conf": float(min_conf), "model": os.path.basename(onnx_model_path)})

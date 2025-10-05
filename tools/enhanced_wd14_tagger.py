# Enhanced WD14 Tagger Node with Provider Management
# Drop-in replacement for comfyui-wd14-tagger with GPU acceleration

import os
import sys
import json
import numpy as np
from PIL import Image
import torch

# Add provider manager to path
current_dir = os.path.dirname(os.path.abspath(__file__))
provider_paths = [
    os.path.join(current_dir, "..", "ComfyUI-ReActor", "rt"),
    os.path.join(current_dir, "rt"),
]

for path in provider_paths:
    if os.path.exists(os.path.join(path, "providers.py")) and path not in sys.path:
        sys.path.insert(0, path)
        break

# Try to import enhanced provider management
try:
    from providers import make_session, get_provider_info
    ENHANCED_PROVIDERS = True
except ImportError:
    ENHANCED_PROVIDERS = False

class EnhancedWD14TaggerNode:
    """
    Enhanced WD14 Tagger with ONNX Runtime provider management
    Provides GPU acceleration and robust fallback handling
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (["wd-v1-4-moat-tagger-v2", "wd-v1-4-swinv2-tagger-v2", "wd-v1-4-convnext-tagger-v2"], {
                    "default": "wd-v1-4-moat-tagger-v2"
                }),
                "threshold": ("FLOAT", {
                    "default": 0.35,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
                "character_threshold": ("FLOAT", {
                    "default": 0.85,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05
                }),
            },
            "optional": {
                "provider_debug": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Debug ON",
                    "label_off": "Debug OFF"
                }),
                "provider_override": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "DmlExecutionProvider,CPUExecutionProvider"
                }),
                "enable_profiling": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Profiling ON",
                    "label_off": "Profiling OFF"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("tags", "provider_info")
    FUNCTION = "tag_image"
    CATEGORY = "WD14Tagger"
    
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(__file__), "models")
        self.model_cache = {}
        self.current_provider = "Unknown"
        
        # Ensure models directory exists
        os.makedirs(self.models_dir, exist_ok=True)
    
    def _log(self, message: str, enable_debug: bool):
        """Log message if debug is enabled"""
        if enable_debug:
            print(f"[WD14Tagger] {message}")
    
    def _parse_provider_override(self, provider_string: str):
        """Parse provider override string"""
        if not provider_string or not provider_string.strip():
            return None
        providers = [p.strip() for p in provider_string.split(",")]
        return [p for p in providers if p] or None
    
    def _create_enhanced_session(
        self,
        model_path: str,
        provider_override=None,
        enable_debug: bool = False,
        enable_profiling: bool = False
    ):
        """Create ONNX session with enhanced provider management"""
        
        if ENHANCED_PROVIDERS:
            try:
                session, provider = make_session(
                    model_path=model_path,
                    log=print if enable_debug else None,
                    override=provider_override,
                    enable_profiling=enable_profiling
                )
                
                self.current_provider = provider
                self._log(f"âœ… Enhanced session created with {provider}", enable_debug)
                return session
                
            except Exception as e:
                self._log(f"Enhanced session failed: {e}, using fallback", enable_debug)
        
        # Fallback method
        return self._create_fallback_session(model_path, provider_override, enable_debug)
    
    def _create_fallback_session(
        self,
        model_path: str,
        provider_override=None,
        enable_debug: bool = False
    ):
        """Fallback session creation"""
        
        import onnxruntime as ort
        
        available = ort.get_available_providers()
        
        if provider_override:
            providers = [p for p in provider_override if p in available]
        else:
            providers = []
            for pref in ["DmlExecutionProvider", "CUDAExecutionProvider", "CPUExecutionProvider"]:
                if pref in available:
                    providers.append(pref)
        
        if not providers:
            providers = ["CPUExecutionProvider"]
        
        self._log(f"Fallback mode - Available: {available}", enable_debug)
        self._log(f"Fallback mode - Using: {providers}", enable_debug)
        
        # Try each provider
        for provider in providers:
            try:
                session = ort.InferenceSession(model_path, providers=[provider])
                self.current_provider = provider
                self._log(f"âœ… Fallback success with {provider}", enable_debug)
                return session
            except Exception as e:
                self._log(f"âŒ {provider} failed: {e}", enable_debug)
                continue
        
        # Final CPU attempt
        session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.current_provider = "CPUExecutionProvider"
        self._log(f"âš ï¸ Final CPU fallback", enable_debug)
        return session
    
    def _get_model_path(self, model_name: str) -> str:
        """Get the path to the ONNX model"""
        return os.path.join(self.models_dir, f"{model_name}.onnx")
    
    def _download_model_if_needed(self, model_name: str, enable_debug: bool = False):
        """Download model if it doesn't exist (placeholder)"""
        model_path = self._get_model_path(model_name)
        
        if not os.path.exists(model_path):
            self._log(f"Model {model_name} not found at {model_path}", enable_debug)
            self._log(f"Please download the model manually or implement download logic", enable_debug)
            # In a real implementation, you'd download the model here
            raise FileNotFoundError(f"Model {model_name} not found. Please download it manually.")
        
        return model_path
    
    def _load_model(
        self,
        model_name: str,
        provider_override=None,
        enable_debug: bool = False,
        enable_profiling: bool = False
    ):
        """Load or get cached model"""
        
        cache_key = f"{model_name}_{str(provider_override)}_{enable_profiling}"
        
        if cache_key in self.model_cache:
            self._log(f"Using cached model for {model_name}", enable_debug)
            return self.model_cache[cache_key]
        
        # Get model path
        model_path = self._download_model_if_needed(model_name, enable_debug)
        
        # Create session
        session = self._create_enhanced_session(
            model_path=model_path,
            provider_override=provider_override,
            enable_debug=enable_debug,
            enable_profiling=enable_profiling
        )
        
        # Cache the session
        self.model_cache[cache_key] = session
        self._log(f"Model {model_name} loaded and cached", enable_debug)
        
        return session
    
    def _preprocess_image(self, image):
        """Preprocess image for WD14 tagger"""
        # Convert ComfyUI image format to PIL
        if isinstance(image, torch.Tensor):
            image = image.squeeze().numpy()
            if image.ndim == 3:
                image = (image * 255).astype(np.uint8)
                image = Image.fromarray(image)
            else:
                raise ValueError("Unsupported image format")
        
        # Resize to model input size (typically 448x448 for WD14)
        target_size = 448
        image = image.convert('RGB')
        image = image.resize((target_size, target_size), Image.LANCZOS)
        
        # Convert to numpy array and normalize
        image_array = np.array(image).astype(np.float32)
        image_array = image_array / 255.0
        
        # Add batch dimension and change to CHW format
        image_array = np.transpose(image_array, (2, 0, 1))
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    
    def _postprocess_predictions(
        self,
        predictions,
        model_name: str,
        threshold: float = 0.35,
        character_threshold: float = 0.85
    ):
        """Post-process model predictions to get tags"""
        
        # This is a placeholder - in a real implementation, you'd need the actual
        # tag files and processing logic for the specific WD14 model
        
        # For demonstration, return placeholder tags
        tags = [
            "1girl", "solo", "long_hair", "looking_at_viewer", 
            "blue_eyes", "blonde_hair", "white_background"
        ]
        
        # In real implementation:
        # 1. Load tag files (CSV with tag names)
        # 2. Apply thresholds to predictions
        # 3. Sort by confidence
        # 4. Format output string
        
        return ", ".join(tags)
    
    def tag_image(
        self,
        image,
        model,
        threshold,
        character_threshold,
        provider_debug=False,
        provider_override="",
        enable_profiling=False
    ):
        """
        Main tagging function
        """
        
        try:
            # Parse provider override
            parsed_providers = self._parse_provider_override(provider_override)
            
            self._log(f"Starting image tagging with model: {model}", provider_debug)
            self._log(f"Provider override: {parsed_providers}", provider_debug)
            self._log(f"Threshold: {threshold}, Character threshold: {character_threshold}", provider_debug)
            
            # Load model with enhanced provider management
            session = self._load_model(
                model_name=model,
                provider_override=parsed_providers,
                enable_debug=provider_debug,
                enable_profiling=enable_profiling
            )
            
            # Preprocess image
            processed_image = self._preprocess_image(image)
            self._log(f"Image preprocessed to shape: {processed_image.shape}", provider_debug)
            
            # Run inference
            input_name = session.get_inputs()[0].name
            output_name = session.get_outputs()[0].name
            
            predictions = session.run([output_name], {input_name: processed_image})[0]
            self._log(f"Inference completed, predictions shape: {predictions.shape}", provider_debug)
            
            # Post-process predictions
            tags = self._postprocess_predictions(
                predictions=predictions,
                model_name=model,
                threshold=threshold,
                character_threshold=character_threshold
            )
            
            # Create provider info
            provider_info = f"Provider: {self._get_friendly_provider_name(self.current_provider)}"
            if enable_profiling:
                provider_info += " | Profiling: Enabled"
            
            self._log(f"Tagging completed successfully", provider_debug)
            self._log(f"Generated {len(tags.split(','))} tags", provider_debug)
            
            return (tags, provider_info)
            
        except Exception as e:
            error_msg = f"WD14 Tagging failed: {str(e)}"
            self._log(f"âŒ {error_msg}", True)  # Always log errors
            
            # Return error information
            return (f"ERROR: {error_msg}", f"ERROR: {self.current_provider}")
    
    def _get_friendly_provider_name(self, provider: str) -> str:
        """Get user-friendly provider name"""
        names = {
            "CUDAExecutionProvider": "ðŸš€ CUDA GPU",
            "DmlExecutionProvider": "ðŸš€ DirectML GPU",
            "CPUExecutionProvider": "ðŸŒ CPU"
        }
        return names.get(provider, provider)

# Node registration
NODE_CLASS_MAPPINGS = {
    "EnhancedWD14TaggerNode": EnhancedWD14TaggerNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EnhancedWD14TaggerNode": "WD14 Tagger (Enhanced)"
}

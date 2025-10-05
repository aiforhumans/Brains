# 🛠️ Development Guide

Complete guide for developers working on comfyui-Brains.

## 🏗️ Development Setup

### Prerequisites
- **ComfyUI**: v0.3.62 or higher
- **Python**: 3.10+ (embedded Python recommended)
- **CUDA**: 11.8+ for GPU acceleration (optional but recommended)
- **VS Code**: Recommended IDE with Python extension

### Installation for Development

1. **Clone the repository:**
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/aiforhumans/Brains.git
cd Brains
```

2. **Install dependencies:**
```bash
# Using ComfyUI's embedded Python (recommended)
C:/comfy/ComfyUI_windows_portable/python_embeded/python.exe -m pip install -r requirements.txt

# Or use your system Python
pip install -r requirements.txt
```

3. **Install dev dependencies:**
```bash
pip install pytest pytest-cov websockets
```

### Symlink Development Setup (Advanced)

For hot-reload development workflow:

**Windows (PowerShell as Administrator):**
```powershell
# Create junction (Windows symlink alternative)
New-Item -ItemType Junction -Path "C:/comfy/ComfyUI_windows_portable/ComfyUI/custom_nodes/comfyui-Brains" -Target "C:/development_node/Brains-XDEV/src"
```

**Linux/Mac:**
```bash
ln -s /path/to/your/dev/folder/src /path/to/ComfyUI/custom_nodes/comfyui-Brains
```

**Benefits:**
- Edit code in your dev folder
- Changes immediately available in ComfyUI (after restart)
- Keep clean separation between dev and deployment

### VS Code Workspace

Open `Brains-XDEV.code-workspace` to get:
- Dual workspace (dev folder + ComfyUI symlink)
- Pre-configured tasks (Run ComfyUI, Install requirements)
- Debug configurations
- Python path settings

## 📝 Node Development

### Node Structure Template

```python
"""
NodeName — Brief description of what this node does.

Docs references and dependencies go here.
"""
from typing import Any, Dict, Tuple, List
import numpy as np

class NodeName:
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "param": ("TYPE", {"default": "value", "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "optional_param": ("STRING", {"default": ""}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO", 
                "unique_id": "UNIQUE_ID",
            }
        }
    
    RETURN_TYPES = ("TYPE",)
    RETURN_NAMES = ("output_name",)
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/SubCategory"
    NODE_NAME = "NodeName"
    
    def run(self, param, optional_param="", prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[List]:
        """
        Main execution function.
        
        Args:
            param: Required parameter description
            optional_param: Optional parameter description
            prompt: Full workflow context (hidden)
            extra_pnginfo: Metadata from workflow (hidden)
            unique_id: Node instance ID (hidden)
            
        Returns:
            Tuple containing results
        """
        try:
            # Implementation here
            result = self._process(param)
            return (result,)
        except Exception as e:
            print(f"[Brains-XDEV] Error in {self.NODE_NAME}: {e}")
            return (None,)
    
    def _process(self, param):
        """Private helper method."""
        # Implementation
        pass
```

### Node Registration

In `src/__init__.py`:

```python
from .module_name import NodeClass

# Single node
NODE_CLASS_MAPPINGS = {"NodeClass": NodeClass}
NODE_DISPLAY_NAME_MAPPINGS = {"NodeClass": "Brains-XDEV • Node Name"}

# Multiple nodes
NODE_CLASS_MAPPINGS.update({
    "Node2": Node2,
    "Node3": Node3,
})
NODE_DISPLAY_NAME_MAPPINGS.update({
    "Node2": "Brains-XDEV • Node2",
    "Node3": "Brains-XDEV • Node3 (function)",
})
```

### Category Organization

- **Brains-XDEV/Examples** - Example/test nodes
- **Brains-XDEV/AI** - AI/ML nodes
- **Brains-XDEV/Utils** - Utility nodes
- **Brains-XDEV/PromptBrain** - BRAIN learning system nodes
- **XDev/** - Development/testing prefix

### Display Name Convention

- Format: `"Brains-XDEV • NodeName (function)"`
- For adapters: `"Brains-XDEV • ModelName Adapter (runtime)"`
- For stubs: `"Brains-XDEV • NodeName (stub)"`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_brain_datatype.py

# Run with verbose output
pytest -v tests/

# Run with coverage
pytest --cov=src tests/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/
```

### Test Structure

```python
import pytest
from src.node_name import NodeClass

def test_registration():
    """Test node registration and structure."""
    node = NodeClass()
    assert hasattr(node, 'run')
    assert isinstance(node.RETURN_TYPES, tuple)
    assert hasattr(node, 'INPUT_TYPES')

def test_functionality():
    """Test node functionality."""
    node = NodeClass()
    result = node.run(test_input)
    assert result is not None
    assert result[0].shape == expected_shape

def test_error_handling():
    """Test error handling."""
    node = NodeClass()
    result = node.run(invalid_input)
    assert result[0] is None  # Should handle gracefully
```

### Workflow Testing

Use `tools/run_ws_client.py` for API testing:

```bash
# Test workflow via WebSocket API
python tools/run_ws_client.py workflows/basic/test.prompt.json
```

**Workflow formats:**
- `.workflow.json` - UI format (for loading in ComfyUI UI)
- `.prompt.json` - API format (for programmatic execution)

## 🏛️ Architecture

### BRAIN Datatype System

**Core Components:**
1. **BrainData class** (`brain_data.py`) - Custom datatype implementation
2. **SQLite storage** - Persistent learning data
3. **Quality tracking** - Multi-dimensional scoring
4. **Style categories** - Artistic style classification

**Data Flow:**
```
Input → BRAIN Source → Learn → Suggest → KSampler → Quality Score → Learn (feedback loop)
```

### Image Processing Pattern

```python
def process_images(self, images):
    """
    Process ComfyUI IMAGE type.
    
    Args:
        images: Tensor or list of HxWxC float32 arrays in [0,1]
        
    Returns:
        Processed results
    """
    # Handle batch
    if isinstance(images, list):
        return [self._process_single(img) for img in images]
    else:
        return self._process_single(images)

def _process_single(self, image):
    """Process single image."""
    # image is HxWxC float32 in range [0, 1]
    # Convert to uint8 if needed
    if image.dtype == np.float32:
        image = (image * 255).astype(np.uint8)
    return result
```

### Error Handling Pattern

```python
try:
    import optional_dependency
    OPTIONAL_AVAILABLE = True
except ImportError:
    OPTIONAL_AVAILABLE = False
    optional_dependency = None

# In run method:
if not OPTIONAL_AVAILABLE:
    return ("Error: optional_dependency not installed. Install with: pip install optional_dependency",)
```

## 🎨 Workflow Development

### Workflow Structure

```json
{
  "last_node_id": 25,
  "last_link_id": 44,
  "nodes": [
    {
      "id": 1,
      "type": "NodeType",
      "pos": [x, y],
      "size": [width, height],
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [...],
      "outputs": [...],
      "properties": {},
      "widgets_values": [...]
    }
  ],
  "links": [
    [link_id, source_node, source_output, target_node, target_input, "TYPE"]
  ],
  "groups": [],
  "config": {},
  "extra": {},
  "version": 0.4
}
```

### Link Format (Critical)

**Valid link:**
```json
[1, 2, 0, 3, 1, "IMAGE"]
```
- `[link_id, source_node_id, source_output_index, target_node_id, target_input_index, type]`

**Invalid (Zod schema error):**
```json
[1, 2, 0, null, null, null]  // ❌ Don't use null values
```

**Solution:** Only include links for used outputs. Remove entries for unused outputs entirely.

### Validation

All workflows must pass Zod schema validation:
- No null values in link arrays (positions 3, 4, 5)
- All node IDs must exist
- All referenced types must be valid
- Link IDs must be unique

## 🔧 Tools & Utilities

### Memory Management

```python
from src.cleanup_memory import cleanup_memory

# Clean up memory
cleanup_memory(aggressive=True)
```

### Status Checking

```python
from src.comfyui_status_check import check_status

# Check ComfyUI health
status = check_status()
```

### BRAIN Analysis

```python
from src.analyze_brain import analyze_brain_data

# Analyze BRAIN database
analysis = analyze_brain_data("path/to/promptbrain.db")
print(analysis["summary"])
```

## 📦 Dependencies

### Core (required)
- `numpy` - Array operations
- `torch` - AI/ML operations (if using AI nodes)
- `pillow` - Image processing

### Optional
- `psutil` - Memory management (for cleanup utilities)
- `onnxruntime` or `onnxruntime-gpu` - ONNX model inference
- `transformers` - HuggingFace models

### Dev
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `websockets` - API testing

## 🐛 Debugging

### Console Messages

Check ComfyUI console for import messages:
```
[Brains-XDEV] brain_datatype import
[Brains-XDEV] florence2_adapter import
[Brains-XDEV] Loaded 20+ nodes successfully
```

### Common Issues

**Import errors:**
- Check embedded Python dependencies
- Verify paths in pyproject.toml
- Clear `__pycache__` folders

**Missing models:**
- Verify model paths in node parameters
- Download required models to `models/` directory
- Check model format (ONNX, SafeTensors, etc.)

**Type errors:**
- Ensure RETURN_TYPES match actual returns
- Verify INPUT_TYPES format
- Check for proper type hints

**Symlink issues:**
- Use junction on Windows if symlinks fail
- Verify permissions
- Check paths in workspace file

### Debug Workflow

Use `workflows/debug_all_nodes.json` to test all nodes at once.

## 📚 Additional Resources

- **[README.md](../README.md)** - Project overview
- **[TESTING.md](../TESTING.md)** - Testing guidelines
- **[Workflow Index](../workflows/INDEX.md)** - Workflow documentation
- **[Copilot Instructions](../.github/copilot-instructions.md)** - AI pair programming patterns

## 🤝 Contributing

### Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Follow existing code patterns (see Node Structure Template)
4. Add tests for new features
5. Update documentation
6. Commit changes (`git commit -m 'Add AmazingFeature'`)
7. Push to branch (`git push origin feature/AmazingFeature`)
8. Open Pull Request

### Code Style

- Follow existing patterns
- Use type hints
- Add docstrings for public methods
- Include error handling
- Write descriptive commit messages

### Testing Requirements

- All new nodes must have tests
- Tests must pass before PR
- Aim for >80% code coverage
- Include integration tests for complex workflows

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/aiforhumans/Brains/issues)
- **Discussions**: [GitHub Discussions](https://github.com/aiforhumans/Brains/discussions)

---

**Happy Development! 🧠**

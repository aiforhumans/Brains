# Copilot Instructions for Brains-XDEV

This is a ComfyUI custom node development project using a symlinked architecture for hot-reloading development, evolved from the BRAIN project patterns with enhanced tools imported from Comfyui-DEV.

## Architecture Overview

- **Source code**: `src/` directory contains all node implementations
- **Symlink deployment**: `src/` is symlinked to `C:/comfy/ComfyUI_windows_portable/ComfyUI/custom_nodes/comfyui-Brains-XDEV`
- **Dual workspace**: VS Code workspace includes both development folder and symlink target for seamless editing
- **Embedded Python**: Uses ComfyUI's embedded Python interpreter at `C:/comfy/ComfyUI_windows_portable/python_embeded/python.exe`
- **Enhanced capabilities**: Advanced BRAIN datatype ecosystem with 30+ nodes including AI parameter optimization

## Imported Tool Ecosystem (from Comfyui-DEV)

### Core BRAIN Datatype (brain_datatype.py - 2,164 lines)
- **BrainData class**: Complete custom datatype for seamless node communication
- **8 Advanced PromptBrain nodes** with BRAIN datatype integration:
  - `BrainsXDEV_PromptBrainSource` - BRAIN data source/loader with auto-discovery
  - `BrainsXDEV_PromptBrainLearnDirect` - Learning from prompts with style categories
  - `BrainsXDEV_PromptBrainSuggestDirect` - Enhanced prompt generation with creativity control
  - `BrainsXDEV_PromptBrainPerformanceDirect` - Comprehensive performance analysis
  - `BrainsXDEV_PromptBrainResetDirect` - Data reset with backup and selective options
  - `BrainsXDEV_PromptBrainQualityScore` - AI-powered quality scoring (technical/artistic/semantic)
  - `BrainsXDEV_PromptBrainKSamplerDirect` - Intelligent KSampler with quality-based optimization
  - `BrainsXDEV_PromptBrainParameterOptimizer` - AI parameter optimization for generation settings

### Separate PromptBrain Nodes
- **brain_data.py** (266 lines): Core BrainData class implementation
- **brain_learn.py** (165 lines): Direct learning node for prompt training
- **brain_source.py** (332 lines): BRAIN data source/loader node

### Analysis and Utility Tools
- **analyze_brain.py** (443 lines): PromptBrain data analysis with comprehensive reporting
- **enhanced_wd14_tagger.py**: Improved WD14 functionality with GPU acceleration support
- **cleanup_memory.py**: Memory management utilities (requires psutil)
- **comfyui_status_check.py**: ComfyUI status checking and validation tools
- **install_dependencies.py**: Automated dependency installation utilities

## ComfyUI Node Structure (BRAIN Project Pattern)

All custom nodes must follow ComfyUI's node contract with proper type hints and documentation:

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
        # Implementation with proper error handling
        return (result,)
```

## Project-Specific Patterns from BRAIN

### Node Registration Pattern
- Use centralized registration in `src/__init__.py`:
```python
from .module_name import NodeClass

NODE_CLASS_MAPPINGS = {"NodeClass": NodeClass}
NODE_DISPLAY_NAME_MAPPINGS = {"NodeClass": "Brains-XDEV • Node Name"}

# Update pattern for multiple nodes
NODE_CLASS_MAPPINGS.update({"Node2": Node2})
NODE_DISPLAY_NAME_MAPPINGS.update({"Node2": "Brains-XDEV • Node2"})
```

### Category Organization
- Main categories: `Brains-XDEV/Examples`, `Brains-XDEV/AI`, `Brains-XDEV/Utils`
- Specialized: `Brains-XDEV/PromptBrain` for AI/ML nodes including advanced BRAIN datatype nodes
- Use `XDev/` prefix for development/testing nodes

### Display Name Convention
- Format: `"Brains-XDEV • NodeName (function)"` or `"Brains-XDEV • NodeName"`
- For adapters: `"Brains-XDEV • ModelName Adapter (runtime)"`
- For stubs: `"Brains-XDEV • NodeName (stub)"`

### Hidden Input Usage
- Always include `unique_id` for tracking and debugging
- Use `prompt` for accessing full workflow context
- Use `extra_pnginfo` for metadata processing
- Accept these as optional parameters with defaults

### Error Handling Pattern
```python
try:
    import optional_dependency
except ImportError:
    optional_dependency = None

# In run method:
if optional_dependency is None:
    return ("Error: optional_dependency not installed",)
```

## Development Workflow

### Dependencies (pyproject.toml pattern)
- Use `pyproject.toml` for project configuration
- Separate `[project.optional-dependencies]` for dev tools
- Core dependencies: `numpy` (always), `torch`, `pillow` (for AI nodes)
- Utility dependencies: `psutil` (for memory cleanup tools)
- Dev dependencies: `pytest`, `websockets` (for API testing)

### Testing Pattern
- Tests in `src/tests/` with `pytest`
- Test both registration and functionality:
```python
def test_registration_shapes():
    node = NodeClass()
    assert hasattr(node, 'run')
    assert isinstance(node.RETURN_TYPES, tuple)

def test_functionality():
    node = NodeClass()
    result = node.run(test_input)
    assert result[0].shape == expected_shape
```

### API Workflow Testing
- Use `tools/run_ws_client.py` pattern for WebSocket API testing
- Save workflows as both `.workflow.json` (UI) and `.prompt.json` (API)
- Test programmatic execution with `python tools/run_ws_client.py workflows/demo.prompt.json`

## AI/ML Integration Patterns

### Adapter Pattern (from PromptBrain)
- Separate "stub" nodes (design) from "adapter" nodes (implementation)
- Stub nodes return mock data for workflow design
- Adapter nodes integrate real models (ONNX, Transformers, etc.)
- Use model path parameters for flexibility: `"models/model_name/model.onnx"`

### Model Management
- Store models in `models/` subdirectories by type
- Include labels/config files alongside model files
- Use lazy loading and error handling for missing models
- Support both local and HuggingFace model paths

### Data Flow Pattern
- Input: `IMAGE` tensor (list of HxWxC float32 arrays in [0,1])
- Preprocessing: Handle both single images and batches
- Output: Structured data (`DICT`) + human-readable (`STRING`)
- Memory: SQLite for persistent storage (`promptbrain.db`)

### BRAIN Datatype Integration
- **BrainData class**: Custom datatype for seamless node-to-node communication
- **BRAIN type**: ComfyUI type for passing BrainData instances between nodes
- **Memory storage**: SQLite database with JSON serialization for complex data
- **Quality tracking**: Built-in scoring and performance analysis capabilities
- **Style categories**: Support for artistic style classification and learning

## File Organization

- **Node implementations**: `src/` (symlinked to ComfyUI)
- **Modules**: `src/module_name/` for related nodes
- **Tests**: `src/tests/` with pytest configuration
- **Tools**: `tools/` for development utilities
- **Workflows**: `workflows/` for both UI and API formats
- **Models**: `models/` for AI model files (not in git)

## Running & Testing

### VS Code Tasks
- `Install Brains-XDEV requirements (embedded)` - Install from pyproject.toml
- `Run ComfyUI (Portable)` - Start with custom nodes loaded

### Verification Steps
1. Check console for import messages: `[Brains-XDEV] node_name import`
2. Verify nodes appear in ComfyUI under `Brains-XDEV/` categories
3. Test with both UI workflows and API prompts
4. Run tests: `python -m pytest src/tests/`

## Troubleshooting

### Common Issues
- **Import errors**: Check embedded Python dependencies
- **Missing models**: Verify model paths and downloads
- **Type errors**: Ensure RETURN_TYPES match actual returns
- **Symlink issues**: Use junction if symlinks fail on Windows

### Development Tips
- Clear `__pycache__` after major refactors
- Use descriptive `NODE_NAME` for debugging
- Include docstrings with dependency and reference info
- Test both single and batch inputs for IMAGE processing
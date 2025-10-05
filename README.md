# 🧠 Brains-XDEV — ComfyUI Advanced AI Nodes

**Advanced AI-powered custom nodes for ComfyUI featuring the BRAIN learning system, Florence2 vision analysis, quality scoring, and 16+ professional workflows.**

[![ComfyUI](https://img.shields.io/badge/ComfyUI-v0.3.62-blue)](https://github.com/comfyanonymous/ComfyUI)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## ✨ Features

### 🧠 BRAIN Learning System
- **BrainData** - Custom datatype for seamless AI learning workflows
- **Persistent Learning** - SQLite-backed memory with quality tracking
- **Style Analysis** - Learn from prompts, images, and quality feedback
- **Smart Suggestions** - AI-generated prompts based on learned patterns
- **Performance Analytics** - Track quality trends and optimization

### 🤖 AI Analysis Nodes
- **Florence2 Adapter** - Microsoft's vision model for detailed image captioning
- **Quality Scoring** - Technical, artistic, and semantic quality metrics
- **Parameter Optimizer** - AI-driven generation settings optimization
- **Enhanced WD14 Tagger** - GPU-accelerated anime/general tagging

### 📦 20+ Production Nodes
Complete toolkit for advanced ComfyUI workflows including learning, analysis, optimization, and memory management.

### 🎨 16 Professional Workflows
- **Basic Templates** (5) - Quick start workflows
- **Advanced Automation** (3) - Quality pipelines, style transfer, parameter optimization
- **Experimental** (4) - Ouroboros Engine, Schizophrenic Tribunal, Corrupted Oracle, Temporal Paradox
- **Professional Creative** (4) - Portrait studio, fashion photography, character design, figure studies

## 🚀 Quick Start

### 1. Installation

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/aiforhumans/Brains.git
cd Brains
pip install -r requirements.txt
```

### 2. Verify Installation

Restart ComfyUI and look for:
```
[Brains-XDEV] Loaded 20+ nodes successfully
```

Search for "Brains-XDEV" in the node menu to access all nodes.

### 3. Try a Workflow

Load any workflow from `workflows/basic/` to get started, or check `workflows/advanced/` for professional examples.

## 🏗️ Development Setup

For development, this project uses a symlink structure to enable hot-reloading:

### Create Development Symlink

**Use PowerShell as Administrator** (or enable Windows "Developer Mode" to create symlinks without admin):

```powershell
# Adjust only if your ComfyUI path differs
$DevSrc = "C:\development_node\Brains-XDEV\src"
$ComfyTarget = "C:\comfy\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-Brains-XDEV"

# Remove any previous folder/link
if (Test-Path $ComfyTarget) { Remove-Item $ComfyTarget -Recurse -Force }

# Create directory symlink (preferred)
cmd /c mklink /D "$ComfyTarget" "$DevSrc"
```

If symlinks are blocked, create a junction instead:

```powershell
cmd /c mklink /J "$ComfyTarget" "$DevSrc"
```

### 3. VS Code Development

Open the `Brains-XDEV.code-workspace` file in VS Code to get both your source code and ComfyUI in one workspace.

### 4. Running ComfyUI

Use the VS Code tasks:
- **Terminal → Run Task → Install Brains-XDEV requirements (embedded)** - Install dependencies
- **Terminal → Run Task → Run ComfyUI (Portable)** - Start ComfyUI

Or use the launch configuration from the Run and Debug panel.

### 5. Installing Dependencies

Always use the embedded Python interpreter:

```powershell
C:\comfy\ComfyUI_windows_portable\python_embeded\python.exe -m pip install <package>
```

## 📋 Node Categories

### 🧠 PromptBrain Nodes
- `BrainsXDEV_PromptBrainSource` - Create/load BRAIN databases
- `BrainsXDEV_PromptBrainLearnDirect` - Learn from prompts with style categories
- `BrainsXDEV_PromptBrainSuggestDirect` - Generate AI-powered prompt suggestions
- `BrainsXDEV_PromptBrainPerformanceDirect` - Analyze quality trends
- `BrainsXDEV_PromptBrainResetDirect` - Reset learning data
- `BrainsXDEV_PromptBrainQualityScore` - Multi-dimensional quality scoring
- `BrainsXDEV_PromptBrainKSamplerDirect` - Quality-optimized sampling
- `BrainsXDEV_PromptBrainParameterOptimizer` - AI parameter optimization

### 🤖 AI Analysis Nodes
- `BrainsXDEV_Florence2Adapter` - Vision model for detailed captions
- `BrainsXDEV_EnhancedWD14Tagger` - GPU-accelerated image tagging
- `BrainsXDEV_AnalyzeBrain` - Comprehensive BRAIN data analysis

### 🛠️ Utility Nodes
- `BrainsXDEV_CleanupMemory` - Memory management utilities
- `BrainsXDEV_ComfyUIStatusCheck` - System health monitoring
- Example nodes for testing and development

## 🎨 Workflow Collection

### Basic Templates (`workflows/basic/`)
Quick-start workflows for learning the system:
- Simple learning loop
- Quality analysis
- Memory operations
- Tag extraction
- Style learning

### Advanced Automation (`workflows/advanced/`)
Production-ready professional workflows:

**Quality Pipeline** - Iterative learning with quality feedback
**Style Transfer Learning** - Extract and apply artistic styles from references
**Parameter Optimization** - AI-driven generation settings tuning

### Experimental (`workflows/experimental/`)
Creative and experimental concepts:

**Ouroboros Engine** (32 nodes) - Self-consuming recursive evolution
**Schizophrenic Tribunal** (35 nodes) - Multi-personality AI competition
**Corrupted Oracle** (22 nodes) - Adversarial quality degradation
**Temporal Paradox** (28 nodes) - Time-loop causality violations

### Professional Creative (`workflows/advanced/`)
High-end creative workflows:

**Professional Portrait Studio** (25 nodes) - Studio photography with AI refinement
**Fashion Photography** (33 nodes) - Editorial fashion with 3-gen evolution
**Character Concept Art** (32 nodes) - Fantasy/game character design
**Artistic Figure Studies** (31 nodes) - Academic figure drawing approach

## 🔧 Project Structure

```
comfyui-Brains/
├── src/                          # Node implementations
│   ├── __init__.py              # Node registration
│   ├── brain_datatype.py        # BRAIN system (2,164 lines)
│   ├── brain_data.py            # BrainData class
│   ├── brain_source.py          # BRAIN loader
│   ├── brain_learn.py           # Learning node
│   ├── florence2_adapter.py     # Vision analysis
│   ├── enhanced_wd14_tagger.py  # Image tagging
│   ├── analyze_brain.py         # Data analysis
│   └── ...                      # Utility nodes
├── workflows/                    # Workflow collection
│   ├── basic/                   # 5 starter workflows
│   ├── advanced/                # 7 professional workflows
│   └── experimental/            # 4 experimental workflows
├── tests/                        # Unit tests
├── tools/                        # Development utilities
├── examples/                     # Example files
├── .github/                      # GitHub configuration
│   └── copilot-instructions.md  # AI pair programming guide
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
├── README.md                    # This file
└── TESTING.md                   # Testing guidelines
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_brain_datatype.py

# With coverage
pytest --cov=src tests/
```

## 📚 Documentation

- **[Quick Reference](workflows/advanced/QUICK_REFERENCE.md)** - Node parameters and common patterns
- **[Workflow Guide](workflows/INDEX.md)** - Complete workflow documentation
- **[Testing Guide](TESTING.md)** - Development and testing guidelines
- **[GitHub Copilot Instructions](.github/copilot-instructions.md)** - AI development patterns

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow the existing code patterns
4. Add tests for new features
5. Submit a pull request

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- **ComfyUI** - The amazing node-based interface
- **Microsoft Florence2** - Powerful vision language model
- **WD14 Tagger** - Anime/general image tagging
- **Community** - For inspiration and feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/aiforhumans/Brains/issues)
- **Discussions**: [GitHub Discussions](https://github.com/aiforhumans/Brains/discussions)

## 🗺️ Roadmap

- [ ] Multi-BRAIN collaboration nodes
- [ ] Real-time quality feedback visualization
- [ ] Advanced style mixing and interpolation
- [ ] Export/import BRAIN templates
- [ ] Web UI for BRAIN management
- [ ] More professional workflow templates

---

**Made with 🧠 for the ComfyUI community**
# Changelog

All notable changes to comfyui-Brains will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX (Initial Release)

### 🎉 Features

#### BRAIN Learning System
- **BrainData Custom Datatype** - Complete datatype ecosystem for AI learning workflows
- **Persistent Learning** - SQLite-backed memory with automatic quality tracking
- **Style Categories** - Support for artistic style classification and learning
- **Quality Scoring** - Multi-dimensional quality metrics (technical/artistic/semantic)
- **Performance Analytics** - Comprehensive quality trend analysis and reporting
- **Smart Suggestions** - AI-powered prompt generation based on learned patterns
- **Parameter Optimization** - Intelligent sampling parameter tuning

#### AI Analysis Nodes (8 nodes)
- `BrainsXDEV_PromptBrainSource` - BRAIN database creation and loading with auto-discovery
- `BrainsXDEV_PromptBrainLearnDirect` - Direct learning from prompts with style categories
- `BrainsXDEV_PromptBrainSuggestDirect` - Enhanced prompt suggestions with creativity control
- `BrainsXDEV_PromptBrainPerformanceDirect` - Comprehensive performance analysis
- `BrainsXDEV_PromptBrainResetDirect` - Data reset with backup and selective options
- `BrainsXDEV_PromptBrainQualityScore` - AI-powered quality scoring system
- `BrainsXDEV_PromptBrainKSamplerDirect` - Quality-optimized KSampler integration
- `BrainsXDEV_PromptBrainParameterOptimizer` - AI-driven parameter optimization

#### Vision & Tagging (3 nodes)
- `BrainsXDEV_Florence2Adapter` - Microsoft Florence2 vision model integration
- `BrainsXDEV_EnhancedWD14Tagger` - GPU-accelerated WD14 anime/general tagging
- `BrainsXDEV_AnalyzeBrain` - Comprehensive BRAIN data analysis and reporting

#### Utility Nodes (9+ nodes)
- `BrainsXDEV_CleanupMemory` - Memory management utilities
- `BrainsXDEV_ComfyUIStatusCheck` - System health monitoring
- Example and testing nodes for development

### 🎨 Workflows (16 total)

#### Basic Templates (5 workflows)
- Simple learning loop for getting started
- Quality analysis workflow
- Memory operations demonstration
- Tag extraction examples
- Style learning basics

#### Advanced Automation (7 workflows)
- **Quality Analysis Pipeline** - Iterative learning with quality feedback loops
- **Style Transfer Learning** - Extract and apply artistic styles from reference images
- **Parameter Optimization** - AI-driven generation settings tuning
- **Iterative Learning Loop** - Multi-stage learning workflow
- **Professional Portrait Studio** (25 nodes) - Studio photography with AI refinement
- **Fashion Photography** (33 nodes) - Editorial fashion with 3-generation evolution
- **Artistic Figure Studies** (31 nodes) - Academic figure drawing approach

#### Experimental Workflows (4 workflows)
- **Ouroboros Engine** (32 nodes, 55 links) - Self-consuming recursive evolution
- **Schizophrenic Tribunal** (35 nodes, 48 links) - Multi-personality AI competition
- **Corrupted Oracle** (22 nodes, 35 links) - Adversarial quality degradation
- **Temporal Paradox** (28 nodes, 45 links) - Time-loop causality violations

### 🐛 Bug Fixes

#### Florence2 Adapter
- Fixed ONNX model path resolution
- Fixed GPU/CPU device detection
- Fixed output format for CAPTION and DETAILED_CAPTION tasks
- Fixed batch processing for multiple images
- Added proper error handling for missing models

#### Memory & Learning
- Fixed SQLite connection handling and thread safety
- Fixed quality score calculation edge cases
- Fixed style category persistence
- Fixed BRAIN data serialization for complex objects
- Fixed learning from empty or invalid prompts

#### Workflow Validation
- Fixed Zod schema validation errors across all workflows
- Removed invalid null links from workflow JSON (8 links total)
- Fixed duplicate link IDs in style_transfer_learning.json
- Fixed node parameter validation in 10+ workflows
- Fixed UI-breaking workflow structure issues

#### Node Registration
- Fixed node display names for consistency
- Fixed category organization (Brains-XDEV/*)
- Fixed RETURN_TYPES and RETURN_NAMES alignment
- Fixed hidden parameter handling (unique_id, prompt, extra_pnginfo)

### 📝 Documentation
- Comprehensive README with installation and usage
- Detailed Copilot instructions for development
- Testing guidelines and examples
- Quick reference guide for all nodes
- Workflow documentation and use cases

### 🔧 Technical Improvements
- Symlink-based hot-reload development structure
- Embedded Python interpreter support
- pyproject.toml configuration
- Comprehensive test suite with pytest
- WebSocket API testing utilities
- VS Code tasks and launch configurations

### 📦 Dependencies
- numpy (core operations)
- torch (AI/ML operations)
- pillow (image processing)
- psutil (memory management)
- pytest (testing)
- websockets (API testing)

### 🎯 Statistics
- **Total Nodes**: 20+
- **Total Workflows**: 16
- **Code Lines**: 2,164 lines (brain_datatype.py alone)
- **Total Workflow Nodes**: ~238 nodes (professional + experimental)
- **Total Workflow Links**: ~375 links
- **JSON Workflow Lines**: ~8,500+ lines

---

## [Unreleased]

### Planned Features
- Multi-BRAIN collaboration nodes
- Real-time quality feedback visualization
- Advanced style mixing and interpolation
- Export/import BRAIN templates
- Web UI for BRAIN management
- More professional workflow templates
- Enhanced model management system
- Cloud synchronization for BRAIN databases

---

## Release Notes

### Version 1.0.0 Highlights

This initial release represents a comprehensive AI learning and analysis system for ComfyUI. The BRAIN datatype ecosystem enables sophisticated workflows that learn from user feedback, optimize generation parameters, and provide detailed quality analysis.

**Key Innovations:**
- **Learning System**: First ComfyUI custom datatype for persistent AI learning
- **Quality Tracking**: Multi-dimensional quality metrics with trend analysis
- **Smart Generation**: AI-driven parameter optimization and prompt suggestions
- **Professional Workflows**: Production-ready templates for various creative workflows
- **Experimental Concepts**: Cutting-edge workflow architectures pushing ComfyUI limits

**Validation & Quality:**
- All workflows validated against ComfyUI Zod schema
- Comprehensive error handling and user feedback
- Extensive testing with pytest suite
- Production-tested with CUDA RTX 5080

### Migration Guide

This is the initial release, no migration needed.

### Known Issues

- Florence2 models require manual download to `models/florence2/` directory
- WD14 models require manual download for GPU acceleration
- Large BRAIN databases (>10,000 entries) may experience slower query times
- Some experimental workflows require high VRAM (16GB+ recommended)

### Support

For bugs, feature requests, or questions:
- GitHub Issues: https://github.com/aiforhumans/Brains/issues
- GitHub Discussions: https://github.com/aiforhumans/Brains/discussions

---

**Previous versions**: None (initial release)

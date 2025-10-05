# Brains-XDEV Workflow Templates

Comprehensive workflow templates for all Brains-XDEV nodes with built-in debugging capabilities.

## Directory Structure

### 📁 `brain_datatype/`
Advanced BRAIN custom datatype workflows for the 8 core PromptBrain nodes:
- **PromptBrain Source** - BRAIN data creation and loading
- **PromptBrain Learn** - Learning from prompts with scoring
- **PromptBrain Suggest** - Enhanced prompt generation
- **PromptBrain Performance** - Performance analysis and reporting
- **PromptBrain Reset** - Data reset with backup options
- **PromptBrain Quality Score** - AI-powered quality analysis
- **PromptBrain KSampler** - Intelligent sampling with optimization
- **PromptBrain Parameter Optimizer** - AI parameter tuning

### 📁 `ai_adapters/`
AI model adapter workflows:
- **Florence2 Adapter** - Image captioning with Florence-2
- **WD14 Adapter** - Anime/booru tagging with WD14
- **Tagger (stub)** - Basic tagging interface
- **Captioner (stub)** - Basic captioning interface

### 📁 `memory_utils/`
Memory and utility node workflows:
- **Memory Read/Write** - SQLite database operations
- **Scorer** - Manual quality scoring
- **Prompt Suggester** - Prompt enhancement
- **EMA Ranker** - Exponential moving average ranking
- **Brightness Example** - Basic image processing example

### 📁 `complete_demos/`
Full end-to-end demonstration workflows:
- **Complete PromptBrain Pipeline** - Full learning and generation cycle
- **AI Quality Analysis Pipeline** - Multi-model quality assessment
- **Prompt Learning System** - Automated prompt improvement
- **Debug All Nodes** - Comprehensive debugging template

## Workflow Features

Each workflow template includes:

✅ **Pre-configured Debug Nodes**
- ShowText nodes for string outputs
- Show any [Crystools] for complex data types
- Console logging for status tracking

✅ **Error Handling**
- Graceful fallbacks for missing models
- Clear error messages
- Status indicators

✅ **Documentation**
- Inline comments explaining each node
- Parameter descriptions
- Expected input/output formats

✅ **Test Data**
- Sample images included
- Example prompts provided
- Pre-configured settings

## Usage

1. **Load Template**: Open any `.json` workflow file in ComfyUI
2. **Configure**: Adjust node parameters as needed
3. **Add Image**: Load your test image (if required)
4. **Queue Prompt**: Execute the workflow
5. **Review Debug Output**: Check ShowText and Show any nodes

## Testing Workflows

Use workflows in order of complexity:

1. Start with **basic examples** (`brightness_example.json`)
2. Test **individual nodes** (templates in respective directories)
3. Try **AI adapters** (requires model downloads)
4. Run **BRAIN datatype** workflows (advanced features)
5. Execute **complete demos** (full pipeline)

## Debugging Tips

- Check console output for `[Brains-XDEV]` messages
- Review ShowText nodes for string outputs
- Use Show any [Crystools] for complex data inspection
- Enable all debug nodes when troubleshooting
- Check node status indicators (green = success, red = error)

## Creating Custom Workflows

Based on these templates, you can:

1. **Combine nodes** for custom pipelines
2. **Add your own debug nodes** as needed
3. **Modify parameters** for your use case
4. **Save variations** with descriptive names
5. **Share workflows** with consistent structure

## Node Requirements

Some workflows require additional dependencies:

- **Florence2 Adapter**: `transformers`, `torch`
- **WD14 Adapter**: `onnxruntime`
- **Memory Nodes**: Core dependencies only
- **Quality Score**: Core dependencies only

Install optional dependencies with:
```bash
C:/comfy/ComfyUI_windows_portable/python_embeded/python.exe -m pip install transformers torch onnxruntime
```

## Support

For issues with workflows:

1. Check console for error messages
2. Verify node is loaded in ComfyUI
3. Review workflow README for requirements
4. Test with simpler workflow first
5. Check GitHub issues for similar problems

---

**Created**: October 2025  
**Project**: Brains-XDEV  
**Purpose**: Workflow templates with comprehensive debugging

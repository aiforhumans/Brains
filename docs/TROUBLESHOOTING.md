# 🔧 Troubleshooting Guide

Common issues and solutions for comfyui-Brains.

## 📚 Quick Links

- [Installation Issues](#-installation-issues)
- [Node Loading Problems](#-node-loading-problems)
- [Workflow Errors](#-workflow-errors)
- [Model & Performance Issues](#-model--performance-issues)
- [BRAIN Database Issues](#-brain-database-issues)
- [Memory & VRAM Issues](#-memory--vram-issues)

---

## 🔌 Installation Issues

### Nodes Not Appearing in ComfyUI

**Symptoms:**
- Can't find "Brains-XDEV" nodes in node search
- No import messages in console

**Solutions:**

1. **Verify installation location:**
```bash
# Check if folder exists
ls ComfyUI/custom_nodes/comfyui-Brains
# Should show: src/, workflows/, requirements.txt, etc.
```

2. **Check console for errors:**
```
# Look for these messages on ComfyUI startup:
[Brains-XDEV] brain_datatype import
[Brains-XDEV] florence2_adapter import
[Brains-XDEV] Loaded 20+ nodes successfully
```

3. **Reinstall dependencies:**
```bash
cd ComfyUI/custom_nodes/comfyui-Brains
pip install -r requirements.txt --upgrade
```

4. **Clear Python cache:**
```bash
# Windows PowerShell
Get-ChildItem -Recurse -Force | Where-Object { $_.Name -eq "__pycache__" } | Remove-Item -Recurse -Force

# Linux/Mac
find . -type d -name "__pycache__" -exec rm -r {} +
```

5. **Restart ComfyUI completely** (not just reload)

---

### ImportError: No module named 'X'

**Symptoms:**
```
ImportError: No module named 'numpy'
ImportError: No module named 'torch'
```

**Solutions:**

1. **Install missing dependencies:**
```bash
pip install numpy torch pillow
```

2. **Use ComfyUI's embedded Python:**
```bash
# Windows
C:/comfy/ComfyUI_windows_portable/python_embeded/python.exe -m pip install -r requirements.txt

# Or add to system PATH and use:
python -m pip install -r requirements.txt
```

3. **Check Python version:**
```bash
python --version  # Should be 3.10 or higher
```

---

## 🎯 Node Loading Problems

### Node Shows "Error Loading Node"

**Symptoms:**
- Node appears but shows red error state
- Console shows import errors

**Solutions:**

1. **Check src/__init__.py registration:**
```python
# Verify node is registered:
NODE_CLASS_MAPPINGS = {
    "NodeClass": NodeClass,  # Should match your node
}
```

2. **Check node file for syntax errors:**
```bash
python -m py_compile src/your_node.py
```

3. **Verify RETURN_TYPES format:**
```python
RETURN_TYPES = ("TYPE",)  # Must be tuple, even for single return
# NOT: RETURN_TYPES = "TYPE"  # ❌ Wrong
```

4. **Check INPUT_TYPES structure:**
```python
@classmethod
def INPUT_TYPES(cls):  # Must be classmethod
    return {
        "required": {},  # Must have required, even if empty
    }
```

---

### Node Missing from Category

**Symptoms:**
- Node imported successfully but can't find in UI
- Shows in different category than expected

**Solutions:**

1. **Check CATEGORY field:**
```python
CATEGORY = "Brains-XDEV/SubCategory"  # Check spelling/capitalization
```

2. **Check display name mapping:**
```python
NODE_DISPLAY_NAME_MAPPINGS = {
    "NodeClass": "Brains-XDEV • Node Name",  # Verify this exists
}
```

3. **Clear ComfyUI cache:**
- Close ComfyUI
- Delete `ComfyUI/temp/` folder
- Restart

---

## 🌐 Workflow Errors

### Validation Error: "Expected number, received null"

**Symptoms:**
```
Zod schema validation error at links[X][3]
Expected number, received null
```

**Solutions:**

**This is a link format error.** Invalid workflow JSON with null values in links.

**Fix manually:**
1. Open workflow JSON in text editor
2. Find the problematic link (check line number from error)
3. Remove the entire link entry if output is unused:

**Before (wrong):**
```json
"links": [
  [20, 15, 3, null, null, null],  // ❌ Invalid
  [21, 16, 0, 17, 0, "IMAGE"]     // ✅ Valid
]
```

**After (correct):**
```json
"links": [
  [21, 16, 0, 17, 0, "IMAGE"]     // Only keep valid links
]
```

**Prevention:**
- Don't create link entries for unused outputs
- Only include links for actual connections

---

### "Node Not Found" Error

**Symptoms:**
```
Error: Node type "BrainsXDEV_NodeName" not found
```

**Solutions:**

1. **Node renamed or removed:**
   - Check CHANGELOG.md for renamed nodes
   - Update workflow to use new node name

2. **Old workflow format:**
   - Node might have been in old version
   - Check workflows/INDEX.md for updated versions

3. **Missing installation:**
   - Verify comfyui-Brains is installed
   - Check console for import errors

---

### Workflow Won't Load

**Symptoms:**
- JSON error when loading workflow
- UI freezes or shows error

**Solutions:**

1. **Validate JSON:**
```bash
# Use online JSON validator or:
python -m json.tool your_workflow.json
```

2. **Check for duplicates:**
   - Duplicate node IDs
   - Duplicate link IDs
   - Use text search: Find "\"id\": 5" to check

3. **Verify version compatibility:**
```json
{
  "version": 0.4  // Should match ComfyUI version
}
```

---

## 🤖 Model & Performance Issues

### Florence2 Model Not Found

**Symptoms:**
```
Error: Florence2 model not found at models/florence2/...
```

**Solutions:**

1. **Download Florence2 models:**
```bash
# Create model directory
mkdir -p models/florence2

# Download model from HuggingFace (manual)
# Visit: https://huggingface.co/microsoft/Florence-2-large
# Download ONNX model files to models/florence2/
```

2. **Check model path in node:**
   - Default: `models/florence2/model.onnx`
   - Update path parameter if different location

3. **Verify files exist:**
```bash
ls models/florence2/
# Should show: model.onnx, config.json, etc.
```

---

### WD14 Tagger Not Working

**Symptoms:**
```
Error: WD14 model not available
```

**Solutions:**

1. **Install ONNX runtime:**
```bash
# For GPU:
pip install onnxruntime-gpu

# For CPU:
pip install onnxruntime
```

2. **Download WD14 model:**
```bash
mkdir -p models/wd14
# Download from HuggingFace: SmilingWolf/wd-v1-4-*
```

3. **Check GPU availability:**
```python
# In Python console:
import torch
print(torch.cuda.is_available())  # Should be True for GPU
```

---

### Slow Generation / Performance Issues

**Symptoms:**
- Workflows take very long to complete
- High memory usage
- System freezes

**Solutions:**

1. **Reduce image size:**
   - Start with 512x512
   - Scale up after testing

2. **Lower batch size:**
   - Set batch_size=1 for learning workflows
   - Higher batches only for testing

3. **Enable xformers:**
```bash
pip install xformers
# ComfyUI will auto-detect and use for memory efficiency
```

4. **Close other programs:**
   - Free up RAM and VRAM
   - Close browsers, other AI tools

5. **Check VRAM usage:**
   - Experimental workflows need 12-16GB+ VRAM
   - Use Task Manager / nvidia-smi to monitor

---

## 🧠 BRAIN Database Issues

### Database Locked Error

**Symptoms:**
```
SQLite error: database is locked
```

**Solutions:**

1. **Close other connections:**
   - Stop any other workflows using same database
   - Close database analysis tools

2. **Restart ComfyUI:**
   - Cleans up stale connections

3. **Check file permissions:**
```bash
# Windows
icacls promptbrain.db

# Linux/Mac
ls -la promptbrain.db
chmod 644 promptbrain.db  # If needed
```

4. **Create new database:**
   - Use PromptBrainResetDirect node
   - Or delete old .db file and recreate

---

### Data Not Persisting

**Symptoms:**
- Learned data not saved
- Database resets after restart

**Solutions:**

1. **Check database path:**
   - Absolute paths work better than relative
   - Example: `C:/comfy/data/promptbrain.db` not `./data/brain.db`

2. **Verify write permissions:**
   - Check folder is writable
   - Not in Program Files (Windows)

3. **Check for errors in console:**
   - Look for SQLite errors during learning
   - Check for disk space issues

---

### Quality Scores Not Updating

**Symptoms:**
- All quality scores show 0.0
- Performance analysis empty

**Solutions:**

1. **Enable quality scoring:**
   - Check PromptBrainQualityScore node is connected
   - Verify it's before PromptBrainLearnDirect in workflow

2. **Check score parameters:**
```python
quality_score = 0.0  # ❌ Wrong - manual override disabled
quality_score = None  # ✅ Correct - enable auto-scoring
```

3. **Verify learning is happening:**
   - Check console for "[Brains-XDEV] Learning from prompt..."
   - Use AnalyzeBrain node to inspect database

---

## 💾 Memory & VRAM Issues

### Out of Memory (OOM) Error

**Symptoms:**
```
CUDA out of memory
RuntimeError: CUDA out of memory. Tried to allocate X GB
```

**Solutions:**

1. **Reduce image resolution:**
   - 512x512 instead of 1024x1024
   - Or use latent space operations

2. **Lower batch size:**
```python
batch_size = 1  # Instead of 4
```

3. **Use CPU offloading:**
   - Check ComfyUI settings for CPU offload options
   - Slower but uses less VRAM

4. **Clear VRAM between generations:**
   - Use CleanupMemory node in workflow
   - Or add manual clearing:
```python
import torch
torch.cuda.empty_cache()
```

5. **Close other GPU applications:**
   - Close browsers with GPU acceleration
   - Close other AI tools

6. **Check VRAM usage:**
```bash
# Windows
nvidia-smi

# Monitor continuously
nvidia-smi -l 1
```

---

### Memory Leak / Increasing Usage

**Symptoms:**
- Memory usage grows with each generation
- Eventually runs out of memory

**Solutions:**

1. **Add CleanupMemory nodes:**
   - Place after major generation steps
   - Use `aggressive=True` for deep cleaning

2. **Restart ComfyUI periodically:**
   - For long batch jobs, restart every 50-100 generations

3. **Update to latest version:**
   - Memory leaks may be fixed in updates

4. **Check for circular references:**
   - In custom workflows
   - Remove unnecessary data storage

---

## 📞 Getting Help

### Before Opening an Issue

1. **Check console for errors:**
   - Full error message
   - Stack trace

2. **Verify versions:**
```bash
# ComfyUI version
git rev-parse HEAD  # In ComfyUI directory

# Python version
python --version

# CUDA version (if using GPU)
nvidia-smi
```

3. **Try with minimal workflow:**
   - Use basic template workflows
   - Isolate the problematic node

4. **Check if issue is known:**
   - Search existing GitHub issues
   - Check CHANGELOG for known issues

### Opening an Issue

Include:
- **ComfyUI version**
- **comfyui-Brains version**
- **Python version**
- **Full error message** (from console)
- **Workflow JSON** (if applicable)
- **Steps to reproduce**
- **Expected vs actual behavior**

**Template:**
```markdown
**Environment:**
- ComfyUI: v0.3.62
- comfyui-Brains: v1.0.0
- Python: 3.10.11
- OS: Windows 11
- GPU: RTX 4090 24GB

**Issue:**
[Describe the problem]

**Steps to Reproduce:**
1. Load workflow X
2. Set parameter Y
3. Click Generate

**Error Message:**
```
[Paste full error from console]
```

**Expected:** [What should happen]
**Actual:** [What actually happens]
```

### Community Support

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general help
- **ComfyUI Discord**: General ComfyUI help

---

## 📚 Additional Resources

- **[README.md](../README.md)** - Installation and overview
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guide
- **[TESTING.md](TESTING.md)** - Testing guidelines
- **[Workflow Index](../workflows/INDEX.md)** - Workflow documentation
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history

---

**Still stuck? Open an issue on GitHub! 🧠**

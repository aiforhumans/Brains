# 🚨 Quick Fix Guide - Florence2 & MemoryWrite Errors

## Error 1: Florence2 Dtype Mismatch ✅ FIXED & TESTED

**Error Message:**
```
RuntimeError: Input type (float) and bias type (struct c10::Half) should be the same
```

**Status:** ✅ Fixed and confirmed working!

**Console Output:**
```
✅ [Brains-XDEV] Florence2 inputs moved to cuda:0 with dtype torch.float16
```

---

## Error 2: Florence2 past_key_values ✅ FIXED

**Error Message:**
```
AttributeError: 'NoneType' object has no attribute 'shape'
past_length = past_key_values[0][0].shape[2]
```

**What Happened:**
- Florence2 generation tries to use KV cache by default
- Cache wasn't initialized, causing NoneType error

**Fix Applied:**
- Added `use_cache=False` to generation parameters
- Disables key-value caching for simpler, more reliable generation

**Status:** ✅ Fixed in code, restart ComfyUI to apply

---

## Error 3: MemoryWrite Image Parameter ⚠️ ACTION NEEDED

**Error Message:**
```
TypeError: BrainsXDEV_MemoryWrite.run() got an unexpected keyword argument 'image'
```

**What Happened:**
- You're using a **cached old workflow** from browser/session
- The workflow has an old `image` input that no longer exists
- The repository file is already correct!

**Fix Required - Choose ONE:**

### Option A: Reload Workflow from Disk (Recommended)
1. In ComfyUI web interface
2. Click **Menu** (☰) → **Load**
3. Navigate to: `workflows/complete_demos/`
4. Load: `debug_all_nodes_FIXED.json` or `debug_all_nodes.json`
5. Click **Queue Prompt**

### Option B: Clear Browser Cache
1. Press **Ctrl+Shift+R** (hard refresh)
2. Or clear ComfyUI browser cache
3. Reload ComfyUI page
4. Load workflow again

### Option C: Manual Fix (if needed)
1. In loaded workflow, find **MemoryWrite** node (node #9)
2. Disconnect the **IMAGE** input link
3. Should only have: `caption` and `score` inputs
4. Save workflow

---

## Testing Checklist

After applying fixes:

### 1. Restart ComfyUI ✅
```powershell
# Stop current ComfyUI (Ctrl+C in terminal)
# Then restart
```

### 2. Reload Workflow ⚠️
- Use Menu → Load → `debug_all_nodes_FIXED.json`
- **Don't** use cached workflow

### 3. Queue and Test 🧪
- Click **Queue Prompt**
- Watch console output
- Check for these success messages:

```
✅ [Brains-XDEV] Florence2 inputs moved to cuda with dtype torch.float16
✅ [Brains-XDEV] Florence2 caption generated: ...
✅ ok:memory_write:...
```

### 4. Verify No Errors ✅
Should NOT see:
- ❌ "Input type (float) and bias type" (FIXED ✅)
- ❌ "'NoneType' object has no attribute 'shape'" (FIXED ✅)
- ❌ "unexpected keyword argument 'image'"

---

## Visual Workflow Check

### MemoryWrite Node Should Look Like:

```
💾 Save to Memory (BrainsXDEV_MemoryWrite)
┌─────────────────────────┐
│ Inputs:                 │
│  ├─ caption (STRING) ←  │ from Florence2
│  └─ score (FLOAT) ←     │ from Quality Score
│                         │
│ Outputs:                │
│  ├─ status (STRING) →   │ to ShowText
│  └─ row_id (INT)        │
└─────────────────────────┘
```

### ❌ OLD (Wrong):
```
Has IMAGE input ← from LoadImage  ❌ Remove this!
```

### ✅ NEW (Correct):
```
No IMAGE input
Only caption and score inputs
```

---

## Still Having Issues?

### Check Console Logs:
Look for these startup messages:
```
[Brains-XDEV] Loaded 20 nodes total
[Brains-XDEV] Successfully loaded 20 nodes
```

### Verify Files Changed:
```powershell
# Check file modification time
Get-Item "c:\comfy\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-Brains\src\promptbrain\florence2_adapter.py" | Select-Object LastWriteTime
```

Should show recent timestamp (today's date).

### Clear Python Cache:
```powershell
# Navigate to Brains directory
cd "c:\comfy\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-Brains"

# Remove cache
Remove-Item -Recurse -Force src\__pycache__
Remove-Item -Recurse -Force src\promptbrain\__pycache__
```

### Test Individual Nodes:
1. Test Florence2 alone first
2. Test MemoryWrite alone  
3. Then test full workflow

---

## Expected Results

### Florence2 Console Output:
```
[Brains-XDEV] Florence2 input type: <class 'torch.Tensor'>
[Brains-XDEV] Florence2 processing image type: <class 'torch.Tensor'>, shape: torch.Size([1, 768, 768, 3])
[Brains-XDEV] Loading Florence-2 model: microsoft/Florence-2-base
[Brains-XDEV] Florence-2 model loaded on CUDA
[Brains-XDEV] Florence2 removing batch dimension: (1, 768, 768, 3)
[Brains-XDEV] Florence2 PIL image created: <class 'PIL.Image.Image'>, size: (768, 768)
[Brains-XDEV] Florence2 inputs moved to cuda with dtype torch.float16  ← NEW!
[Brains-XDEV] Florence2 caption generated: a woman with long hair...
```

### MemoryWrite Output:
```
Status: "ok:memory_write:9"  ← Node executed successfully
```

---

## Summary

| Issue | Status | Action |
|-------|--------|--------|
| Florence2 dtype | ✅ Fixed | Restart ComfyUI |
| MemoryWrite image param | ⚠️ User cache | Reload workflow |
| Batch dimensions | ✅ Working | No action |
| Code changes | ✅ Complete | Applied |

**Next Step:** Reload workflow file → Queue prompt → Success! 🎉

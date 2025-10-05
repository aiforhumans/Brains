# Workflow Validation Fixes

## Issues Found and Fixed - iterative_learning_loop.json

### ❌ Error 1: Invalid Parameters in Node 16 (PromptBrainSuggestDirect)
**Console Output:**
```
Failed to validate prompt for output 18:
* BrainsXDEV_PromptBrainSuggestDirect 16:
  - Value 0 smaller than min of 1: suggestion_count
  - Value 5.0 bigger than max of 1.0: quality_threshold
  - Failed to convert an input value to a FLOAT value: creativity, photorealistic
  - Value not in list: target_style: 'improve' not in ['none', 'photorealistic', ...]
```

**Root Cause:**
Wrong widget_values order and invalid values in workflow JSON.

**Fix Applied:**
```json
"widgets_values": [
  "",              // base_prompt (STRING)
  3,               // suggestion_count (INT, min=1, max=10)
  1.0,             // creativity (FLOAT, min=0.0, max=2.0)
  "none",          // target_style (ENUM, default="none")
  0.3              // quality_threshold (FLOAT, min=0.0, max=1.0)
]
```

**Changed From:**
```json
"widgets_values": [
  "",                  // base_prompt
  0.8,                 // ❌ Wrong position/type
  "photorealistic",    // ❌ Wrong position
  "improve",           // ❌ Invalid enum value
  5,                   // ❌ Was 0, changed to 5 but still wrong position
  1.2,                 // ❌ creativity in wrong position
  0.7                  // ❌ quality_threshold in wrong position
]
```

### ❌ Error 2: Wrong Output Types in Node 16
**Console Output:**
```
Return type mismatch between linked nodes: 
received_type(BRAIN) mismatch input_type(STRING)
```

**Root Cause:**
Workflow was using old output signature that doesn't match the actual node implementation.

**Fix Applied:**
Updated outputs to match actual BrainsXDEV_PromptBrainSuggestDirect implementation:
```json
"outputs": [
  {"name": "brain_data", "type": "BRAIN", "links": null},
  {"name": "suggestion_1", "type": "STRING", "links": [21]},
  {"name": "suggestion_2", "type": "STRING", "links": null},
  {"name": "suggestion_3", "type": "STRING", "links": null}
]
```

**Changed From:**
```json
"outputs": [
  {"name": "suggested_prompt", "type": "STRING", "links": [21]},
  {"name": "suggestion_metadata", "type": "DICT", "links": [22]},  // ❌ Wrong type
  {"name": "confidence", "type": "FLOAT", "links": null}           // ❌ Wrong type
]
```

### ❌ Error 3: Invalid Input Connection (target_score)
**Root Cause:**
Node 16 had an input `target_score` that doesn't exist in the actual node implementation.

**Fix Applied:**
Removed the invalid input:
```json
"inputs": [
  {"name": "brain_data", "type": "BRAIN", "link": 19},
  {"name": "base_prompt", "type": "STRING", "widget": {"name": "base_prompt"}, "link": 13}
  // ❌ Removed: {"name": "target_score", "type": "FLOAT", "link": 15}
]
```

### ❌ Error 4: Invalid Link 15 and Link 22
**Fix Applied:**
Removed unused links from the links array:
- Link 15: Was connecting Quality Score to non-existent `target_score` input
- Link 22: Was connecting to wrong output type (DICT instead of STRING)

Updated links array to remove these invalid connections.

### ✅ Node 18: Updated for Consistency
Changed from `Show any [Crystools]` to `ShowText|pysssss` for consistency with other debug nodes.

## Actual Node Signature Reference

### BrainsXDEV_PromptBrainSuggestDirect (brain_datatype.py)

**INPUT_TYPES:**
```python
"required": {
    "brain_data": ("BRAIN", {"forceInput": True}),
    "base_prompt": ("STRING", {"multiline": True, "default": ""}),
    "suggestion_count": ("INT", {"default": 3, "min": 1, "max": 10}),
    "creativity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1})
},
"optional": {
    "target_style": (["none", "photorealistic", "artistic", "anime", "fantasy", 
                     "portrait", "landscape", "cinematic", "vintage", "modern", 
                     "abstract", "minimalist"], {"default": "none"}),
    "quality_threshold": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.1})
}
```

**RETURN_TYPES:**
```python
RETURN_TYPES = ("BRAIN", "STRING", "STRING", "STRING")
RETURN_NAMES = ("brain_data", "suggestion_1", "suggestion_2", "suggestion_3")
```

## Testing Status

✅ **Fixed workflow should now validate successfully**

### Updated Workflow Structure:
- Node 16 inputs: `brain_data` (BRAIN), `base_prompt` (STRING)
- Node 16 outputs: `brain_data` (BRAIN), `suggestion_1/2/3` (STRING)
- Node 17 receives: `suggestion_1` (STRING) - valid ShowText input
- Node 18: Changed to ShowText for consistency

### Next Steps:
1. Reload workflow from disk in ComfyUI (Ctrl+O or File → Load)
2. Verify no validation errors in console
3. Queue prompt to test full workflow
4. Verify suggestions generate correctly

## Lesson Learned

**Always match workflow JSON to actual node implementation:**
- Check `INPUT_TYPES` for parameter order and types
- Check `RETURN_TYPES` for output signatures
- Verify enum values are in the allowed list
- Ensure min/max constraints are respected
- Don't add inputs/outputs that don't exist in the node

**Browser caching can preserve old workflows:**
- Always reload from disk after repository updates
- Check console validation errors before queuing
- Use "Clear" → "Load" workflow instead of just loading over existing

# comfyui-custom-nodes (XDEV Starter)

A minimal, **Copilot-friendly** starter for building and testing **ComfyUI custom nodes** and running them via the **API prompt** format.

## What’s inside
- `src/my_nodes/basic_example.py` — `XDEV_Brightness` node (required/hidden inputs, simple numpy image op)
- `src/my_nodes/__init__.py` — node registration (`NODE_CLASS_MAPPINGS`, `NODE_DISPLAY_NAME_MAPPINGS`)
- `workflows/demo_ui.workflow.json` — example saved from UI-style graph
- `workflows/demo_api.prompt.json` — **Save (API Format)**-style prompt for programmatic runs
- `tools/run_ws_client.py` — tiny WebSocket runner (requires `websockets`)
- `src/tests/test_basic_example.py` — pytest sanity tests

## Quick start
1. Drop this repo under `ComfyUI/custom_nodes/comfyui-custom-nodes` (or symlink).
2. (Optional) `pip install -U numpy pytest websockets`
3. Start ComfyUI.
4. Open the graph and wire: **LoadImage → XDEV_Brightness → PreviewImage**.
5. Or run via API prompt:
   ```bash
   python tools/run_ws_client.py workflows/demo_api.prompt.json
   ```

## Authoring guidelines (TL;DR)
- **Required vs Optional vs Hidden** inputs live in `INPUT_TYPES()`.
- Hidden keys you can request when needed:
  - `PROMPT` — full prompt graph object
  - `EXTRA_PNGINFO` — metadata dictionary
  - `UNIQUE_ID` — stable id of this node on canvas

## References
- Server / node properties: https://docs.comfy.org/custom-nodes/backend/server_overview
- Hidden inputs & more on inputs: https://docs.comfy.org/custom-nodes/backend/more_on_inputs
- Walkthrough (step-by-step): https://docs.comfy.org/custom-nodes/walkthrough
- Manager publishing: https://docs.comfy.org/custom-nodes/backend/manager
- API format vs workflow JSON (discussion): https://github.com/comfyanonymous/ComfyUI/issues/1112
- WS/API usage example: https://9elements.com/blog/hosting-a-comfyui-workflow-via-api/

## PromptBrain nodes (design stubs)

This repo includes **PromptBrain** node stubs to help you build a self-learning loop:

- `PB_WD14Tagger` — emits tags/score dict + a tag string (replace with ComfyUI-WD14-Tagger)
- `PB_Captioner` — emits a caption (BLIP, Florence-2, or external)
- `PB_Scorer` — manual rating node (0..1)
- `PB_MemoryWrite` / `PB_MemoryRead` — tiny SQLite memory
- `PB_PromptSuggester` — composes positive/negative prompts

See `workflows/demo_promptbrain.workflow.json` for wiring.

### PromptBrain Adapters (real models)

**WD14 Adapter (ONNX Runtime)**
- Place ONNX model and labels CSV, e.g.:
  - `models/wd14/wd-v1-4-swinv2-tagger-v2.onnx`
  - `models/wd14/selected_tags.csv` (the labels file from the model repo)
- Install: `pip install onnxruntime-gpu` (or `onnxruntime`)
- Node: `PB_WD14Adapter` → outputs `{tags: {label: score}}` and `tags_text`

**Florence-2 Adapter (Transformers)**
- Install: `pip install torch transformers pillow`
- First run will download `microsoft/Florence-2-base` (configurable)
- Node: `PB_Florence2Adapter` → outputs caption text (use `<CAPTION>` as task prompt)

**EMA Ranker**
- Node: `PB_EMARanker` → maintains per-tag exponential moving averages in `promptbrain_ema.db`
- Use output `ranked_tags` to guide `PB_PromptSuggester` or your own prompt composer

> Tip: You can still use the native ComfyUI nodes (ComfyUI-WD14-Tagger, ComfyUI-Florence2) and skip these adapters. These are provided when you prefer a pure-Python path or API workflows.

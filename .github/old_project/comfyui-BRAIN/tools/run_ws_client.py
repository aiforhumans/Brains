"""Minimal WebSocket runner for ComfyUI API prompts.
Requires: pip install websockets
Docs:
- Hosting / WebSocket usage: https://9elements.com/blog/hosting-a-comfyui-workflow-via-api/
- API format vs workflow JSON: https://github.com/comfyanonymous/ComfyUI/issues/1112
"""
import asyncio
import json
import uuid
import pathlib
import websockets

COMFY_WS = "ws://127.0.0.1:8188/ws"
COMFY_HTTP = "http://127.0.0.1:8188"

async def run_prompt(prompt_path: str):
    prompt = json.loads(pathlib.Path(prompt_path).read_text(encoding="utf-8"))
    client_id = prompt.get("client_id") or str(uuid.uuid4())
    prompt["client_id"] = client_id

    async with websockets.connect(COMFY_WS) as ws:
        # Start listening for progress in background
        async def recv_loop():
            try:
                async for msg in ws:
                    data = json.loads(msg)
                    if data.get("type") == "progress":
                        p = data.get("data",{})
                        print(f"[progress] {p.get('value')}/{p.get('max')}")
                    elif data.get("type") == "executed":
                        print("[executed]", data.get("data",{}).get("node"))
                    elif data.get("type") == "execution_error":
                        print("[error]", data)
            except Exception as e:
                print("[recv error]", e)

        recv_task = asyncio.create_task(recv_loop())

        # Queue the prompt
        await ws.send(json.dumps({"prompt": prompt["prompt"], "client_id": client_id}))
        await asyncio.sleep(0.1)

        # Wait a bit for completion (simple demo)
        await asyncio.sleep(5.0)
        recv_task.cancel()

if __name__ == "__main__":
    import sys, asyncio
    asyncio.run(run_prompt(sys.argv[1] if len(sys.argv) > 1 else "../workflows/demo_api.prompt.json"))

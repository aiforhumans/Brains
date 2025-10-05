"""
Brains-XDEV WebSocket Client for ComfyUI API

Minimal WebSocket runner for ComfyUI API prompts.
Useful for testing Brains-XDEV nodes programmatically.

Migrated from BRAIN project with improvements.

Requirements: pip install websockets

Usage:
    python tools/run_ws_client.py workflows/demo.prompt.json

Docs:
- Hosting / WebSocket usage: https://9elements.com/blog/hosting-a-comfyui-workflow-via-api/
- API format vs workflow JSON: https://github.com/comfyanonymous/ComfyUI/issues/1112
"""
import asyncio
import json
import uuid
import pathlib
import sys
import time

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    websockets = None
    WEBSOCKETS_AVAILABLE = False

# Default ComfyUI endpoints
COMFY_WS = "ws://127.0.0.1:8188/ws"
COMFY_HTTP = "http://127.0.0.1:8188"

async def run_prompt(prompt_path: str, verbose: bool = True):
    """
    Run a ComfyUI API prompt and monitor its execution.
    
    Args:
        prompt_path: Path to .prompt.json file
        verbose: Print detailed progress messages
    """
    if not WEBSOCKETS_AVAILABLE:
        print("Error: websockets not installed. Install with: pip install websockets")
        return False
    
    # Load and validate prompt
    try:
        prompt_file = pathlib.Path(prompt_path)
        if not prompt_file.exists():
            print(f"Error: Prompt file not found: {prompt_path}")
            return False
            
        prompt = json.loads(prompt_file.read_text(encoding="utf-8"))
        
        if "prompt" not in prompt:
            print(f"Error: Invalid prompt format. Expected 'prompt' key in {prompt_path}")
            return False
            
    except Exception as e:
        print(f"Error loading prompt file {prompt_path}: {e}")
        return False
    
    # Set up client ID
    client_id = prompt.get("client_id") or str(uuid.uuid4())
    prompt["client_id"] = client_id
    
    if verbose:
        print(f"[Brains-XDEV] Running prompt: {prompt_path}")
        print(f"[Brains-XDEV] Client ID: {client_id}")
    
    try:
        async with websockets.connect(COMFY_WS) as ws:
            # Listen for messages
            execution_complete = False
            execution_error = False
            
            async def recv_loop():
                nonlocal execution_complete, execution_error
                try:
                    async for msg in ws:
                        data = json.loads(msg)
                        msg_type = data.get("type")
                        
                        if msg_type == "progress":
                            p = data.get("data", {})
                            if verbose:
                                print(f"[progress] {p.get('value', 0)}/{p.get('max', 0)}")
                                
                        elif msg_type == "executed":
                            node_id = data.get("data", {}).get("node")
                            if verbose:
                                print(f"[executed] Node {node_id}")
                                
                        elif msg_type == "execution_start":
                            if verbose:
                                print("[execution_start]")
                                
                        elif msg_type == "execution_cached":
                            if verbose:
                                print("[execution_cached]")
                                
                        elif msg_type == "executing":
                            node_id = data.get("data", {}).get("node")
                            if node_id is None:
                                execution_complete = True
                                if verbose:
                                    print("[execution_complete]")
                            elif verbose:
                                print(f"[executing] Node {node_id}")
                                
                        elif msg_type == "execution_error":
                            execution_error = True
                            error_data = data.get("data", {})
                            print(f"[execution_error] {error_data}")
                            
                        elif msg_type == "status":
                            status = data.get("data", {})
                            if verbose and "queue_remaining" in status:
                                print(f"[status] Queue remaining: {status['queue_remaining']}")
                                
                except websockets.exceptions.ConnectionClosed:
                    print("[connection_closed]")
                except Exception as e:
                    print(f"[recv_error] {e}")

            # Start receiving messages
            recv_task = asyncio.create_task(recv_loop())

            # Send the prompt
            queue_message = {"prompt": prompt["prompt"], "client_id": client_id}
            await ws.send(json.dumps(queue_message))
            
            if verbose:
                print("[prompt_sent] Waiting for execution...")
            
            # Wait for completion or timeout
            timeout = 60  # 60 seconds timeout
            start_time = time.time()
            
            while not execution_complete and not execution_error:
                if time.time() - start_time > timeout:
                    print(f"[timeout] Execution timed out after {timeout} seconds")
                    break
                await asyncio.sleep(0.1)
            
            recv_task.cancel()
            
            if execution_error:
                print("[result] Execution failed with errors")
                return False
            elif execution_complete:
                if verbose:
                    print("[result] Execution completed successfully")
                return True
            else:
                print("[result] Execution status unknown (timeout)")
                return False
                
    except Exception as e:
        print(f"[connection_error] {e}")
        return False

def main():
    """Main entry point for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python run_ws_client.py <prompt_file.json> [--quiet]")
        print("Example: python run_ws_client.py ../workflows/demo.prompt.json")
        sys.exit(1)
    
    prompt_path = sys.argv[1]
    verbose = "--quiet" not in sys.argv
    
    # Run the prompt
    try:
        success = asyncio.run(run_prompt(prompt_path, verbose))
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[interrupted] Execution cancelled by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
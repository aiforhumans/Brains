#!/usr/bin/env python3
"""
ComfyUI Memory Cleanup Utility
Comprehensive memory cleaning for ComfyUI and associated processes
"""

import gc
import os
import sys
import psutil
import time
from pathlib import Path

def format_bytes(bytes_value):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"

def get_memory_info():
    """Get current memory usage information"""
    process = psutil.Process()
    memory_info = process.memory_info()
    return {
        'rss': memory_info.rss,  # Resident Set Size
        'vms': memory_info.vms,  # Virtual Memory Size
        'percent': process.memory_percent()
    }

def cleanup_python_memory():
    """Clean up Python memory"""
    print("ðŸ§¹ Cleaning Python memory...")
    
    # Get initial memory
    initial_memory = get_memory_info()
    print(f"   Initial memory: {format_bytes(initial_memory['rss'])} ({initial_memory['percent']:.1f}%)")
    
    # Force garbage collection multiple times
    collected_objects = 0
    for i in range(3):
        collected = gc.collect()
        collected_objects += collected
        time.sleep(0.1)  # Small delay between collections
    
    # Final memory check
    final_memory = get_memory_info()
    memory_freed = initial_memory['rss'] - final_memory['rss']
    
    print(f"   Collected {collected_objects} objects")
    print(f"   Final memory: {format_bytes(final_memory['rss'])} ({final_memory['percent']:.1f}%)")
    if memory_freed > 0:
        print(f"   Memory freed: {format_bytes(memory_freed)}")
    print("   âœ… Python memory cleanup complete")

def cleanup_torch_memory():
    """Clean up PyTorch/CUDA memory if available"""
    try:
        import torch
        print("ðŸ”¥ Cleaning PyTorch memory...")
        
        if torch.cuda.is_available():
            # Get CUDA memory info before cleanup
            device_count = torch.cuda.device_count()
            print(f"   Found {device_count} CUDA device(s)")
            
            for i in range(device_count):
                memory_allocated = torch.cuda.memory_allocated(i)
                memory_cached = torch.cuda.memory_reserved(i)
                print(f"   GPU {i} - Allocated: {format_bytes(memory_allocated)}, Cached: {format_bytes(memory_cached)}")
            
            # Clear CUDA cache
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            
            print("   âœ… CUDA memory cache cleared")
        else:
            print("   â„¹ï¸  CUDA not available, skipping GPU memory cleanup")
            
    except ImportError:
        print("   â„¹ï¸  PyTorch not available, skipping torch memory cleanup")

def cleanup_comfyui_cache():
    """Clean ComfyUI specific caches"""
    print("ðŸ“ Cleaning ComfyUI caches...")
    
    # Common ComfyUI cache directories
    comfy_base = Path(__file__).parent.parent.parent
    cache_dirs = [
        comfy_base / "temp",
        comfy_base / "output" / ".thumbnails",
        comfy_base / "web" / "cache",
        comfy_base / "models" / ".cache",
    ]
    
    total_freed = 0
    files_removed = 0
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            try:
                for file_path in cache_dir.rglob("*"):
                    if file_path.is_file():
                        try:
                            file_size = file_path.stat().st_size
                            file_path.unlink()
                            total_freed += file_size
                            files_removed += 1
                        except (OSError, PermissionError):
                            continue  # Skip files we can't delete
            except (OSError, PermissionError):
                continue  # Skip directories we can't access
    
    if files_removed > 0:
        print(f"   Removed {files_removed} cache files ({format_bytes(total_freed)})")
    else:
        print("   No cache files to remove")
    
    print("   âœ… ComfyUI cache cleanup complete")

def cleanup_system_memory():
    """Clean system-level memory caches"""
    print("ðŸ’¾ System memory information...")
    
    # Get system memory info
    memory = psutil.virtual_memory()
    print(f"   Total RAM: {format_bytes(memory.total)}")
    print(f"   Available: {format_bytes(memory.available)} ({memory.percent:.1f}% used)")
    
    # On Windows, suggest system cleanup
    if sys.platform == "win32":
        print("   ðŸ’¡ For additional system cleanup, consider running:")
        print("      - Windows Disk Cleanup (cleanmgr)")
        print("      - Clear Windows temp files (%temp%)")

def main():
    """Main memory cleanup function"""
    print("ðŸš€ ComfyUI Memory Cleanup Utility")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        # 1. Clean Python memory
        cleanup_python_memory()
        print()
        
        # 2. Clean PyTorch/CUDA memory
        cleanup_torch_memory()
        print()
        
        # 3. Clean ComfyUI caches
        cleanup_comfyui_cache()
        print()
        
        # 4. Show system memory info
        cleanup_system_memory()
        print()
        
        # Final summary
        end_time = time.time()
        print(f"âœ¨ Memory cleanup completed in {end_time - start_time:.2f} seconds")
        print("\nðŸ’¡ Recommendations:")
        print("   - Restart ComfyUI for maximum memory recovery")
        print("   - Close unnecessary browser tabs")
        print("   - Use PromptBrainPerformance node to monitor memory usage")
        
    except Exception as e:
        print(f"âŒ Error during cleanup: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

"""
Quick test script to validate Brains-XDEV node imports
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("[Testing] Importing brightness example...")
    from brightness_example import BrainsXDEV_Brightness
    print("✓ Brightness node imported successfully")
    
    node = BrainsXDEV_Brightness()
    print(f"✓ Node instantiated: {node.NODE_NAME}")
    print(f"✓ Category: {node.CATEGORY}")
    
    # Test basic functionality
    import numpy as np
    img = np.zeros((8, 8, 3), dtype=np.float32) + 0.5
    result = node.run([img], strength=0.1)
    print(f"✓ Node execution successful, output shape: {result[0][0].shape}")
    
except Exception as e:
    print(f"✗ Error testing brightness node: {e}")

try:
    print("\n[Testing] Importing memory nodes...")
    from promptbrain.memory import BrainsXDEV_MemoryWrite, BrainsXDEV_MemoryRead
    print("✓ Memory nodes imported successfully")
    
    # Test memory write
    write_node = BrainsXDEV_MemoryWrite()
    tags_dict = {"tags": {"test": 0.9}}
    result = write_node.run(tags_dict, "test caption", 0.8, "test")
    print(f"✓ Memory write test: {result[0]}")
    
    # Test memory read
    read_node = BrainsXDEV_MemoryRead()
    captions, raw = read_node.run(5, 0.0)
    print(f"✓ Memory read test: found {len(captions)} captions")
    
except Exception as e:
    print(f"✗ Error testing memory nodes: {e}")

try:
    print("\n[Testing] Importing stub nodes...")
    from promptbrain.tagger import BrainsXDEV_Tagger
    from promptbrain.captioner import BrainsXDEV_Captioner
    from promptbrain.scorer import BrainsXDEV_Scorer
    print("✓ Stub nodes imported successfully")
    
except Exception as e:
    print(f"✗ Error testing stub nodes: {e}")

print("\n[Testing] Complete!")
"""
Quick test script to verify beginner nodes can be imported
Run from ComfyUI's embedded Python to test imports
"""
import sys
import os

# Add ComfyUI to path
comfy_path = r"C:\comfy\ComfyUI_windows_portable\ComfyUI"
if comfy_path not in sys.path:
    sys.path.insert(0, comfy_path)

# Add custom nodes path
custom_nodes_path = r"C:\comfy\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui-Brains\src"
if custom_nodes_path not in sys.path:
    sys.path.insert(0, custom_nodes_path)

print("=" * 60)
print("BEGINNER NODES IMPORT TEST")
print("=" * 60)

# Test imports
test_results = []

def test_import(name, import_path):
    """Test a single import"""
    try:
        exec(import_path)
        print(f"✅ {name}: SUCCESS")
        return True
    except Exception as e:
        print(f"❌ {name}: FAILED - {e}")
        return False

# Test each node
tests = [
    ("Smart Memory Loader", "from smart_memory_loader import BrainsXDEV_SmartMemoryLoader"),
    ("Smart Prompt Helper", "from smart_prompt_helper import BrainsXDEV_SmartPromptHelper"),
    ("Memory Teacher", "from memory_teacher import BrainsXDEV_MemoryTeacher"),
    ("Auto Quality Rater", "from auto_quality_rater import BrainsXDEV_AutoQualityRater"),
    ("Memory Stats Dashboard", "from memory_stats_dashboard import BrainsXDEV_MemoryStatsDashboard"),
]

print("\n📦 Testing Node Imports:\n")
for name, import_path in tests:
    result = test_import(name, import_path)
    test_results.append(result)

print("\n" + "=" * 60)
print(f"RESULTS: {sum(test_results)}/{len(test_results)} nodes imported successfully")
print("=" * 60)

if all(test_results):
    print("\n🎉 All beginner nodes are ready to use!")
    print("\nNext steps:")
    print("1. Start ComfyUI")
    print("2. Look for nodes under 'Brains-XDEV/Beginner' category")
    print("3. Load workflow: workflows/beginner_nodes_test.workflow.json")
else:
    print("\n⚠️ Some nodes failed to import. Check error messages above.")

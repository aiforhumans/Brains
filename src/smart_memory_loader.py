"""
Smart Memory Loader — Beginner-friendly interface for loading/creating BRAIN memory.

This node provides an intuitive interface for users to load or create AI memory databases.
It wraps the advanced BrainsXDEV_PromptBrainSource functionality with simpler parameters.
"""
from typing import Any, Dict, Tuple
import os

# Import the advanced BRAIN source node
try:
    from .brain_datatype import BrainData, BrainsXDEV_PromptBrainSource
    BRAIN_AVAILABLE = True
except ImportError:
    BRAIN_AVAILABLE = False
    BrainData = None


class BrainsXDEV_SmartMemoryLoader:
    """
    Smart Memory Loader - Beginner-friendly BRAIN database loader.
    
    This node automatically discovers existing brain files, creates fresh databases,
    and makes backups to prevent data loss. Perfect for users new to the BRAIN system.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "database_path": ("STRING", {
                    "default": "promptbrain.db",
                    "multiline": False,
                }),
                "auto_discover": ("BOOLEAN", {
                    "default": True,
                }),
                "create_backup": ("BOOLEAN", {
                    "default": True,
                }),
            },
        }
    
    RETURN_TYPES = ("BRAIN",)
    RETURN_NAMES = ("smart_memory",)
    FUNCTION = "load_memory"
    CATEGORY = "Brains-XDEV/Beginner"
    NODE_NAME = "SmartMemoryLoader"
    
    def load_memory(
        self,
        database_path: str,
        auto_discover: bool,
        create_backup: bool,
    ) -> Tuple[Any]:
        """
        Load or create a BRAIN memory database.
        
        Args:
            database_path: Path to database file (or "auto" for discovery)
            auto_discover: Automatically find existing databases
            create_backup: Create backup before loading
            
        Returns:
            Tuple containing BrainData object
        """
        if not BRAIN_AVAILABLE:
            print("[Brains-XDEV] ❌ BRAIN system not available. Please check installation.")
            return (None,)
        
        try:
            # If auto_discover is enabled and path is default, search for existing
            if auto_discover and database_path == "promptbrain.db":
                discovered = self._discover_brains()
                if discovered:
                    database_path = discovered[0]
                    print(f"[Brains-XDEV] 🔍 Auto-discovered: {database_path}")
            
            # Use the advanced PromptBrainSource node
            source_node = BrainsXDEV_PromptBrainSource()
            
            # Call with backup settings
            brain_data_tuple = source_node.create_brain(
                brain_source=database_path,
                refresh_list=False,
                backup_on_load=create_backup,
            )
            
            # Extract brain_data from tuple
            brain_data = brain_data_tuple[0] if isinstance(brain_data_tuple, tuple) else brain_data_tuple
            
            print(f"[Brains-XDEV] ✅ Smart Memory loaded successfully!")
            print(f"[Brains-XDEV] 📁 Database: {database_path}")
            
            return (brain_data,)
            
        except Exception as e:
            print(f"[Brains-XDEV] ❌ Error loading Smart Memory: {e}")
            import traceback
            traceback.print_exc()
            return (None,)
    
    def _discover_brains(self):
        """Discover existing BRAIN database files."""
        search_paths = [
            ".",
            "custom_nodes/comfyui-Brains",
            "custom_nodes/Brains",
            "..",
        ]
        
        found = []
        for path in search_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith(".db") and "brain" in file.lower():
                        found.append(os.path.join(path, file))
        
        return found


# Export for registration
__all__ = ["BrainsXDEV_SmartMemoryLoader"]

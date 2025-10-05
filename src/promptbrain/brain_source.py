#!/usr/bin/env python3
"""
Brains-XDEV PromptBrain Source Node

Creates or loads BRAIN data with auto-discovery of available brain files.
Imported from Comfyui-DEV and adapted for Brains-XDEV architecture.

References:
- ComfyUI Custom Datatypes: https://docs.comfy.org/custom-nodes/backend/custom_datatypes
- PromptBrain Architecture: https://github.com/aiforhumans/Brains
"""

print("[Brains-XDEV] brain_source import")

from typing import Any, Dict, Tuple
import json
import time
from pathlib import Path
import shutil

from .brain_data import BrainData


class BrainsXDEV_PromptBrainSource:
    """
    Source node that creates or loads BRAIN data with auto-discovery.
    Automatically finds and lists available brain files in common locations.
    """
    
    @classmethod
    def get_available_brains(cls):
        """Discover available brain files in common locations."""
        brain_files = []
        
        # Search locations for brain files
        search_paths = [
            Path("."),  # Current directory
            Path("../../../user"),  # ComfyUI user directory
            Path("c:/comfy/ComfyUI_windows_portable/ComfyUI/user"),  # Windows standard
            Path("user"),  # Relative user directory
            Path("models/brain"),  # Models subdirectory
            Path("../../../models/brain"),  # ComfyUI models/brain
        ]
        
        for search_path in search_paths:
            try:
                if search_path.exists() and search_path.is_dir():
                    # Look for .json files that might be brain files
                    for file_path in search_path.glob("*.json"):
                        if file_path.is_file():
                            # Check if it looks like a brain file
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                    
                                # Check for direct BRAIN format
                                is_brain_format = (isinstance(data, dict) and 
                                                 all(key in data for key in ['tags', 'history']) and
                                                 'co' in data)
                                
                                # Check for exported brain format (wrapped with export_info)
                                is_export_format = (isinstance(data, dict) and 
                                                  'export_info' in data and 
                                                  'tags' in data and 'history' in data)
                                
                                if is_brain_format or is_export_format:
                                    relative_name = f"{search_path.name}/{file_path.name}" if search_path.name != "." else file_path.name
                                    brain_files.append((relative_name, str(file_path.absolute())))
                            except:
                                continue
            except:
                continue
        
        # Add special options
        if not brain_files:
            return ["<create_new>", "<auto_find>"]
        else:
            return ["<create_new>", "<auto_find>"] + [name for name, _ in brain_files]
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        available_brains = cls.get_available_brains()
        
        return {
            "required": {
                "brain_source": (available_brains, {
                    "default": available_brains[1] if len(available_brains) > 1 else available_brains[0],
                    "tooltip": "Select brain file to load or create new"
                })
            },
            "optional": {
                "refresh_list": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Refresh the list of available brain files"
                }),
                "backup_on_load": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Create backup when loading existing brain"
                })
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            }
        }
    
    RETURN_TYPES = ("BRAIN",)
    RETURN_NAMES = ("brain_data",)
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_PromptBrainSource"
    DESCRIPTION = "Create or load BRAIN data with auto-discovery of available brain files"
    
    def load_brain_file(self, file_path: Path) -> BrainData:
        """Load brain file and convert from export format if needed."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if this is an exported format that needs conversion
        if 'export_info' in data:
            print(f"ðŸ”„ Converting exported brain format...")
            converted_data = self.convert_export_to_brain_format(data)
            return BrainData.from_dict(converted_data)
        else:
            # Standard BRAIN format
            return BrainData.from_dict(data)
    
    def convert_export_to_brain_format(self, export_data: Dict) -> Dict:
        """Convert exported brain format to standard BRAIN format."""
        converted = {
            "tags": {},
            "co": export_data.get("co", {}),
            "history": export_data.get("history", []),
            "styles": export_data.get("styles", {}),
            "features": export_data.get("features", {}),
            "tag_styles": export_data.get("tag_styles", {}),
            "metadata": {
                "created": time.time(),
                "version": "2.1",
                "node_count": 0,
                "converted_from_export": True,
                "original_export_info": export_data.get("export_info", {})
            }
        }
        
        # Convert tags from export format (pos/neg) to BRAIN format (score)
        export_tags = export_data.get("tags", {})
        for tag, tag_data in export_tags.items():
            if isinstance(tag_data, dict):
                # Convert pos/neg to score
                pos = tag_data.get("pos", 0.0)
                neg = tag_data.get("neg", 0.0)
                total = pos + neg
                score = pos / total if total > 0 else 0.5
                
                converted["tags"][tag] = {
                    "count": tag_data.get("count", 1),
                    "score": score,
                    "last": tag_data.get("last", time.time())
                }
        
        return converted
    
    def run(
        self,
        brain_source: str = "<create_new>",
        refresh_list: bool = False,
        backup_on_load: bool = True,
        prompt=None,
        extra_pnginfo=None,
        unique_id=None
    ) -> Tuple[BrainData]:
        """
        Create or load brain data with auto-discovery.
        
        Args:
            brain_source: Brain file to load or special option
            refresh_list: Refresh the list of available brain files
            backup_on_load: Create backup when loading existing brain
            prompt: Hidden input - current workflow prompt
            extra_pnginfo: Hidden input - PNG metadata
            unique_id: Hidden input - node unique identifier
            
        Returns:
            Tuple containing BrainData instance
        """
        # Handle refresh list
        if refresh_list:
            print("ðŸ”„ Refreshing brain file list...")
        
        # Handle create new
        if brain_source == "<create_new>":
            brain = BrainData()
            brain.add_node_to_chain("PromptBrainSource")
            print("ðŸ§  Created new brain data")
            return (brain,)
        
        # Handle auto find
        elif brain_source == "<auto_find>":
            return self._auto_find_brain(backup_on_load)
        
        # Handle specific file selection
        else:
            return self._load_specific_brain(brain_source, backup_on_load)
    
    def _auto_find_brain(self, backup_on_load: bool) -> Tuple[BrainData]:
        """Auto-find brain file in standard locations."""
        try:
            # Look for brain file in standard locations (including exported files)
            possible_paths = [
                Path("prompt_brain.json"),
                Path("../../../user/prompt_brain.json"),
                Path("c:/comfy/ComfyUI_windows_portable/ComfyUI/user/prompt_brain.json"),
                Path("user/prompt_brain.json"),
                # Also check for exported files
                Path("prompt_brain_export.json"),
                Path("../../../user/prompt_brain_export.json"),
                Path("c:/comfy/ComfyUI_windows_portable/ComfyUI/user/prompt_brain_export.json"),
                Path("user/prompt_brain_export.json")
            ]
            
            for brain_path in possible_paths:
                if brain_path.exists():
                    print(f"ðŸ§  Auto-found brain file: {brain_path}")
                    
                    # Create backup if requested
                    if backup_on_load:
                        backup_path = brain_path.with_suffix(f".backup_{int(time.time())}.json")
                        shutil.copy2(brain_path, backup_path)
                        print(f"ðŸ’¾ Created backup: {backup_path.name}")
                    
                    # Load the brain file (with format conversion if needed)
                    brain = self.load_brain_file(brain_path)
                    brain.add_node_to_chain("PromptBrainSource")
                    
                    # Get stats for display
                    stats = brain.get_performance_stats()
                    print(f"ðŸ“Š Loaded brain: {stats['total_tags']} tags, {stats['total_history']} events")
                    
                    return (brain,)
            
            # If no file found, create new
            print("âš ï¸ No brain files found, creating new")
            brain = BrainData()
            brain.add_node_to_chain("PromptBrainSource")
            return (brain,)
            
        except Exception as e:
            print(f"âŒ Error auto-finding brain file: {e}")
            brain = BrainData()
            brain.add_node_to_chain("PromptBrainSource")
            return (brain,)
    
    def _load_specific_brain(self, brain_source: str, backup_on_load: bool) -> Tuple[BrainData]:
        """Load a specific brain file by name."""
        try:
            # Re-discover files to find the selected one
            brain_files = self._discover_brain_files()
            
            # Find matching file
            selected_path = None
            for name, path in brain_files:
                if name == brain_source:
                    selected_path = Path(path)
                    break
            
            if selected_path and selected_path.exists():
                print(f"ðŸ§  Loading selected brain: {brain_source}")
                
                # Create backup if requested
                if backup_on_load:
                    backup_path = selected_path.with_suffix(f".backup_{int(time.time())}.json")
                    shutil.copy2(selected_path, backup_path)
                    print(f"ðŸ’¾ Created backup: {backup_path.name}")
                
                # Load the brain file (with format conversion if needed)
                brain = self.load_brain_file(selected_path)
                brain.add_node_to_chain("PromptBrainSource")
                
                # Get stats for display
                stats = brain.get_performance_stats()
                print(f"ðŸ“Š Loaded brain: {stats['total_tags']} tags, {stats['total_history']} events, avg score: {stats['average_score']:.2f}")
                
                return (brain,)
            else:
                print(f"âš ï¸ Selected brain file not found: {brain_source}")
                brain = BrainData()
                brain.add_node_to_chain("PromptBrainSource")
                return (brain,)
                
        except Exception as e:
            print(f"âŒ Error loading selected brain: {e}")
            brain = BrainData()
            brain.add_node_to_chain("PromptBrainSource")
            return (brain,)
    
    def _discover_brain_files(self):
        """Internal helper to discover brain files."""
        brain_files = []
        search_paths = [
            Path("."),
            Path("../../../user"),
            Path("c:/comfy/ComfyUI_windows_portable/ComfyUI/user"),
            Path("user"),
            Path("models/brain"),
            Path("../../../models/brain"),
        ]
        
        for search_path in search_paths:
            try:
                if search_path.exists() and search_path.is_dir():
                    for file_path in search_path.glob("*.json"):
                        if file_path.is_file():
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                    
                                is_brain_format = (isinstance(data, dict) and 
                                                 all(key in data for key in ['tags', 'history']) and
                                                 'co' in data)
                                
                                is_export_format = (isinstance(data, dict) and 
                                                  'export_info' in data and 
                                                  'tags' in data and 'history' in data)
                                
                                if is_brain_format or is_export_format:
                                    relative_name = f"{search_path.name}/{file_path.name}" if search_path.name != "." else file_path.name
                                    brain_files.append((relative_name, str(file_path.absolute())))
                            except:
                                continue
            except:
                continue
        
        return brain_files

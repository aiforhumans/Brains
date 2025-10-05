#!/usr/bin/env python3
"""
Brains-XDEV PromptBrain Custom DataType Implementation

Creates a BRAIN datatype for seamless data flow between PromptBrain nodes.
Imported from Comfyui-DEV and adapted for Brains-XDEV architecture.

Original functionality preserved with Brains-XDEV naming conventions.
"""

import json
import time
from typing import Dict, Any, Optional, List, Tuple

class BrainData:
    """
    Custom BRAIN datatype for PromptBrain system
    Allows direct data passing between nodes without file I/O
    """
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """Initialize brain data structure"""
        if data is None:
            self.data = {
                "tags": {},
                "co": {},
                "history": [],
                "styles": {},
                "features": {},
                "tag_styles": {},
                "metadata": {
                    "created": time.time(),
                    "version": "2.1",
                    "node_count": 0
                }
            }
        else:
            self.data = data
            # Ensure metadata exists even in loaded data
            if "metadata" not in self.data:
                self.data["metadata"] = {
                    "created": time.time(),
                    "version": "2.1",
                    "node_count": 0
                }
            # Ensure all required metadata fields exist
            metadata = self.data["metadata"]
            if "node_count" not in metadata:
                metadata["node_count"] = 0
            if "version" not in metadata:
                metadata["version"] = "2.1"
            if "created" not in metadata:
                metadata["created"] = time.time()
        
        # Add runtime metadata
        self._last_modified = time.time()
        self._node_chain = []
        self._performance_cache = {}
    
    def get_tags(self) -> Dict[str, Dict[str, Any]]:
        """Get all tag data"""
        return self.data.get("tags", {})
    
    def get_cooccurrence(self) -> Dict[str, int]:
        """Get co-occurrence data"""
        return self.data.get("co", {})
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get learning history"""
        return self.data.get("history", [])
    
    def get_styles(self) -> Dict[str, Any]:
        """Get style definitions"""
        return self.data.get("styles", {})
    
    def get_features(self) -> Dict[str, Any]:
        """Get feature definitions"""
        return self.data.get("features", {})
    
    def _ensure_metadata_exists(self) -> None:
        """Ensure metadata structure exists and is complete"""
        if "metadata" not in self.data:
            self.data["metadata"] = {
                "created": time.time(),
                "version": "2.1",
                "node_count": 0
            }
        else:
            metadata = self.data["metadata"]
            if "node_count" not in metadata:
                metadata["node_count"] = 0
            if "version" not in metadata:
                metadata["version"] = "2.1"
            if "created" not in metadata:
                metadata["created"] = time.time()
    
    def add_learning_event(self, prompt: str, score: float, tags: List[str], 
                          style_category: str = "none", feature_emphasis: str = "none") -> None:
        """Add a learning event to the brain"""
        # Update tags
        for tag in tags:
            if tag not in self.data["tags"]:
                self.data["tags"][tag] = {
                    "count": 0,
                    "score": 0.0,
                    "last": 0
                }
            
            tag_data = self.data["tags"][tag]
            
            # Ensure score field exists (backwards compatibility)
            if "score" not in tag_data:
                tag_data["score"] = 0.0
            if "count" not in tag_data:
                tag_data["count"] = 0
            
            tag_data["count"] += 1
            tag_data["score"] = (tag_data["score"] * (tag_data["count"] - 1) + score) / tag_data["count"]
            tag_data["last"] = time.time()
        
        # Update co-occurrence
        for i, tag1 in enumerate(tags):
            for j, tag2 in enumerate(tags):
                if i != j:
                    pair_key = f"{tag1}|{tag2}"
                    self.data["co"][pair_key] = self.data["co"].get(pair_key, 0) + 1
        
        # Add to history
        self.data["history"].append({
            "prompt": prompt,
            "score": score,
            "tags": tags,
            "style": style_category,
            "feature": feature_emphasis,
            "timestamp": time.time()
        })
        
        # Update metadata
        self._last_modified = time.time()
        self._ensure_metadata_exists()
        self.data["metadata"]["node_count"] += 1
    
    def get_suggestions(self, base_tags: List[str], style: str = "none", 
                       feature: str = "none", quality_threshold: float = 0.3) -> List[str]:
        """Get tag suggestions based on current brain data"""
        suggestions = []
        
        # Find related tags through co-occurrence
        for base_tag in base_tags:
            for pair_key, count in self.data["co"].items():
                if "|" in pair_key:
                    tag1, tag2 = pair_key.split("|", 1)
                    if tag1 == base_tag and tag2 not in base_tags:
                        tag_score = self.data["tags"].get(tag2, {}).get("score", 0.0)
                        if tag_score >= quality_threshold:
                            suggestions.append((tag2, tag_score, count))
        
        # Sort by score and co-occurrence count
        suggestions.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        # Return top suggestions
        return [tag for tag, _, _ in suggestions[:20]]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            "total_tags": len(self.data["tags"]),
            "total_cooccurrence": len(self.data["co"]),
            "total_history": len(self.data["history"]),
            "last_modified": self._last_modified,
            "node_chain": self._node_chain.copy(),
            "average_score": self._calculate_average_score()
        }
    
    def _calculate_average_score(self) -> float:
        """Calculate average score across all tags"""
        tags = self.data["tags"]
        if not tags:
            return 0.0
        
        total_score = sum(tag_data.get("score", 0.0) for tag_data in tags.values())
        return total_score / len(tags)
    
    def add_node_to_chain(self, node_name: str) -> None:
        """Track which nodes have processed this brain data"""
        self._node_chain.append({
            "node": node_name,
            "timestamp": time.time()
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return self.data.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BrainData':
        """Create BrainData from dictionary"""
        return cls(data)
    
    def __str__(self) -> str:
        """String representation"""
        stats = self.get_performance_stats()
        return f"BrainData(tags={stats['total_tags']}, history={stats['total_history']}, avg_score={stats['average_score']:.2f})"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"BrainData({self.to_dict()})"


class BrainsXDEV_PromptBrainSource:
    """
    Source node that creates or loads BRAIN data with auto-discovery
    Automatically finds and lists available brain files
    """
    
    @classmethod
    def get_available_brains(cls):
        """Discover available brain files in common locations"""
        import os
        from pathlib import Path
        
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
                                                 'co' in data)  # co is optional for export format
                                
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
    def INPUT_TYPES(cls):
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
            }
        }
    
    RETURN_TYPES = ("BRAIN",)
    RETURN_NAMES = ("brain_data",)
    FUNCTION = "create_brain"
    CATEGORY = "Brains-XDEV/PromptBrain"
    DESCRIPTION = "Create or load BRAIN data with auto-discovery of available brain files"
    
    def load_brain_file(self, file_path):
        """Load brain file and convert from export format if needed"""
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
    
    def convert_export_to_brain_format(self, export_data):
        """Convert exported brain format to standard BRAIN format"""
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
    
    def create_brain(self, brain_source="<create_new>", refresh_list=False, backup_on_load=True):
        """Create or load brain data with auto-discovery"""
        import os
        from pathlib import Path
        import shutil
        import time
        
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
        
        # Handle specific file selection
        else:
            try:
                # Find the selected brain file by re-discovering files
                brain_files = []
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
                            for file_path in search_path.glob("*.json"):
                                if file_path.is_file():
                                    try:
                                        with open(file_path, 'r', encoding='utf-8') as f:
                                            data = json.load(f)
                                            
                                        # Check for direct BRAIN format
                                        is_brain_format = (isinstance(data, dict) and 
                                                         all(key in data for key in ['tags', 'history']) and
                                                         'co' in data)  # co is optional for export format
                                        
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


class BrainsXDEV_PromptBrainLearnDirect:
    """
    Enhanced PromptBrainLearn that works with BRAIN datatype
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "brain_data": ("BRAIN", {"forceInput": True}),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "The prompt to learn from"
                }),
                "score": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "Quality score (0.0=poor, 1.0=excellent)"
                }),
                "style_category": (["none", "photorealistic", "artistic", "anime", "fantasy", 
                                  "portrait", "landscape", "cinematic", "vintage", "modern", 
                                  "abstract", "minimalist"], {
                    "default": "none",
                    "tooltip": "Artistic style category"
                }),
                "feature_emphasis": (["none", "composition", "lighting", "color", "texture", 
                                    "mood", "character", "background", "clothing", "accessories"], {
                    "default": "none",
                    "tooltip": "Visual feature to emphasize"
                })
            },
            "optional": {
                "learning_rate": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "Learning intensity multiplier"
                })
            }
        }
    
    RETURN_TYPES = ("BRAIN", "STRING")
    RETURN_NAMES = ("brain_data", "status")
    FUNCTION = "learn_direct"
    CATEGORY = "Brains-XDEV/PromptBrain"
    DESCRIPTION = "Learn from prompt using BRAIN datatype"
    
    def learn_direct(self, brain_data: BrainData, prompt: str, score: float, 
                    style_category: str = "none", feature_emphasis: str = "none", 
                    learning_rate: float = 1.0):
        """Learn from prompt using direct brain data"""
        
        # Validate inputs
        if not (0.0 <= score <= 1.0):
            return (brain_data, "âŒ Score must be between 0.0 and 1.0")
        
        # Extract tags from prompt
        tags = self.extract_tags(prompt)
        
        if not tags:
            return (brain_data, "âŒ No valid tags found in prompt")
        
        # Apply learning rate
        adjusted_score = score * learning_rate
        
        # Add learning event to brain
        brain_data.add_learning_event(
            prompt=prompt,
            score=adjusted_score,
            tags=tags,
            style_category=style_category,
            feature_emphasis=feature_emphasis
        )
        
        # Track node processing
        brain_data.add_node_to_chain("PromptBrainLearnDirect")
        
        # Generate status message
        status = f"âœ… Learned from {len(tags)} tags with score {score:.1f}"
        if style_category != "none":
            status += f" (Style: {style_category})"
        if feature_emphasis != "none":
            status += f" (Feature: {feature_emphasis})"
        
        return (brain_data, status)
    
    def extract_tags(self, prompt: str) -> List[str]:
        """Extract tags from prompt"""
        import re
        
        # Clean and normalize
        cleaned = re.sub(r'[^\w\s,:-]', '', prompt.lower())
        
        # Split by commas and clean
        raw_tags = [tag.strip() for tag in cleaned.split(',')]
        
        # Filter valid tags
        valid_tags = []
        for tag in raw_tags:
            if tag and len(tag) > 1:
                valid_tags.append(tag)
        
        return valid_tags


class BrainsXDEV_PromptBrainSuggestDirect:
    """
    Enhanced PromptBrainSuggest that works with BRAIN datatype
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "brain_data": ("BRAIN", {"forceInput": True}),
                "base_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Starting prompt to enhance"
                }),
                "suggestion_count": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 10,
                    "tooltip": "Number of enhanced prompts to generate"
                }),
                "creativity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "Creativity level"
                })
            },
            "optional": {
                "target_style": (["none", "photorealistic", "artistic", "anime", "fantasy", 
                                "portrait", "landscape", "cinematic", "vintage", "modern", 
                                "abstract", "minimalist"], {
                    "default": "none",
                    "tooltip": "Target artistic style"
                }),
                "quality_threshold": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "Minimum quality score for suggestions"
                })
            }
        }
    
    RETURN_TYPES = ("BRAIN", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("brain_data", "suggestion_1", "suggestion_2", "suggestion_3")
    FUNCTION = "suggest_direct"
    CATEGORY = "Brains-XDEV/PromptBrain"
    DESCRIPTION = "Generate enhanced prompts using BRAIN datatype"
    
    def suggest_direct(self, brain_data: BrainData, base_prompt: str, suggestion_count: int = 3,
                      creativity: float = 1.0, target_style: str = "none", 
                      quality_threshold: float = 0.3):
        """Generate suggestions using direct brain data"""
        
        # Extract base tags
        base_tags = self.extract_tags(base_prompt)
        
        # Get suggestions from brain
        suggested_tags = brain_data.get_suggestions(
            base_tags=base_tags,
            style=target_style,
            quality_threshold=quality_threshold
        )
        
        # Generate enhanced prompts
        suggestions = []
        for i in range(min(suggestion_count, 3)):  # Limit to 3 outputs for now
            enhanced_prompt = self.build_enhanced_prompt(
                base_prompt, suggested_tags, creativity, i
            )
            suggestions.append(enhanced_prompt)
        
        # Pad to 3 suggestions
        while len(suggestions) < 3:
            suggestions.append(base_prompt)
        
        # Track node processing
        brain_data.add_node_to_chain("PromptBrainSuggestDirect")
        
        return (brain_data, suggestions[0], suggestions[1], suggestions[2])
    
    def extract_tags(self, prompt: str) -> List[str]:
        """Extract tags from prompt"""
        import re
        cleaned = re.sub(r'[^\w\s,:-]', '', prompt.lower())
        raw_tags = [tag.strip() for tag in cleaned.split(',')]
        return [tag for tag in raw_tags if tag and len(tag) > 1]
    
    def build_enhanced_prompt(self, base_prompt: str, suggested_tags: List[str], 
                            creativity: float, variation: int) -> str:
        """Build enhanced prompt with suggestions"""
        import random
        
        # Start with base prompt
        enhanced = base_prompt
        
        # Add suggested tags based on creativity and variation
        tags_to_add = []
        max_additions = max(1, int(creativity * 5))
        
        # Select tags with some randomness
        available_tags = suggested_tags.copy()
        random.seed(variation * 42)  # Deterministic but varied
        
        for _ in range(min(max_additions, len(available_tags))):
            if available_tags:
                if random.random() < creativity:
                    tag = available_tags.pop(0)
                    tags_to_add.append(tag)
                else:
                    # Skip this tag
                    if available_tags:
                        available_tags.pop(0)
        
        # Add tags to prompt
        if tags_to_add:
            if enhanced.strip():
                enhanced += ", " + ", ".join(tags_to_add)
            else:
                enhanced = ", ".join(tags_to_add)
        
        return enhanced


class BrainsXDEV_PromptBrainPerformanceDirect:
    """
    Enhanced PromptBrainPerformance that works with BRAIN datatype
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "brain_data": ("BRAIN", {"forceInput": True})
            },
            "optional": {
                "show_detailed_stats": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Show comprehensive performance analysis"
                })
            }
        }
    
    RETURN_TYPES = ("BRAIN", "STRING")
    RETURN_NAMES = ("brain_data", "performance_report")
    FUNCTION = "analyze_direct"
    CATEGORY = "Brains-XDEV/PromptBrain"
    DESCRIPTION = "Analyze performance using BRAIN datatype"
    
    def analyze_direct(self, brain_data: BrainData, show_detailed_stats: bool = True):
        """Analyze brain performance using direct data"""
        
        # Get performance statistics
        stats = brain_data.get_performance_stats()
        
        # Generate report
        if show_detailed_stats:
            report = self.generate_detailed_report(stats, brain_data)
        else:
            report = self.generate_basic_report(stats)
        
        # Track node processing
        brain_data.add_node_to_chain("PromptBrainPerformanceDirect")
        
        return (brain_data, report)
    
    def generate_detailed_report(self, stats: Dict[str, Any], brain_data: BrainData) -> str:
        """Generate detailed performance report"""
        report = "ðŸ§  BRAIN DATATYPE PERFORMANCE REPORT\n"
        report += "=" * 50 + "\n\n"
        
        report += f"ðŸ“Š Dataset Overview:\n"
        report += f"   â€¢ Total Tags: {stats['total_tags']:,}\n"
        report += f"   â€¢ Co-occurrence Pairs: {stats['total_cooccurrence']:,}\n"
        report += f"   â€¢ Learning History: {stats['total_history']:,} events\n"
        report += f"   â€¢ Average Score: {stats['average_score']:.3f}\n\n"
        
        report += f"ðŸ”„ Node Processing Chain:\n"
        for i, node_event in enumerate(stats['node_chain'][-5:], 1):  # Last 5 nodes
            report += f"   {i}. {node_event['node']}\n"
        
        report += f"\nâš¡ Performance Status:\n"
        if stats['total_tags'] < 100:
            report += "   ðŸŸ¢ Small dataset - Excellent performance\n"
        elif stats['total_tags'] < 500:
            report += "   ðŸŸ¡ Medium dataset - Good performance\n"
        else:
            report += "   ðŸŸ  Large dataset - Consider optimization\n"
        
        report += f"\nðŸ’¡ BRAIN Datatype Benefits:\n"
        report += "   â€¢ No file I/O between nodes\n"
        report += "   â€¢ Direct memory data passing\n"
        report += "   â€¢ Real-time node chain tracking\n"
        report += "   â€¢ Instant performance feedback\n"
        
        return report
    
    def generate_basic_report(self, stats: Dict[str, Any]) -> str:
        """Generate basic performance report"""
        return f"ðŸ§  Brain: {stats['total_tags']} tags, {stats['total_history']} events, avg score: {stats['average_score']:.2f}"


class BrainsXDEV_PromptBrainResetDirect:
    """
    Reset BRAIN datatype with options for backup and selective clearing
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "brain_data": ("BRAIN", {"forceInput": True}),
                "reset_type": (["complete", "preserve_styles", "preserve_history"], {
                    "default": "complete",
                    "tooltip": "Type of reset to perform"
                })
            },
            "optional": {
                "create_backup": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Create backup before reset"
                }),
                "confirmation": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Confirm reset operation (safety check)"
                })
            }
        }
    
    RETURN_TYPES = ("BRAIN", "STRING")
    RETURN_NAMES = ("brain_data", "reset_status")
    FUNCTION = "reset_direct"
    CATEGORY = "Brains-XDEV/PromptBrain"
    DESCRIPTION = "Reset BRAIN datatype with backup and selective options"
    
    def reset_direct(self, brain_data: BrainData, reset_type: str = "complete", 
                    create_backup: bool = True, confirmation: bool = False):
        """Reset brain data with backup and selective options"""
        
        # Safety check - require confirmation for destructive operations
        if not confirmation:
            return (brain_data, "âŒ Reset cancelled - confirmation required for safety")
        
        # Create backup if requested
        backup_info = ""
        if create_backup:
            try:
                import json
                import time
                from pathlib import Path
                
                # Create timestamped backup
                timestamp = int(time.time())
                backup_filename = f"prompt_brain_backup_{timestamp}.json"
                
                # Try to save in user directory first
                backup_paths = [
                    Path("c:/comfy/ComfyUI_windows_portable/ComfyUI/user") / backup_filename,
                    Path("../../../user") / backup_filename,
                    Path("user") / backup_filename,
                    Path(".") / backup_filename
                ]
                
                saved = False
                for backup_path in backup_paths:
                    try:
                        backup_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            # Export current brain data
                            export_data = {
                                "export_info": {
                                    "timestamp": timestamp,
                                    "version": "2.1",
                                    "source": "PromptBrainResetDirect",
                                    "reset_type_requested": reset_type
                                },
                                "tags": brain_data.get_tags(),
                                "co": brain_data.get_cooccurrence(),
                                "history": brain_data.get_history(),
                                "styles": brain_data.get_styles(),
                                "features": brain_data.get_features(),
                                "metadata": brain_data.data.get("metadata", {})
                            }
                            json.dump(export_data, f, indent=2, ensure_ascii=False)
                        
                        backup_info = f"ðŸ’¾ Backup created: {backup_path.name}"
                        saved = True
                        break
                    except Exception as e:
                        continue
                
                if not saved:
                    backup_info = "âš ï¸ Backup failed - proceeding with reset"
                
            except Exception as e:
                backup_info = f"âš ï¸ Backup error: {str(e)[:50]}... - proceeding with reset"
        
        # Perform reset based on type
        original_stats = brain_data.get_performance_stats()
        
        if reset_type == "complete":
            # Complete reset - create fresh brain data
            new_brain = BrainData()
            new_brain.add_node_to_chain("PromptBrainResetDirect")
            status = f"ðŸ”„ Complete brain reset - all data cleared\n{backup_info}\nðŸ“Š Before: {original_stats['total_tags']} tags, {original_stats['total_history']} events"
            
        elif reset_type == "preserve_styles":
            # Reset but keep styles and features
            preserved_styles = brain_data.get_styles()
            preserved_features = brain_data.get_features()
            
            new_brain = BrainData()
            new_brain.data["styles"] = preserved_styles
            new_brain.data["features"] = preserved_features
            new_brain.add_node_to_chain("PromptBrainResetDirect")
            status = f"ðŸ”„ Brain reset (styles preserved) - tags and history cleared\n{backup_info}\nðŸ“Š Before: {original_stats['total_tags']} tags, {original_stats['total_history']} events"
            
        elif reset_type == "preserve_history":
            # Reset but keep learning history
            preserved_history = brain_data.get_history()
            
            new_brain = BrainData()
            new_brain.data["history"] = preserved_history
            new_brain.add_node_to_chain("PromptBrainResetDirect")
            status = f"ðŸ”„ Brain reset (history preserved) - tags cleared, {len(preserved_history)} history events kept\n{backup_info}\nðŸ“Š Before: {original_stats['total_tags']} tags"
        
        else:
            # Fallback to complete reset
            new_brain = BrainData()
            new_brain.add_node_to_chain("PromptBrainResetDirect")
            status = f"ðŸ”„ Complete brain reset (fallback) - all data cleared\n{backup_info}\nðŸ“Š Before: {original_stats['total_tags']} tags, {original_stats['total_history']} events"
        
        return (new_brain, status)


class BrainsXDEV_PromptBrainQualityScore:
    """
    Enhanced AI-powered quality scoring node with advanced analysis features
    Provides comprehensive image quality assessment with multiple scoring algorithms
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"tooltip": "Generated image to analyze for quality"}),
                "caption": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Caption or prompt that generated this image"
                })
            },
            "optional": {
                "scoring_criteria": (["overall_quality", "prompt_adherence", "artistic_merit", 
                                    "technical_quality", "creativity", "composition", "color_harmony", 
                                    "detail_richness", "style_consistency", "emotional_impact"], {
                    "default": "overall_quality",
                    "tooltip": "Primary scoring criterion"
                }),
                "analysis_depth": (["basic", "standard", "detailed", "expert"], {
                    "default": "standard",
                    "tooltip": "Depth of quality analysis"
                }),
                "scoring_model": (["balanced", "conservative", "generous", "artistic", "technical"], {
                    "default": "balanced",
                    "tooltip": "Scoring model personality"
                }),
                "score_boost": ("FLOAT", {
                    "default": 0.0,
                    "min": -0.5,
                    "max": 0.5,
                    "step": 0.05,
                    "tooltip": "Manual adjustment to AI score"
                }),
                "minimum_score": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 0.5,
                    "step": 0.05,
                    "tooltip": "Minimum allowable score (quality threshold)"
                }),
                "enable_histogram_analysis": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable advanced histogram-based color analysis"
                }),
                "enable_composition_analysis": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable rule-of-thirds and composition analysis"
                }),
                "enable_noise_detection": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable noise and artifact detection"
                }),
                "enable_semantic_analysis": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable prompt-image semantic matching"
                })
            }
        }
    
    RETURN_TYPES = ("FLOAT", "STRING", "STRING", "FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("quality_score", "detailed_analysis", "quality_grade", "technical_score", "artistic_score", "semantic_score")
    FUNCTION = "analyze_quality"
    CATEGORY = "Brains-XDEV/PromptBrain"
    DESCRIPTION = "Enhanced AI-powered quality scoring with comprehensive analysis features"
    
    def analyze_quality(self, image, caption: str, scoring_criteria: str = "overall_quality", 
                       analysis_depth: str = "standard", scoring_model: str = "balanced",
                       score_boost: float = 0.0, minimum_score: float = 0.0,
                       enable_histogram_analysis: bool = True, enable_composition_analysis: bool = True,
                       enable_noise_detection: bool = True, enable_semantic_analysis: bool = True):
        """Enhanced image quality analysis with comprehensive features"""
        try:
            import torch
            import numpy as np
            
            # Validate and fix parameter values to prevent validation errors
            valid_analysis_depths = ["basic", "standard", "detailed", "expert"]
            if analysis_depth not in valid_analysis_depths:
                print(f"Warning: Invalid analysis_depth '{analysis_depth}', using 'standard'")
                analysis_depth = "standard"
            
            valid_scoring_criteria = ["overall_quality", "prompt_adherence", "artistic_merit", 
                                    "technical_quality", "creativity", "composition", "color_harmony", 
                                    "detail_richness", "style_consistency", "emotional_impact"]
            if scoring_criteria not in valid_scoring_criteria:
                print(f"Warning: Invalid scoring_criteria '{scoring_criteria}', using 'overall_quality'")
                scoring_criteria = "overall_quality"
            
            valid_scoring_models = ["balanced", "conservative", "generous", "artistic", "technical"]
            if scoring_model not in valid_scoring_models:
                print(f"Warning: Invalid scoring_model '{scoring_model}', using 'balanced'")
                scoring_model = "balanced"
            
            # Initialize analysis results
            analysis_results = {
                "technical_metrics": {},
                "artistic_metrics": {},
                "semantic_metrics": {},
                "composition_metrics": {},
                "quality_flags": []
            }
            
            # Convert image tensor to analyzable format
            if isinstance(image, torch.Tensor):
                # ComfyUI image format: [batch, height, width, channels]
                img_array = image[0].cpu().numpy()
                height, width = img_array.shape[:2]
                channels = img_array.shape[2] if len(img_array.shape) == 3 else 1
                
                # Basic image quality metrics
                brightness = np.mean(img_array)
                contrast = np.std(img_array)
                
                # Enhanced sharpness detection using multiple methods
                sharpness_scores = self.calculate_enhanced_sharpness(img_array)
                sharpness = np.mean(list(sharpness_scores.values()))
                
                # Advanced color analysis
                color_metrics = self.analyze_color_properties(img_array, enable_histogram_analysis)
                
                # Composition analysis
                composition_metrics = {}
                if enable_composition_analysis:
                    composition_metrics = self.analyze_composition(img_array)
                
                # Noise and artifact detection
                noise_metrics = {}
                if enable_noise_detection:
                    noise_metrics = self.detect_noise_and_artifacts(img_array)
                
                # Store metrics
                analysis_results["technical_metrics"] = {
                    "brightness": brightness,
                    "contrast": contrast,
                    "sharpness": sharpness,
                    "sharpness_breakdown": sharpness_scores,
                    "resolution": {"width": width, "height": height, "channels": channels},
                    "dynamic_range": np.max(img_array) - np.min(img_array)
                }
                analysis_results["technical_metrics"].update(color_metrics)
                analysis_results["composition_metrics"] = composition_metrics
                analysis_results["technical_metrics"].update(noise_metrics)
                
            else:
                # Fallback for non-tensor input
                analysis_results["technical_metrics"] = {
                    "brightness": 0.5, "contrast": 0.5, "sharpness": 0.5,
                    "color_balance": 0.5, "color_harmony": 0.5
                }
                analysis_results["quality_flags"].append("âš ï¸ Fallback mode - limited analysis")
            
            # Enhanced caption analysis
            if enable_semantic_analysis:
                semantic_metrics = self.analyze_semantic_quality(caption, analysis_depth)
                analysis_results["semantic_metrics"] = semantic_metrics
            else:
                analysis_results["semantic_metrics"] = {"caption_score": 0.5}
            
            # Calculate scores using enhanced algorithms
            technical_score = self.calculate_technical_score(analysis_results["technical_metrics"], scoring_model)
            artistic_score = self.calculate_artistic_score(analysis_results, scoring_model)
            semantic_score = analysis_results["semantic_metrics"].get("caption_score", 0.5)
            
            # Calculate final score based on criteria and depth
            final_score = self.calculate_final_score(
                technical_score, artistic_score, semantic_score,
                scoring_criteria, scoring_model, analysis_depth
            )
            
            # Apply adjustments
            final_score = max(minimum_score, min(1.0, final_score + score_boost))
            
            # Generate comprehensive analysis report
            detailed_analysis = self.generate_comprehensive_report(
                analysis_results, technical_score, artistic_score, semantic_score,
                final_score, scoring_criteria, analysis_depth, scoring_model
            )
            
            # Generate quality grade
            quality_grade = self.generate_quality_grade(final_score)
            
            return (final_score, detailed_analysis, quality_grade, technical_score, artistic_score, semantic_score)
            
        except Exception as e:
            # Enhanced fallback with error details
            fallback_score = max(minimum_score, min(1.0, 0.5 + score_boost))
            
            error_analysis = f"âŒ Enhanced AI Analysis Error\n"
            error_analysis += f"ðŸ”§ Error Details: {str(e)}\n"
            error_analysis += f"ðŸ“Š Fallback Score: {fallback_score:.3f}\n"
            error_analysis += f"âš™ï¸ Analysis Depth: {analysis_depth}\n"
            error_analysis += f"ðŸŽ¯ Scoring Model: {scoring_model}\n"
            error_analysis += "ðŸ’¡ Using safe fallback scoring"
            
            quality_grade = self.generate_quality_grade(fallback_score)
            
            return (fallback_score, error_analysis, quality_grade, fallback_score, fallback_score, fallback_score)
    
    def calculate_enhanced_sharpness(self, img_array):
        """Calculate multiple sharpness metrics for comprehensive analysis"""
        import numpy as np
        
        metrics = {}
        height, width = img_array.shape[:2]
        
        if height > 2 and width > 2:
            # Gradient-based sharpness (Sobel-like)
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            # Horizontal and vertical gradients
            grad_x = np.abs(np.diff(gray, axis=1))
            grad_y = np.abs(np.diff(gray, axis=0))
            metrics["gradient_sharpness"] = (np.mean(grad_x) + np.mean(grad_y)) / 2
            
            # Laplacian-based sharpness
            if height > 3 and width > 3:
                # Simple Laplacian approximation
                laplacian = np.abs(gray[1:-1, 1:-1] * 4 - gray[:-2, 1:-1] - gray[2:, 1:-1] - gray[1:-1, :-2] - gray[1:-1, 2:])
                metrics["laplacian_sharpness"] = np.mean(laplacian)
            else:
                metrics["laplacian_sharpness"] = metrics["gradient_sharpness"]
            
            # Variance-based sharpness
            metrics["variance_sharpness"] = np.var(gray)
            
            # Edge density
            edge_threshold = np.std(gray) * 0.5
            edges = (grad_x > edge_threshold).sum() + (grad_y > edge_threshold).sum()
            total_pixels = gray.size
            metrics["edge_density"] = edges / total_pixels if total_pixels > 0 else 0
            
        else:
            # Fallback for small images
            metrics = {
                "gradient_sharpness": 0.5,
                "laplacian_sharpness": 0.5,
                "variance_sharpness": 0.5,
                "edge_density": 0.5
            }
        
        return metrics
    
    def analyze_color_properties(self, img_array, enable_histogram=True):
        """Advanced color analysis including harmony and distribution"""
        import numpy as np
        
        metrics = {}
        
        if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
            # RGB channels
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
            
            # Color balance (variance across channels)
            color_variance = np.var([np.mean(r), np.mean(g), np.mean(b)])
            metrics["color_balance"] = 1.0 - min(1.0, color_variance * 10)  # Inverse relationship
            
            # Color saturation
            max_rgb = np.maximum(np.maximum(r, g), b)
            min_rgb = np.minimum(np.minimum(r, g), b)
            saturation = np.mean((max_rgb - min_rgb) / (max_rgb + 1e-8))
            metrics["color_saturation"] = saturation
            
            # Color harmony (complementary color analysis)
            if enable_histogram:
                # Simplified color wheel analysis
                hue_approx = np.arctan2(g - b, r - g) % (2 * np.pi)
                hue_variance = np.var(hue_approx)
                metrics["color_harmony"] = 1.0 - min(1.0, hue_variance / np.pi)
                
                # Color temperature estimation
                blue_dominance = np.mean(b) - np.mean(r)
                metrics["color_temperature"] = 0.5 + blue_dominance  # Simplified
            else:
                metrics["color_harmony"] = 0.7  # Default good harmony
                metrics["color_temperature"] = 0.5
            
            # Dynamic range per channel
            metrics["red_range"] = np.max(r) - np.min(r)
            metrics["green_range"] = np.max(g) - np.min(g)
            metrics["blue_range"] = np.max(b) - np.min(b)
            metrics["avg_dynamic_range"] = (metrics["red_range"] + metrics["green_range"] + metrics["blue_range"]) / 3
            
        else:
            # Grayscale or limited color
            metrics = {
                "color_balance": 0.5,
                "color_saturation": 0.0,
                "color_harmony": 0.5,
                "color_temperature": 0.5,
                "avg_dynamic_range": np.max(img_array) - np.min(img_array) if img_array.size > 0 else 0
            }
        
        return metrics
    
    def analyze_composition(self, img_array):
        """Analyze composition using rule of thirds and balance"""
        import numpy as np
        
        metrics = {}
        height, width = img_array.shape[:2]
        
        if height > 6 and width > 6:  # Minimum size for composition analysis
            # Convert to grayscale for analysis
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            # Rule of thirds analysis
            third_h, third_w = height // 3, width // 3
            
            # Divide image into 9 sections
            sections = []
            for i in range(3):
                for j in range(3):
                    start_h, end_h = i * third_h, (i + 1) * third_h
                    start_w, end_w = j * third_w, (j + 1) * third_w
                    section = gray[start_h:end_h, start_w:end_w]
                    sections.append(np.mean(section))
            
            # Calculate interest points (high variance sections)
            section_variances = []
            for i in range(3):
                for j in range(3):
                    start_h, end_h = i * third_h, (i + 1) * third_h
                    start_w, end_w = j * third_w, (j + 1) * third_w
                    section = gray[start_h:end_h, start_w:end_w]
                    section_variances.append(np.var(section))
            
            # Rule of thirds score (interest at intersection points)
            # Sections 1, 3, 5, 7 are near rule-of-thirds intersections
            intersection_sections = [1, 3, 5, 7]
            intersection_interest = np.mean([section_variances[i] for i in intersection_sections])
            total_interest = np.mean(section_variances)
            metrics["rule_of_thirds"] = intersection_interest / (total_interest + 1e-8)
            
            # Balance analysis (left-right, top-bottom)
            left_half = np.mean(gray[:, :width//2])
            right_half = np.mean(gray[:, width//2:])
            top_half = np.mean(gray[:height//2, :])
            bottom_half = np.mean(gray[height//2:, :])
            
            metrics["horizontal_balance"] = 1.0 - abs(left_half - right_half)
            metrics["vertical_balance"] = 1.0 - abs(top_half - bottom_half)
            
            # Center focus vs edge focus
            center_quarter = gray[height//4:3*height//4, width//4:3*width//4]
            center_interest = np.var(center_quarter)
            edge_interest = (np.var(gray[:height//4, :]) + np.var(gray[3*height//4:, :]) + 
                           np.var(gray[:, :width//4]) + np.var(gray[:, 3*width//4:])) / 4
            metrics["center_focus"] = center_interest / (center_interest + edge_interest + 1e-8)
            
        else:
            # Fallback for small images
            metrics = {
                "rule_of_thirds": 0.7,
                "horizontal_balance": 0.8,
                "vertical_balance": 0.8,
                "center_focus": 0.6
            }
        
        return metrics
    
    def detect_noise_and_artifacts(self, img_array):
        """Detect noise and compression artifacts"""
        import numpy as np
        
        metrics = {}
        
        if img_array.size > 100:  # Minimum size for noise detection
            # Convert to grayscale
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            # High frequency noise detection
            if gray.shape[0] > 2 and gray.shape[1] > 2:
                # Calculate second derivatives (approximation of high-frequency content)
                diff2_h = np.abs(np.diff(gray, n=2, axis=0))
                diff2_v = np.abs(np.diff(gray, n=2, axis=1))
                high_freq = (np.mean(diff2_h) + np.mean(diff2_v)) / 2
                
                # Normalize and invert (lower is better)
                metrics["noise_level"] = min(1.0, high_freq * 20)
                metrics["clarity"] = 1.0 - metrics["noise_level"]
                
                # Blocking artifacts detection (simplified)
                # Look for regular patterns that might indicate compression
                block_size = 8
                if gray.shape[0] >= block_size and gray.shape[1] >= block_size:
                    block_variances = []
                    for i in range(0, gray.shape[0] - block_size, block_size):
                        for j in range(0, gray.shape[1] - block_size, block_size):
                            block = gray[i:i+block_size, j:j+block_size]
                            block_variances.append(np.var(block))
                    
                    if block_variances:
                        block_variance_uniformity = 1.0 - np.var(block_variances) / (np.mean(block_variances) + 1e-8)
                        metrics["blocking_artifacts"] = max(0.0, block_variance_uniformity - 0.8) * 5  # Detect excessive uniformity
                    else:
                        metrics["blocking_artifacts"] = 0.0
                else:
                    metrics["blocking_artifacts"] = 0.0
            else:
                metrics["noise_level"] = 0.5
                metrics["clarity"] = 0.5
                metrics["blocking_artifacts"] = 0.0
        else:
            metrics = {"noise_level": 0.3, "clarity": 0.7, "blocking_artifacts": 0.0}
        
        return metrics
    
    def analyze_semantic_quality(self, caption: str, analysis_depth: str):
        """Enhanced semantic analysis of caption quality"""
        if not caption or len(caption.strip()) < 3:
            # More graceful handling of empty captions
            return {
                "caption_score": 0.3,  # Slightly higher base score
                "word_count": 0, 
                "complexity": "minimal",
                "vocabulary_score": 0.0,
                "style_score": 0.0,
                "technical_score": 0.0,
                "unique_word_ratio": 0.0,
                "char_count": len(caption.strip()) if caption else 0
            }
        
        words = caption.lower().split()
        word_count = len(words)
        char_count = len(caption)
        
        # Basic metrics
        length_score = min(1.0, word_count / 25.0)  # Optimal around 25 words
        detail_score = min(1.0, char_count / 250.0)  # Good detail around 250 chars
        
        # Advanced vocabulary analysis based on depth
        quality_words = {
            "basic": ["detailed", "beautiful", "high quality", "professional"],
            "standard": ["detailed", "beautiful", "stunning", "high quality", "professional", 
                        "artistic", "cinematic", "masterpiece", "intricate", "elegant"],
            "detailed": ["detailed", "beautiful", "stunning", "high quality", "professional", 
                        "artistic", "cinematic", "masterpiece", "intricate", "elegant", "exquisite",
                        "sophisticated", "atmospheric", "photorealistic", "hyperdetailed"],
            "expert": ["detailed", "beautiful", "stunning", "high quality", "professional", 
                      "artistic", "cinematic", "masterpiece", "intricate", "elegant", "exquisite",
                      "sophisticated", "atmospheric", "photorealistic", "hyperdetailed", "chiaroscuro",
                      "bokeh", "composition", "dynamic", "ethereal", "luminous", "textural"]
        }
        
        style_indicators = ["photorealistic", "artistic", "anime", "oil painting", "watercolor", 
                          "digital art", "3d render", "photograph", "sketch", "illustration"]
        technical_terms = ["4k", "8k", "uhd", "hdr", "ray tracing", "octane render", "unreal engine",
                          "depth of field", "bokeh", "golden hour", "dramatic lighting"]
        
        # Count quality indicators
        quality_list = quality_words.get(analysis_depth, quality_words["standard"])
        quality_count = sum(1 for word in quality_list if word in caption.lower())
        style_count = sum(1 for term in style_indicators if term in caption.lower())
        tech_count = sum(1 for term in technical_terms if term in caption.lower())
        
        # Calculate scores
        vocabulary_score = min(1.0, quality_count / len(quality_list) * 3)
        style_score = min(1.0, style_count / 2)
        technical_score = min(1.0, tech_count / 3)
        
        # Complexity analysis
        unique_words = len(set(words))
        complexity_ratio = unique_words / word_count if word_count > 0 else 0
        
        if complexity_ratio > 0.8:
            complexity = "high"
            complexity_bonus = 0.1
        elif complexity_ratio > 0.6:
            complexity = "medium"
            complexity_bonus = 0.05
        else:
            complexity = "basic"
            complexity_bonus = 0.0
        
        # Combine scores
        base_score = (length_score + detail_score + vocabulary_score + style_score + technical_score) / 5
        final_caption_score = min(1.0, base_score + complexity_bonus)
        
        return {
            "caption_score": final_caption_score,
            "word_count": word_count,
            "char_count": char_count,
            "complexity": complexity,
            "vocabulary_score": vocabulary_score,
            "style_score": style_score,
            "technical_score": technical_score,
            "unique_word_ratio": complexity_ratio
        }
    
    def calculate_technical_score(self, technical_metrics, scoring_model):
        """Calculate technical quality score"""
        # Normalize metrics
        brightness = max(0.0, min(1.0, technical_metrics.get("brightness", 0.5)))
        contrast = max(0.0, min(1.0, technical_metrics.get("contrast", 0.5) * 2))
        sharpness = max(0.0, min(1.0, technical_metrics.get("sharpness", 0.5) * 3))
        clarity = technical_metrics.get("clarity", 0.7)
        dynamic_range = max(0.0, min(1.0, technical_metrics.get("dynamic_range", 0.5)))
        
        # Scoring model adjustments
        if scoring_model == "conservative":
            weights = {"sharpness": 0.4, "contrast": 0.3, "clarity": 0.2, "brightness": 0.1}
            penalty = 0.1
        elif scoring_model == "generous":
            weights = {"sharpness": 0.25, "contrast": 0.25, "clarity": 0.25, "brightness": 0.25}
            penalty = -0.05  # Boost
        elif scoring_model == "technical":
            weights = {"sharpness": 0.5, "contrast": 0.25, "clarity": 0.2, "brightness": 0.05}
            penalty = 0.0
        else:  # balanced
            weights = {"sharpness": 0.35, "contrast": 0.25, "clarity": 0.25, "brightness": 0.15}
            penalty = 0.0
        
        score = (sharpness * weights["sharpness"] + 
                contrast * weights["contrast"] + 
                clarity * weights["clarity"] + 
                brightness * weights["brightness"])
        
        return max(0.0, min(1.0, score + penalty))
    
    def calculate_artistic_score(self, analysis_results, scoring_model):
        """Calculate artistic quality score"""
        color_metrics = analysis_results["technical_metrics"]
        composition_metrics = analysis_results["composition_metrics"]
        
        # Extract color metrics
        color_harmony = color_metrics.get("color_harmony", 0.7)
        color_balance = color_metrics.get("color_balance", 0.7)
        saturation = color_metrics.get("color_saturation", 0.5)
        
        # Extract composition metrics
        rule_of_thirds = composition_metrics.get("rule_of_thirds", 0.7)
        balance = (composition_metrics.get("horizontal_balance", 0.8) + 
                  composition_metrics.get("vertical_balance", 0.8)) / 2
        
        # Scoring model adjustments
        if scoring_model == "artistic":
            weights = {"harmony": 0.3, "composition": 0.3, "balance": 0.25, "saturation": 0.15}
            bonus = 0.05
        elif scoring_model == "conservative":
            weights = {"harmony": 0.2, "composition": 0.2, "balance": 0.3, "saturation": 0.3}
            bonus = -0.05
        elif scoring_model == "generous":
            weights = {"harmony": 0.25, "composition": 0.25, "balance": 0.25, "saturation": 0.25}
            bonus = 0.1
        else:  # balanced or technical
            weights = {"harmony": 0.25, "composition": 0.3, "balance": 0.3, "saturation": 0.15}
            bonus = 0.0
        
        score = (color_harmony * weights["harmony"] + 
                rule_of_thirds * weights["composition"] + 
                balance * weights["balance"] + 
                saturation * weights["saturation"])
        
        return max(0.0, min(1.0, score + bonus))
    
    def calculate_final_score(self, technical_score, artistic_score, semantic_score,
                            scoring_criteria, scoring_model, analysis_depth):
        """Calculate final weighted score based on criteria"""
        
        # Base weights by criteria
        if scoring_criteria == "technical_quality":
            weights = {"technical": 0.6, "artistic": 0.2, "semantic": 0.2}
        elif scoring_criteria == "artistic_merit":
            weights = {"technical": 0.2, "artistic": 0.6, "semantic": 0.2}
        elif scoring_criteria == "prompt_adherence":
            weights = {"technical": 0.2, "artistic": 0.2, "semantic": 0.6}
        elif scoring_criteria == "creativity":
            weights = {"technical": 0.15, "artistic": 0.35, "semantic": 0.5}
        elif scoring_criteria == "composition":
            weights = {"technical": 0.3, "artistic": 0.5, "semantic": 0.2}
        elif scoring_criteria == "color_harmony":
            weights = {"technical": 0.25, "artistic": 0.6, "semantic": 0.15}
        elif scoring_criteria == "detail_richness":
            weights = {"technical": 0.5, "artistic": 0.3, "semantic": 0.2}
        elif scoring_criteria == "style_consistency":
            weights = {"technical": 0.2, "artistic": 0.4, "semantic": 0.4}
        elif scoring_criteria == "emotional_impact":
            weights = {"technical": 0.15, "artistic": 0.45, "semantic": 0.4}
        else:  # overall_quality
            weights = {"technical": 0.4, "artistic": 0.35, "semantic": 0.25}
        
        # Analysis depth adjustments
        if analysis_depth == "expert":
            # More demanding scoring
            depth_modifier = 0.95
        elif analysis_depth == "detailed":
            depth_modifier = 0.98
        elif analysis_depth == "basic":
            # More lenient scoring
            depth_modifier = 1.05
        else:  # standard
            depth_modifier = 1.0
        
        final_score = (technical_score * weights["technical"] + 
                      artistic_score * weights["artistic"] + 
                      semantic_score * weights["semantic"]) * depth_modifier
        
        return max(0.0, min(1.0, final_score))
    
    def generate_quality_grade(self, score):
        """Generate letter grade from score"""
        if score >= 0.95:
            return "A+"
        elif score >= 0.9:
            return "A"
        elif score >= 0.85:
            return "A-"
        elif score >= 0.8:
            return "B+"
        elif score >= 0.75:
            return "B"
        elif score >= 0.7:
            return "B-"
        elif score >= 0.65:
            return "C+"
        elif score >= 0.6:
            return "C"
        elif score >= 0.55:
            return "C-"
        elif score >= 0.5:
            return "D+"
        elif score >= 0.45:
            return "D"
        elif score >= 0.4:
            return "D-"
        else:
            return "F"
    
    def generate_comprehensive_report(self, analysis_results, technical_score, artistic_score, 
                                    semantic_score, final_score, scoring_criteria, analysis_depth, scoring_model):
        """Generate detailed analysis report"""
        
        report = f"ðŸ¤– Enhanced AI Quality Analysis\n"
        report += f"{'='*50}\n"
        report += f"ðŸ“Š Final Score: {final_score:.3f} | Grade: {self.generate_quality_grade(final_score)}\n"
        report += f"ðŸŽ¯ Criteria: {scoring_criteria.replace('_', ' ').title()}\n"
        report += f"ðŸ” Analysis Depth: {analysis_depth.title()}\n"
        report += f"âš™ï¸ Scoring Model: {scoring_model.title()}\n\n"
        
        # Score breakdown
        report += f"ðŸ“ˆ Score Breakdown:\n"
        report += f"   ðŸ”§ Technical: {technical_score:.3f}\n"
        report += f"   ðŸŽ¨ Artistic: {artistic_score:.3f}\n"
        report += f"   ðŸ“ Semantic: {semantic_score:.3f}\n\n"
        
        # Technical metrics
        tech_metrics = analysis_results["technical_metrics"]
        report += f"ðŸ” Technical Analysis:\n"
        report += f"   â€¢ Brightness: {tech_metrics.get('brightness', 0):.3f}\n"
        report += f"   â€¢ Contrast: {tech_metrics.get('contrast', 0):.3f}\n"
        report += f"   â€¢ Sharpness: {tech_metrics.get('sharpness', 0):.3f}\n"
        report += f"   â€¢ Clarity: {tech_metrics.get('clarity', 0):.3f}\n"
        report += f"   â€¢ Color Balance: {tech_metrics.get('color_balance', 0):.3f}\n"
        report += f"   â€¢ Color Harmony: {tech_metrics.get('color_harmony', 0):.3f}\n"
        report += f"   â€¢ Noise Level: {tech_metrics.get('noise_level', 0):.3f}\n\n"
        
        # Composition analysis
        if analysis_results["composition_metrics"]:
            comp_metrics = analysis_results["composition_metrics"]
            report += f"ðŸŽ¨ Composition Analysis:\n"
            report += f"   â€¢ Rule of Thirds: {comp_metrics.get('rule_of_thirds', 0):.3f}\n"
            report += f"   â€¢ Horizontal Balance: {comp_metrics.get('horizontal_balance', 0):.3f}\n"
            report += f"   â€¢ Vertical Balance: {comp_metrics.get('vertical_balance', 0):.3f}\n"
            report += f"   â€¢ Center Focus: {comp_metrics.get('center_focus', 0):.3f}\n\n"
        
        # Semantic analysis
        if analysis_results["semantic_metrics"]:
            sem_metrics = analysis_results["semantic_metrics"]
            report += f"ðŸ“ Semantic Analysis:\n"
            report += f"   â€¢ Caption Quality: {sem_metrics.get('caption_score', 0):.3f}\n"
            report += f"   â€¢ Word Count: {sem_metrics.get('word_count', 0)}\n"
            report += f"   â€¢ Complexity: {sem_metrics.get('complexity', 'unknown').title()}\n"
            report += f"   â€¢ Vocabulary Score: {sem_metrics.get('vocabulary_score', 0):.3f}\n\n"
        
        # Quality assessment
        if final_score >= 0.9:
            report += "âœ… Exceptional Quality - Premium learning value\n"
            report += "ðŸ† Recommended for showcase and training\n"
        elif final_score >= 0.8:
            report += "ðŸŸ¢ Excellent Quality - High learning value\n"
            report += "ðŸ“š Great for training and reference\n"
        elif final_score >= 0.7:
            report += "ðŸŸ¡ Good Quality - Suitable for learning\n"
            report += "ðŸ“– Acceptable for training datasets\n"
        elif final_score >= 0.6:
            report += "ðŸŸ  Fair Quality - Moderate learning value\n"
            report += "âš ï¸ Consider improvements before training\n"
        elif final_score >= 0.4:
            report += "ðŸ”´ Below Average - Limited learning value\n"
            report += "ðŸ”„ Recommend regeneration with improvements\n"
        else:
            report += "âŒ Poor Quality - Not suitable for learning\n"
            report += "ðŸš« Regeneration strongly recommended\n"
        
        # Improvement suggestions
        report += f"\nðŸ’¡ Improvement Suggestions:\n"
        if technical_score < 0.7:
            report += "   ðŸ”§ Technical: Consider higher resolution, better lighting\n"
        if artistic_score < 0.7:
            report += "   ðŸŽ¨ Artistic: Improve composition, color harmony\n"
        if semantic_score < 0.7:
            report += "   ðŸ“ Semantic: Add more descriptive details to prompt\n"
        
        return report


class BrainsXDEV_PromptBrainKSamplerDirect:
    """
    Intelligent KSampler that adjusts parameters based on quality analysis
    Uses technical, artistic, and semantic scores to optimize sampling settings
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "brain_data": ("BRAIN", {"forceInput": True}),
                "model": ("MODEL",),
                "positive": ("CONDITIONING",),
                "negative": ("CONDITIONING",),
                "latent_image": ("LATENT",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            },
            "optional": {
                "quality_analysis": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Paste quality analysis output to optimize settings"
                }),
                "auto_optimize": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Automatically adjust parameters based on quality scores"
                }),
                "optimization_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "How aggressively to apply optimizations"
                }),
                "manual_steps": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 150,
                    "tooltip": "Override steps (0 = auto-optimize)"
                }),
                "manual_cfg": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 30.0,
                    "step": 0.1,
                    "tooltip": "Override CFG (0 = auto-optimize)"
                })
            }
        }
    
    RETURN_TYPES = ("BRAIN", "LATENT", "STRING")
    RETURN_NAMES = ("brain_data", "samples", "optimization_report")
    FUNCTION = "ksampler_direct"
    CATEGORY = "Brains-XDEV/PromptBrain"
    DESCRIPTION = "Intelligent KSampler with quality-based parameter optimization"
    
    def ksampler_direct(self, brain_data: BrainData, model, positive, negative, latent_image, 
                       seed: int, quality_analysis: str = "", auto_optimize: bool = True,
                       optimization_strength: float = 1.0, manual_steps: int = 0, 
                       manual_cfg: float = 0.0):
        """Intelligent KSampler with quality-based optimization"""
        
        # Parse quality analysis if provided
        quality_metrics = self.parse_quality_analysis(quality_analysis)
        
        # Determine optimal sampling parameters
        if auto_optimize and quality_metrics:
            steps, cfg, sampler_name, scheduler = self.optimize_parameters(
                quality_metrics, optimization_strength
            )
        else:
            # Default parameters
            steps = 20
            cfg = 8.0
            sampler_name = "euler"
            scheduler = "normal"
        
        # Apply manual overrides
        if manual_steps > 0:
            steps = manual_steps
        if manual_cfg > 0.0:
            cfg = manual_cfg
        
        # Perform sampling using ComfyUI's KSampler logic
        try:
            # Import ComfyUI sampling modules
            import comfy.sample
            import comfy.samplers
            import random
            
            # Generate optimization report first
            report = self.generate_optimization_report(
                quality_metrics, steps, cfg, sampler_name, scheduler, 
                auto_optimize, optimization_strength
            )
            
            # Prepare sampling parameters
            noise_seed = seed
            if seed == 0:
                noise_seed = random.randint(1, 0xffffffffffffffff)
            
            # Get latent samples
            latent_samples = latent_image["samples"]
            
            # Prepare noise for sampling
            noise = comfy.sample.prepare_noise(latent_samples, noise_seed, None)
            
            # Create sampling callback function (ComfyUI pattern)
            def callback(step, x0, x, total_steps):
                # Optional: could add progress tracking here
                pass
            
            # Perform sampling using ComfyUI's standard method
            samples = comfy.sample.sample(
                model=model,
                noise=noise,
                steps=steps,
                cfg=cfg,
                sampler_name=sampler_name,
                scheduler=scheduler,
                positive=positive,
                negative=negative,
                latent_image=latent_samples,
                denoise=1.0,
                disable_noise=False,
                start_step=None,
                last_step=None,
                force_full_denoise=False,
                noise_mask=None,
                callback=callback,
                disable_pbar=False,
                seed=noise_seed
            )
            
            # Format output as expected latent structure
            output_samples = {"samples": samples}
            
            # Track node processing
            brain_data.add_node_to_chain("PromptBrainKSamplerDirect")
            
            return (brain_data, output_samples, report)
            
        except ImportError as e:
            # ComfyUI modules not available - return optimized parameters as text
            error_report = f"âš ï¸ ComfyUI sampling not available: {str(e)}\n\n"
            error_report += self.generate_optimization_report(
                quality_metrics, steps, cfg, sampler_name, scheduler, 
                auto_optimize, optimization_strength
            )
            error_report += f"\n\nðŸ”§ Use these optimized parameters with a regular KSampler:\n"
            error_report += f"â€¢ Steps: {steps}\nâ€¢ CFG: {cfg}\nâ€¢ Sampler: {sampler_name}\nâ€¢ Scheduler: {scheduler}\nâ€¢ Seed: {seed}"
            
            # Return pass-through latent
            brain_data.add_node_to_chain("PromptBrainKSamplerDirect")
            return (brain_data, latent_image, error_report)
            
        except Exception as e:
            # Other sampling errors - provide detailed fallback
            error_report = f"âŒ Sampling error: {str(e)}\n\n"
            error_report += "ðŸ”§ Troubleshooting:\n"
            error_report += "â€¢ Ensure model, conditioning, and latent are properly connected\n"
            error_report += "â€¢ Check that sampler name is valid (euler, dpm_2, etc.)\n"
            error_report += "â€¢ Verify scheduler is compatible (normal, karras, exponential)\n\n"
            
            error_report += self.generate_optimization_report(
                quality_metrics, steps, cfg, sampler_name, scheduler, 
                auto_optimize, optimization_strength
            )
            error_report += f"\n\nðŸ”§ Optimized parameters to try manually:\n"
            error_report += f"â€¢ Steps: {steps}\nâ€¢ CFG: {cfg}\nâ€¢ Sampler: {sampler_name}\nâ€¢ Scheduler: {scheduler}\nâ€¢ Seed: {seed}"
            
            # Return pass-through latent
            brain_data.add_node_to_chain("PromptBrainKSamplerDirect")
            return (brain_data, latent_image, error_report)
    
    def parse_quality_analysis(self, analysis_text: str) -> dict:
        """Parse quality analysis text to extract metrics"""
        metrics = {
            "technical_score": 0.5,
            "artistic_score": 0.5,
            "semantic_score": 0.5,
            "final_score": 0.5,
            "grade": "C",
            "sharpness": 0.5,
            "contrast": 0.5,
            "brightness": 0.5,
            "color_harmony": 0.5,
            "rule_of_thirds": 0.5
        }
        
        if not analysis_text:
            return metrics
        
        try:
            lines = analysis_text.split('\n')
            for line in lines:
                line = line.strip()
                
                # Parse main scores
                if "ðŸ”§ Technical:" in line:
                    try:
                        score = float(line.split(":")[1].strip())
                        metrics["technical_score"] = score
                    except:
                        pass
                elif "ðŸŽ¨ Artistic:" in line:
                    try:
                        score = float(line.split(":")[1].strip())
                        metrics["artistic_score"] = score
                    except:
                        pass
                elif "ðŸ“ Semantic:" in line:
                    try:
                        score = float(line.split(":")[1].strip())
                        metrics["semantic_score"] = score
                    except:
                        pass
                elif "ðŸ“Š Final Score:" in line:
                    try:
                        score_part = line.split("ðŸ“Š Final Score:")[1].split("|")[0].strip()
                        score = float(score_part)
                        metrics["final_score"] = score
                        
                        # Extract grade
                        if "Grade:" in line:
                            grade = line.split("Grade:")[1].strip().split()[0]
                            metrics["grade"] = grade
                    except:
                        pass
                
                # Parse detailed metrics
                elif "â€¢ Sharpness:" in line:
                    try:
                        score = float(line.split(":")[1].strip())
                        metrics["sharpness"] = score
                    except:
                        pass
                elif "â€¢ Contrast:" in line:
                    try:
                        score = float(line.split(":")[1].strip())
                        metrics["contrast"] = score
                    except:
                        pass
                elif "â€¢ Brightness:" in line:
                    try:
                        score = float(line.split(":")[1].strip())
                        metrics["brightness"] = score
                    except:
                        pass
                elif "â€¢ Color Harmony:" in line:
                    try:
                        score = float(line.split(":")[1].strip())
                        metrics["color_harmony"] = score
                    except:
                        pass
                elif "â€¢ Rule of Thirds:" in line:
                    try:
                        score = float(line.split(":")[1].strip())
                        metrics["rule_of_thirds"] = score
                    except:
                        pass
        
        except Exception as e:
            print(f"âš ï¸ Error parsing quality analysis: {e}")
        
        return metrics
    
    def optimize_parameters(self, quality_metrics: dict, strength: float) -> tuple:
        """Optimize sampling parameters based on quality metrics"""
        
        technical = quality_metrics.get("technical_score", 0.5)
        artistic = quality_metrics.get("artistic_score", 0.5)
        semantic = quality_metrics.get("semantic_score", 0.5)
        final = quality_metrics.get("final_score", 0.5)
        
        sharpness = quality_metrics.get("sharpness", 0.5)
        contrast = quality_metrics.get("contrast", 0.5)
        brightness = quality_metrics.get("brightness", 0.5)
        color_harmony = quality_metrics.get("color_harmony", 0.5)
        
        # Base parameters
        steps = 20
        cfg = 8.0
        sampler_name = "euler"
        scheduler = "normal"
        
        # Optimize steps based on sharpness and technical score
        if sharpness < 0.3 or technical < 0.5:
            # Low sharpness needs more steps
            steps = min(50, int(20 + (1.0 - sharpness) * 30 * strength))
        elif sharpness > 0.8 and technical > 0.7:
            # High quality can use fewer steps
            steps = max(15, int(20 - (sharpness - 0.8) * 25 * strength))
        
        # Optimize CFG based on contrast and artistic score
        if contrast < 0.3 or artistic < 0.5:
            # Low contrast needs higher CFG
            cfg = min(15.0, 8.0 + (1.0 - contrast) * 7.0 * strength)
        elif contrast > 0.8:
            # High contrast can use lower CFG
            cfg = max(5.0, 8.0 - (contrast - 0.8) * 10.0 * strength)
        
        # Choose sampler based on overall quality
        if final < 0.4:
            # Poor quality - use more sophisticated sampler
            sampler_name = "dpmpp_2m"
            scheduler = "karras"
        elif final > 0.8:
            # High quality - can use efficient sampler
            sampler_name = "euler_a"
            scheduler = "normal"
        elif color_harmony < 0.3:
            # Poor color harmony - try different approach
            sampler_name = "dpm_2"
            scheduler = "exponential"
        
        # Adjust based on semantic score
        if semantic < 0.3:
            # Poor semantic content might benefit from higher CFG
            cfg = min(cfg + 2.0 * strength, 20.0)
        
        return int(steps), round(cfg, 1), sampler_name, scheduler
    
    def generate_optimization_report(self, quality_metrics: dict, steps: int, cfg: float, 
                                   sampler_name: str, scheduler: str, auto_optimize: bool,
                                   optimization_strength: float) -> str:
        """Generate report on parameter optimization"""
        
        if not auto_optimize:
            return f"ðŸ”§ Manual Mode - Using specified parameters:\nâ€¢ Steps: {steps}\nâ€¢ CFG: {cfg}\nâ€¢ Sampler: {sampler_name}\nâ€¢ Scheduler: {scheduler}"
        
        if not quality_metrics or quality_metrics.get("final_score", 0.5) == 0.5:
            return f"ðŸ“Š Default Mode - No quality analysis provided:\nâ€¢ Steps: {steps}\nâ€¢ CFG: {cfg}\nâ€¢ Sampler: {sampler_name}\nâ€¢ Scheduler: {scheduler}"
        
        report = "ðŸ§  PromptBrain Intelligent KSampler\n"
        report += "=" * 40 + "\n\n"
        
        # Quality summary
        final_score = quality_metrics.get("final_score", 0.5)
        grade = quality_metrics.get("grade", "C")
        report += f"ðŸ“Š Input Quality: {final_score:.3f} | Grade: {grade}\n"
        report += f"âš™ï¸ Optimization Strength: {optimization_strength:.1f}\n\n"
        
        # Optimized parameters
        report += f"ðŸŽ¯ Optimized Parameters:\n"
        report += f"   â€¢ Steps: {steps}\n"
        report += f"   â€¢ CFG Scale: {cfg}\n"
        report += f"   â€¢ Sampler: {sampler_name}\n"
        report += f"   â€¢ Scheduler: {scheduler}\n\n"
        
        # Optimization reasoning
        report += f"ðŸ§® Optimization Logic:\n"
        
        technical = quality_metrics.get("technical_score", 0.5)
        artistic = quality_metrics.get("artistic_score", 0.5)
        semantic = quality_metrics.get("semantic_score", 0.5)
        sharpness = quality_metrics.get("sharpness", 0.5)
        contrast = quality_metrics.get("contrast", 0.5)
        
        if sharpness < 0.3:
            report += f"   â€¢ Low sharpness ({sharpness:.3f}) â†’ Increased steps to {steps}\n"
        if contrast < 0.3:
            report += f"   â€¢ Low contrast ({contrast:.3f}) â†’ Increased CFG to {cfg}\n"
        if technical < 0.5:
            report += f"   â€¢ Low technical quality ({technical:.3f}) â†’ Enhanced sampling\n"
        if artistic < 0.5:
            report += f"   â€¢ Low artistic quality ({artistic:.3f}) â†’ Adjusted parameters\n"
        if semantic < 0.3:
            report += f"   â€¢ Low semantic quality ({semantic:.3f}) â†’ Higher guidance\n"
        
        # Expected improvements
        report += f"\nðŸ’¡ Expected Improvements:\n"
        if steps > 25:
            report += "   ðŸ” Higher steps should improve detail and sharpness\n"
        if cfg > 10:
            report += "   ðŸŽ¨ Higher CFG should improve prompt adherence\n"
        if sampler_name != "euler":
            report += f"   âš¡ {sampler_name} sampler optimized for current quality profile\n"
        
        return report


class BrainsXDEV_PromptBrainParameterOptimizer:
    """
    AI Parameter Optimizer that outputs optimized KSampler parameters
    Use this with a regular KSampler node for guaranteed compatibility
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "brain_data": ("BRAIN", {"forceInput": True}),
                "quality_analysis": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Paste quality analysis output to optimize settings"
                })
            },
            "optional": {
                "optimization_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "How aggressively to apply optimizations"
                }),
                "base_steps": ("INT", {
                    "default": 20,
                    "min": 1,
                    "max": 150,
                    "tooltip": "Base steps before optimization"
                }),
                "base_cfg": ("FLOAT", {
                    "default": 8.0,
                    "min": 1.0,
                    "max": 30.0,
                    "step": 0.1,
                    "tooltip": "Base CFG before optimization"
                })
            }
        }
    
    RETURN_TYPES = ("BRAIN", "INT", "FLOAT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("brain_data", "optimized_steps", "optimized_cfg", "optimized_sampler", "optimized_scheduler", "optimization_report")
    FUNCTION = "optimize_parameters"
    CATEGORY = "Brains-XDEV/PromptBrain"
    DESCRIPTION = "AI Parameter Optimizer - outputs optimized KSampler parameters"
    
    def optimize_parameters(self, brain_data: BrainData, quality_analysis: str = "",
                          optimization_strength: float = 1.0, base_steps: int = 20, 
                          base_cfg: float = 8.0):
        """Generate optimized parameters for use with regular KSampler"""
        
        # Use the same parser and optimizer from KSamplerDirect
        ksampler_helper = BrainsXDEV_PromptBrainKSamplerDirect()
        
        # Parse quality analysis
        quality_metrics = ksampler_helper.parse_quality_analysis(quality_analysis)
        
        # Set base parameters in the quality metrics for optimization
        quality_metrics["base_steps"] = base_steps
        quality_metrics["base_cfg"] = base_cfg
        
        # Get optimized parameters
        if quality_metrics and quality_analysis.strip():
            steps, cfg, sampler_name, scheduler = ksampler_helper.optimize_parameters(
                quality_metrics, optimization_strength
            )
        else:
            # No quality analysis - return base parameters
            steps = base_steps
            cfg = base_cfg
            sampler_name = "euler"
            scheduler = "normal"
        
        # Generate detailed report
        report = ksampler_helper.generate_optimization_report(
            quality_metrics, steps, cfg, sampler_name, scheduler, 
            bool(quality_analysis.strip()), optimization_strength
        )
        
        # Add connection instructions
        if quality_analysis.strip():
            report += f"\n\nðŸ”— Connection Guide:\n"
            report += f"â€¢ Connect 'optimized_steps' â†’ KSampler 'steps'\n"
            report += f"â€¢ Connect 'optimized_cfg' â†’ KSampler 'cfg'\n"
            report += f"â€¢ Set KSampler sampler_name to: {sampler_name}\n"
            report += f"â€¢ Set KSampler scheduler to: {scheduler}\n"
            report += f"â€¢ Use these settings for optimal quality based on analysis!"
        else:
            report = f"ðŸ“Š No quality analysis provided - using base parameters:\n"
            report += f"â€¢ Steps: {steps}\nâ€¢ CFG: {cfg}\nâ€¢ Sampler: {sampler_name}\nâ€¢ Scheduler: {scheduler}\n\n"
            report += f"ðŸ’¡ Paste quality analysis output to get AI-optimized parameters!"
        
        # Track node processing
        brain_data.add_node_to_chain("PromptBrainParameterOptimizer")
        
        return (brain_data, steps, cfg, sampler_name, scheduler, report)


# Node mappings for ComfyUI registration
NODE_CLASS_MAPPINGS_BRAIN = {
    "BrainsXDEV_PromptBrainSource": BrainsXDEV_PromptBrainSource,
    "BrainsXDEV_PromptBrainLearnDirect": BrainsXDEV_PromptBrainLearnDirect,
    "BrainsXDEV_PromptBrainSuggestDirect": BrainsXDEV_PromptBrainSuggestDirect,
    "BrainsXDEV_PromptBrainPerformanceDirect": BrainsXDEV_PromptBrainPerformanceDirect,
    "BrainsXDEV_PromptBrainResetDirect": BrainsXDEV_PromptBrainResetDirect,
    "BrainsXDEV_PromptBrainKSamplerDirect": BrainsXDEV_PromptBrainKSamplerDirect,
    "BrainsXDEV_PromptBrainParameterOptimizer": BrainsXDEV_PromptBrainParameterOptimizer,
    "BrainsXDEV_PromptBrainQualityScore": BrainsXDEV_PromptBrainQualityScore,
}

NODE_DISPLAY_NAME_MAPPINGS_BRAIN = {
    "BrainsXDEV_PromptBrainSource": "Brains-XDEV • PromptBrain Source (BRAIN)",
    "BrainsXDEV_PromptBrainLearnDirect": "Brains-XDEV • PromptBrain Learn (BRAIN)",
    "BrainsXDEV_PromptBrainSuggestDirect": "Brains-XDEV • PromptBrain Suggest (BRAIN)",
    "BrainsXDEV_PromptBrainPerformanceDirect": "Brains-XDEV • PromptBrain Performance (BRAIN)",
    "BrainsXDEV_PromptBrainResetDirect": "Brains-XDEV • PromptBrain Reset (BRAIN)",
    "BrainsXDEV_PromptBrainKSamplerDirect": "Brains-XDEV • PromptBrain KSampler (AI-Optimized)",
    "BrainsXDEV_PromptBrainParameterOptimizer": "Brains-XDEV • PromptBrain Parameter Optimizer (AI)",
    "BrainsXDEV_PromptBrainQualityScore": "Brains-XDEV • PromptBrain Quality Score (AI)",
}

#!/usr/bin/env python3
"""
Brains-XDEV PromptBrain - BrainData Core Class

Shared data structure for all PromptBrain nodes.
Imported from Comfyui-DEV and adapted for Brains-XDEV architecture.

References:
- ComfyUI Custom Datatypes: https://docs.comfy.org/custom-nodes/backend/custom_datatypes
- PromptBrain Architecture: https://github.com/aiforhumans/Brains
"""

print("[Brains-XDEV] brain_data import")

import json
import time
from typing import Dict, Any, Optional, List, Tuple


class BrainData:
    """
    Custom BRAIN datatype for PromptBrain system.
    Allows direct data passing between nodes without file I/O.
    
    This class manages:
    - Tag learning and scoring
    - Co-occurrence tracking
    - Learning history
    - Style and feature categorization
    - Performance metadata
    """
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initialize brain data structure.
        
        Args:
            data: Optional existing data dictionary. If None, creates new empty brain.
        """
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
        """Get all tag data."""
        return self.data.get("tags", {})
    
    def get_cooccurrence(self) -> Dict[str, int]:
        """Get co-occurrence data."""
        return self.data.get("co", {})
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get learning history."""
        return self.data.get("history", [])
    
    def get_styles(self) -> Dict[str, Any]:
        """Get style definitions."""
        return self.data.get("styles", {})
    
    def get_features(self) -> Dict[str, Any]:
        """Get feature definitions."""
        return self.data.get("features", {})
    
    def _ensure_metadata_exists(self) -> None:
        """Ensure metadata structure exists and is complete."""
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
    
    def add_learning_event(
        self, 
        prompt: str, 
        score: float, 
        tags: List[str], 
        style_category: str = "none", 
        feature_emphasis: str = "none"
    ) -> None:
        """
        Add a learning event to the brain.
        
        Args:
            prompt: The prompt text that was used
            score: Quality score (0.0-1.0)
            tags: List of tags to learn from
            style_category: Style category (photorealistic, artistic, etc.)
            feature_emphasis: Feature emphasis (character, environment, etc.)
        """
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
    
    def get_suggestions(
        self, 
        base_tags: List[str], 
        style: str = "none", 
        feature: str = "none", 
        quality_threshold: float = 0.3
    ) -> List[str]:
        """
        Get tag suggestions based on current brain data.
        
        Args:
            base_tags: Tags to base suggestions on
            style: Target style category
            feature: Target feature emphasis
            quality_threshold: Minimum quality score for suggestions
            
        Returns:
            List of suggested tags
        """
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
        """
        Get performance statistics.
        
        Returns:
            Dictionary with performance metrics
        """
        return {
            "total_tags": len(self.data["tags"]),
            "total_cooccurrence": len(self.data["co"]),
            "total_history": len(self.data["history"]),
            "last_modified": self._last_modified,
            "node_chain": self._node_chain.copy(),
            "average_score": self._calculate_average_score()
        }
    
    def _calculate_average_score(self) -> float:
        """Calculate average score across all tags."""
        tags = self.data["tags"]
        if not tags:
            return 0.0
        
        total_score = sum(tag_data.get("score", 0.0) for tag_data in tags.values())
        return total_score / len(tags)
    
    def add_node_to_chain(self, node_name: str) -> None:
        """
        Track which nodes have processed this brain data.
        
        Args:
            node_name: Name of the node to add to chain
        """
        self._node_chain.append({
            "node": node_name,
            "timestamp": time.time()
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return self.data.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BrainData':
        """
        Create BrainData from dictionary.
        
        Args:
            data: Dictionary with brain data
            
        Returns:
            New BrainData instance
        """
        return cls(data)
    
    def __str__(self) -> str:
        """String representation."""
        stats = self.get_performance_stats()
        return f"BrainData(tags={stats['total_tags']}, history={stats['total_history']}, avg_score={stats['average_score']:.2f})"

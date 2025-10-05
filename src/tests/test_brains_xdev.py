"""
Tests for Brains-XDEV nodes

Basic unit tests to ensure node registration and functionality work correctly.
Migrated and adapted from BRAIN project.
"""
import pytest
import numpy as np
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import nodes for testing
from brightness_example import BrainsXDEV_Brightness
from promptbrain.memory import BrainsXDEV_MemoryWrite, BrainsXDEV_MemoryRead
from promptbrain.scorer import BrainsXDEV_Scorer
from promptbrain.tagger import BrainsXDEV_Tagger
from promptbrain.captioner import BrainsXDEV_Captioner
from promptbrain.suggester import BrainsXDEV_PromptSuggester


class TestNodeRegistration:
    """Test that all nodes have proper registration properties."""
    
    def test_brightness_registration(self):
        node = BrainsXDEV_Brightness()
        assert hasattr(node, 'run')
        assert isinstance(node.RETURN_TYPES, tuple)
        assert isinstance(node.INPUT_TYPES(), dict)
        assert hasattr(node, 'CATEGORY')
        assert "Brains-XDEV" in node.CATEGORY

    def test_memory_write_registration(self):
        node = BrainsXDEV_MemoryWrite()
        assert hasattr(node, 'run')
        assert isinstance(node.RETURN_TYPES, tuple)
        assert isinstance(node.INPUT_TYPES(), dict)

    def test_memory_read_registration(self):
        node = BrainsXDEV_MemoryRead()
        assert hasattr(node, 'run')
        assert isinstance(node.RETURN_TYPES, tuple)
        assert isinstance(node.INPUT_TYPES(), dict)


class TestBrightnessNode:
    """Test the brightness adjustment node."""
    
    def test_brightness_changes_stats(self):
        node = BrainsXDEV_Brightness()
        img = np.zeros((8, 8, 3), dtype=np.float32) + 0.5
        out, = node.run([img], strength=0.2)
        arr = out[0]
        
        assert arr.shape == img.shape
        # Mean should increase but remain <= 1.0
        assert arr.mean() > img.mean()
        assert arr.max() <= 1.0 + 1e-6
    
    def test_brightness_negative_strength(self):
        node = BrainsXDEV_Brightness()
        img = np.ones((4, 4, 3), dtype=np.float32) * 0.8
        out, = node.run([img], strength=-0.3)
        arr = out[0]
        
        assert arr.shape == img.shape
        # Mean should decrease but remain >= 0.0
        assert arr.mean() < img.mean()
        assert arr.min() >= 0.0
    
    def test_brightness_batch_input(self):
        node = BrainsXDEV_Brightness()
        img1 = np.zeros((4, 4, 3), dtype=np.float32) + 0.3
        img2 = np.zeros((4, 4, 3), dtype=np.float32) + 0.7
        out, = node.run([img1, img2], strength=0.1)
        
        assert len(out) == 2
        assert out[0].shape == img1.shape
        assert out[1].shape == img2.shape


class TestMemoryNodes:
    """Test the memory storage and retrieval nodes."""
    
    def test_memory_write_basic(self):
        node = BrainsXDEV_MemoryWrite()
        tags_dict = {"tags": {"test": 0.9, "example": 0.7}}
        status, = node.run(tags_dict, "test caption", 0.8, "test context")
        
        assert isinstance(status, str)
        assert "ok:memory_write" in status
    
    def test_memory_read_basic(self):
        node = BrainsXDEV_MemoryRead()
        captions, raw = node.run(top_k=5, min_score=0.0)
        
        assert isinstance(captions, list)
        assert isinstance(raw, dict)
        assert "rows" in raw


class TestStubNodes:
    """Test the stub nodes return expected formats."""
    
    def test_tagger_stub(self):
        node = BrainsXDEV_Tagger()
        img = np.zeros((32, 32, 3), dtype=np.float32)
        tags_text, tags_dict = node.run([img], min_conf=0.5, allow_list="", deny_list="")
        
        assert isinstance(tags_text, str)
        assert isinstance(tags_dict, dict)
        assert "tags" in tags_dict
        assert "stub" in tags_dict
    
    def test_captioner_stub(self):
        node = BrainsXDEV_Captioner()
        img = np.zeros((32, 32, 3), dtype=np.float32)
        caption, metadata = node.run([img], model_hint="mock")
        
        assert isinstance(caption, str)
        assert isinstance(metadata, dict)
        assert "stub" in metadata
    
    def test_scorer_basic(self):
        node = BrainsXDEV_Scorer()
        score, notes = node.run(score=0.75, notes="test note")
        
        assert isinstance(score, float)
        assert score == 0.75
        assert isinstance(notes, str)
        assert notes == "test note"


class TestPromptSuggester:
    """Test the prompt suggestion functionality."""
    
    def test_suggester_basic(self):
        node = BrainsXDEV_PromptSuggester()
        tags_dict = {"tags": {"girl": 0.9, "solo": 0.8, "simple": 0.6}}
        captions = ["A nice image", "Good quality"]
        
        positive, negative, metadata = node.run(
            tags_dict, captions, max_terms=10, 
            negatives="low quality", quality_prefix="masterpiece, "
        )
        
        assert isinstance(positive, str)
        assert isinstance(negative, str)
        assert isinstance(metadata, dict)
        assert "masterpiece" in positive
        assert "girl" in positive or "solo" in positive
    
    def test_suggester_empty_inputs(self):
        node = BrainsXDEV_PromptSuggester()
        positive, negative, metadata = node.run({}, [], max_terms=10)
        
        assert isinstance(positive, str)
        assert len(positive) > 0  # Should provide fallback
        assert isinstance(metadata, dict)


if __name__ == "__main__":
    pytest.main([__file__])
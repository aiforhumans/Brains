import numpy as np
from my_nodes.basic_example import XDEV_Brightness

def test_registration_shapes():
    node = XDEV_Brightness()
    assert hasattr(node, 'run')
    assert isinstance(node.RETURN_TYPES, tuple)

def test_brightness_changes_stats():
    node = XDEV_Brightness()
    img = np.zeros((8,8,3), dtype=np.float32) + 0.5
    out, = node.run([img], strength=0.2)
    arr = out[0]
    assert arr.shape == img.shape
    # mean should increase but remain <= 1.0
    assert arr.mean() > img.mean()
    assert arr.max() <= 1.0 + 1e-6

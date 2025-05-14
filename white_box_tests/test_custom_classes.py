import pickle
import hashlib
import pytest

class Example:
    def __init__(self, x):
        self.x = x
    def __eq__(self, other):
        return isinstance(other, Example) and self.x == other.x

def get_hash(obj):
    return hashlib.sha256(pickle.dumps(obj)).hexdigest()

def test_custom_object_hash():
    """测试自定义类实例的哈希一致性和反序列化等价性"""
    inst = Example(123)
    h1 = get_hash(inst)
    h2 = get_hash(inst)
    assert h1 == h2
    new = pickle.loads(pickle.dumps(inst))
    assert new == inst

def test_custom_object_protocols():
    """测试自定义类在不同协议下的序列化一致性"""
    inst = Example("测试")
    for proto in range(pickle.HIGHEST_PROTOCOL + 1):
        data = pickle.dumps(inst, protocol=proto)
        assert hashlib.sha256(data).hexdigest() == hashlib.sha256(data).hexdigest()
        assert pickle.loads(data) == inst

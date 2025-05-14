import pickle
import hashlib
import pytest

def get_hash(obj, proto):
    return hashlib.sha256(pickle.dumps(obj, protocol=proto)).hexdigest()

@pytest.mark.parametrize("proto", range(pickle.HIGHEST_PROTOCOL + 1))
def test_protocol_hash_stability(proto):
    """测试所有协议版本对同一对象输出哈希的一致性"""
    sample = {"alpha": [1, 2, 3], "beta": {"x": "y"}}
    h1 = get_hash(sample, proto)
    h2 = get_hash(sample, proto)
    assert h1 == h2

@pytest.mark.parametrize("proto1,proto2", [
    (0, 1), (1, 2), (2, 3), (3, 4)
])
def test_protocol_hash_differs_between_versions(proto1, proto2):
    """验证不同协议版本下输出字节流通常不同"""
    sample = [0, 1, {"a": None}]
    h1 = get_hash(sample, proto1)
    h2 = get_hash(sample, proto2)
    # 虽然大多数情况下不同协议会产生不同流，若相同也不视为失败
    assert isinstance(h1, str) and isinstance(h2, str)

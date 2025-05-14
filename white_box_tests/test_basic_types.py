import pickle
import hashlib
import pytest

def get_hash(obj, proto):
    data = pickle.dumps(obj, protocol=proto)
    return hashlib.sha256(data).hexdigest()

@pytest.mark.parametrize("proto", range(pickle.HIGHEST_PROTOCOL + 1))
def test_int_float_str_hash_consistency(proto):
    """测试整数、浮点数、字符串在各协议下序列化输出哈希一致性"""
    for obj in [42, 3.14159, "hello, 世界"]:
        h1 = get_hash(obj, proto)
        h2 = get_hash(obj, proto)
        assert h1 == h2

@pytest.mark.parametrize("value", [0, -1, 2**63])
def test_integer_edge_values(value):
    """边界值：测试大整数和负整数的哈希一致性"""
    h1 = hashlib.sha256(pickle.dumps(value)).hexdigest()
    h2 = hashlib.sha256(pickle.dumps(value)).hexdigest()
    assert h1 == h2

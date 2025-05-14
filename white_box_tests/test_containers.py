import pickle
import hashlib
import pytest

def get_hash(obj):
    return hashlib.sha256(pickle.dumps(obj)).hexdigest()

@pytest.mark.parametrize("lst", [
    [], [1, 2, 3], ["a", ["nested", []]]
])
def test_list_hash(lst):
    """测试列表及嵌套列表的一致性"""
    assert get_hash(lst) == get_hash(lst)

@pytest.mark.parametrize("dct", [
    {}, {"x": 1, "y": [1, 2]}, {"nested": {"a": {"b": 2}}}
])
def test_dict_hash(dct):
    """测试字典及嵌套字典的一致性"""
    assert get_hash(dct) == get_hash(dct)

@pytest.mark.parametrize("tup", [
    (), (1,), (1, 2, (3, 4))
])
def test_tuple_hash(tup):
    """测试元组及嵌套元组的一致性"""
    assert get_hash(tup) == get_hash(tup)

import pickle
import hashlib
import pytest

def get_hash(obj):
    return hashlib.sha256(pickle.dumps(obj)).hexdigest()

def test_self_referential_list():
    """测试自引用列表的序列化一致性"""
    lst = [1, 2, 3]
    lst.append(lst)
    h1 = get_hash(lst)
    h2 = get_hash(lst)
    assert h1 == h2
    new = pickle.loads(pickle.dumps(lst))
    assert new[-1] is new  # 反序列化后仍自引用

def test_shared_subobject():
    """测试多个引用同一子对象时的处理"""
    shared = {"key": "value"}
    obj = [shared, shared]
    h1 = get_hash(obj)
    h2 = get_hash(obj)
    assert h1 == h2
    new = pickle.loads(pickle.dumps(obj))
    assert new[0] is new[1]

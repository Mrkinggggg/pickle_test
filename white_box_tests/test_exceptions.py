import pickle
import pytest

class Unserializable:
    def __init__(self):
        self.fp = open(__file__, 'rb')  # 文件句柄不可序列化

def test_pickling_error_for_unserializable():
    """测试对不可序列化对象抛 PicklingError"""
    obj = Unserializable()
    with pytest.raises(pickle.PicklingError):
        pickle.dumps(obj)

def test_unpickling_error_for_corrupted_data():
    """测试对损坏字节流抛 UnpicklingError"""
    bad = b'not a valid pickle'
    with pytest.raises(pickle.UnpicklingError):
        pickle.loads(bad)

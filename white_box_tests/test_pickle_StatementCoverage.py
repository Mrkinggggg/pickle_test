import pytest
import hashlib
import builtins
import importlib.util
import os
import sys
import decimal

# 在模块级别定义一个可测试的自定义类，以便 pickle 可以按名称导入它
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

# 模拟缺少 _pickle 模块，确保使用 my_pickle 中的 Python 实现（而非 C 实现）
orig_import = builtins.__import__
def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == '_pickle':
        raise ImportError("simulate missing _pickle")
    return orig_import(name, globals, locals, fromlist, level)
builtins.__import__ = fake_import

# 从文件位置加载 my_pickle 模块
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("my_pickle", os.path.join(here, "my_pickle.py"))
my_pickle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_pickle)

# 恢复原始导入函数
builtins.__import__ = orig_import

def test_primitives_and_bytearray():
    cases = [42, 3.14, True, False, "hello", b"bytes", bytearray(b"abc")]
    for obj in cases:
        data = my_pickle.dumps(obj)
        result = my_pickle.loads(data)
        if isinstance(obj, bytearray):
            assert isinstance(result, bytearray)
        assert result == obj

def test_containers_and_none_empty():
    cases = [
        [1, 2, 3],
        (4, 5, 6),
        {1, 2, 3},
        {"a": 1, "b": 2},
        None,
        [],
        (),
        {},
        ""
    ]
    for obj in cases:
        data = my_pickle.dumps(obj)
        result = my_pickle.loads(data)
        assert result == obj

def test_nested_structures_and_stable_hash():
    obj = [{"key": [1, 2]}, (3, {"inner": 4}), None]
    data = my_pickle.dumps(obj)
    result = my_pickle.loads(data)
    assert result == obj
    # 稳定序列化：两次 dumps 应产生相同的字节
    data2 = my_pickle.dumps(obj)
    assert hashlib.sha256(data).hexdigest() == hashlib.sha256(data2).hexdigest()

def test_custom_class_roundtrip():
    pt = Point(5, 7)
    data = my_pickle.dumps(pt)
    result = my_pickle.loads(data)
    assert isinstance(result, Point)
    assert result == pt

def test_dump_and_load_with_file(tmp_path):
    obj = {"x": [1, 2, 3], "y": (4, 5)}
    file_path = tmp_path / "test.pkl"
    with open(file_path, 'wb') as f:
        my_pickle.dump(obj, f)
    with open(file_path, 'rb') as f:
        loaded = my_pickle.load(f)
    assert loaded == obj

def test_recursive_list_and_dict():
    lst = []
    lst.append(lst)
    data = my_pickle.dumps(lst)
    result = my_pickle.loads(data)
    assert isinstance(result, list)
    assert result[0] is result

    d = {}
    d['self'] = d
    data = my_pickle.dumps(d)
    result = my_pickle.loads(data)
    assert isinstance(result, dict)
    assert result['self'] is result

def test_loads_type_error():
    with pytest.raises(TypeError):
        my_pickle.loads("this is a str, not bytes")

def test_protocol_and_buffer_callback():
    # protocol < 0 时使用 HIGHEST_PROTOCOL，不应报错
    data = my_pickle.dumps([1, 2, 3], protocol=-1)
    result = my_pickle.loads(data)
    assert result == [1, 2, 3]
    # protocol > HIGHEST_PROTOCOL 应抛出 ValueError
    with pytest.raises(ValueError):
        my_pickle.dumps([1, 2], protocol=my_pickle.HIGHEST_PROTOCOL+1)
    # 在 protocol < 5 时传入 buffer_callback 应报错
    with pytest.raises(ValueError):
        my_pickle.dumps([1, 2, 3], buffer_callback=lambda b: True)
    # protocol=5 时使用 buffer_callback 是允许的
    data = my_pickle.dumps([7, 8], protocol=5, buffer_callback=lambda b: b"")
    assert my_pickle.loads(data) == [7, 8]

def test_type_error_on_invalid_file():
    class NoWrite:
        pass
    with pytest.raises(TypeError):
        my_pickle.dump(123, NoWrite())

# 在模块级别定义额外的测试类（确保反序列化时可导入）
class SlottedClass:
    __slots__ = ['a', 'b']
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __eq__(self, other):
        return isinstance(other, SlottedClass) and self.a == other.a and self.b == other.b

class ParentClass:
    def __init__(self, x):
        self.x = x
    def __eq__(self, other):
        return isinstance(other, ParentClass) and self.x == other.x

class ChildClass(ParentClass):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y
    def __eq__(self, other):
        return super().__eq__(other) and self.y == other.y

class CustomStateClass:
    def __init__(self, name):
        self.name = name
    def __getstate__(self):
        return {"name": self.name.upper()}
    def __setstate__(self, state):
        self.name = state["name"].lower()
    def __eq__(self, other):
        return isinstance(other, CustomStateClass) and self.name == other.name

# 测试复杂数据类型
def test_complex_data_types():
    cases = [
        frozenset([1, 2, 3]),
        complex(3, 4),
        decimal.Decimal("3.141592653589793238462643383279"),
    ]
    for obj in cases:
        data = my_pickle.dumps(obj)
        result = my_pickle.loads(data)
        assert result == obj
        # 类型检查（例如 complex 反序列化后类型是否正确）
        assert type(result) is type(obj)

def test_slotted_class():
    obj = SlottedClass(5, "test")
    data = my_pickle.dumps(obj)
    result = my_pickle.loads(data)
    assert result == obj
    # 检查 __slots__ 属性是否保留
    assert isinstance(result, SlottedClass)
    assert not hasattr(result, '__dict__')

def test_inheritance_and_dynamic_class():
    # 测试继承类
    child = ChildClass(10, 20)
    data = my_pickle.dumps(child)
    result = my_pickle.loads(data)
    assert result == child

    # 测试动态生成的类（绑定到当前模块）
    DynamicClass = type('DynamicClass', (), {'value': 100})
    # 将动态类绑定到当前模块的命名空间
    sys.modules[__name__].DynamicClass = DynamicClass
    dyn_obj = DynamicClass()

    data = my_pickle.dumps(dyn_obj)
    result = my_pickle.loads(data)
    assert type(result).__name__ == 'DynamicClass'
    assert result.value == 100

def test_custom_state_methods():
    obj = CustomStateClass("Alice")
    data = my_pickle.dumps(obj)
    result = my_pickle.loads(data)
    # __getstate__ 应存储大写，__setstate__ 会转为小写
    assert result.name == "alice"
    assert obj.name == "Alice"  # 确保原始对象未被修改

def test_module_and_function_objects():
    # 模块对象不可序列化，应抛出错误
    with pytest.raises((my_pickle.PicklingError, TypeError)):
        my_pickle.dumps(sys)

    # 函数对象（如 lambda）不可序列化，应抛出 PicklingError
    with pytest.raises(my_pickle.PicklingError):
        my_pickle.dumps(lambda x: x + 1)

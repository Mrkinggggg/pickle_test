import io
import hashlib
import pytest

import my_pickle as pickle

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

# 1. 基础类型 round-trip & 稳定性
@pytest.mark.parametrize("obj", [
    None,
    True,
    False,
    0,
    123,
    -2**65,         # 大整数
    3.14159,
    "",
    "短字符串",
    "长字符串" * 100,  # 长 Unicode
    b"",
    b"bytes\x00\xff",
    bytearray(),
    bytearray(b"\x01\x02\x03"),
])
def test_dumps_loads_roundtrip_and_stability(obj):
    # 多次 dumps，保证一致
    data1 = pickle.dumps(obj)
    data2 = pickle.dumps(obj)
    assert data1 == data2
    assert sha256(data1) == sha256(data2)
    # loads 能正确还原
    res = pickle.loads(data1)
    assert res == obj

# 2. 文件接口 dump/load
@pytest.mark.parametrize("obj", [
    [1, 2, 3],
    (4, 5, 6),
    (7, 8, 9, 10),  # tuple >3 元素
    {"a": 1, "b": 2},
    {1, 2, 3},
    frozenset([4, 5, 6]),
    [{"nested": (1,2,3)}, 42],
])
def test_dump_load_fileobj(obj):
    buf1 = io.BytesIO()
    buf2 = io.BytesIO()
    pickle.dump(obj, buf1)
    pickle.dump(obj, buf2)
    b1 = buf1.getvalue(); b2 = buf2.getvalue()
    # 稳定性
    assert b1 == b2
    # load 正确
    buf1.seek(0)
    out = pickle.load(buf1)
    assert out == obj

# 3. encode_long/decode_long 覆盖
from my_pickle import encode_long, decode_long
@pytest.mark.parametrize("n", [0, 127, 128, 255, 256, -1, -128, -256, 2**200])
def test_encode_decode_long(n):
    enc = encode_long(n)
    assert decode_long(enc) == n

# 4. 容器分支：空 vs 非空 list/dict/set/frozenset
def test_empty_containers():
    for obj in ([], {}, set(), frozenset()):
        data = pickle.dumps(obj)
        assert pickle.loads(data) == obj

# 5. 递归结构
def test_recursive_tuple():
    t = (1, 2)
    # 制造递归
    t = (t, )
    buf = io.BytesIO()
    pickle.dump(t, buf)
    buf.seek(0)
    out = pickle.load(buf)
    # 结构和值相同，但不必是同一对象
    assert isinstance(out, tuple)
    assert out[0][0] == 1

# 6. 错误分支：loads 接受 unicode
def test_loads_type_error():
    with pytest.raises(TypeError):
        pickle.loads("not bytes")

# 7. 错误分支：buffer_callback 与 protocol <5 不兼容
def test_buffer_callback_error():
    class Dummy: pass
    with pytest.raises(ValueError):
        pickle.dumps(42, protocol=4, buffer_callback=lambda b: True)

# 8. 错误分支：dump 接受无 write 属性
def test_dump_bad_fileobj():
    class NoWrite:
        pass
    with pytest.raises(TypeError):
        pickle.dump(123, NoWrite())

# 9. protocol 边界：非法 protocol
def test_invalid_protocol():
    with pytest.raises(ValueError):
        pickle.dumps(1, protocol=999)

if __name__ == "__main__":
    # 直接用 pytest 运行
    pytest.main(["-q", "--disable-warnings", "--maxfail=1"])
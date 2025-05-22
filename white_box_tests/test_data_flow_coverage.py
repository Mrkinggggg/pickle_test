import sys
import hashlib
import pytest
import platform
from pathlib import Path
import my_pickle as pickle




def save_test_result(func_name, obj, protocol, hash):
    """
    保存测试结果，包括函数名、对象、协议和哈希值。
    在终端中输出
    """
    # 将结果输出到终端
    print(f"Function: {func_name}, Object: {obj!r}, Protocol: {protocol}, Hash: {hash}")

@pytest.mark.parametrize("protocol", range(0, 6))
@pytest.mark.parametrize("func", ["dump", "dumps", "load", "loads"])
def test_pickle_io_with_data_flow_coverage(tmp_path, protocol, func):
    """
    测试 pickle.dump、pickle.dumps、pickle.load 和 pickle.loads 在协议 0-5 之间的表现。
    包含 All-Defs 和 All-Uses 覆盖，确保每个变量定义和使用都被完全覆盖。
    """
    obj = {"a": 1, "b": [2, 3], "c": "text"}  # 定义对象 obj，将被序列化和反序列化
    file_path = tmp_path / "test.obj"  # 定义文件路径，用于保存序列化数据

    # 序列化：覆盖数据流定义
    if func == "dump":
        with open(file_path, "wb") as f:
            pickle.dump(obj, f, protocol=protocol)  # 定义了 obj 并使用了 file_path
        data = file_path.read_bytes()  # 使用 file_path 来获取序列化后的数据

    elif func == "dumps":
        data = pickle.dumps(obj, protocol=protocol)  # obj 被序列化
        file_path.write_bytes(data)  # 使用 file_path 写入数据

    else:
        # 对于 load/loads，先用 dumps 生成数据
        data = pickle.dumps(obj, protocol=protocol)  # obj 被使用并序列化
        file_path.write_bytes(data)  # 使用 file_path 来存储数据

    hash_ser = hashlib.sha256(data).hexdigest()  # 使用 data 来计算哈希
    save_test_result(func, obj, protocol, hash_ser)  # 输出测试结果到终端

    # 反序列化：确保 obj_back 被正确恢复
    if func == "load":
        with open(file_path, "rb") as f:
            obj_back = pickle.load(f)  # 使用了 file_path 来恢复对象
    elif func == "loads":
        obj_back = pickle.loads(data)  # 使用 data 来恢复对象
    else:
        with open(file_path, "rb") as f:
            obj_back = pickle.load(f)  # 再次使用 file_path 来恢复对象

    # 验证一致性：确保反序列化后的 obj_back 与原始 obj 相同
    assert obj_back == obj  # obj_back 应该和 obj 相等，验证了变量的使用
    assert isinstance(data, (bytes, bytearray)) or func in ("dump", "load")  # 确保序列化数据是字节类型


@pytest.mark.parametrize("protocol", range(0, 6))
def test_dump_all_uses(tmp_path, protocol):
    """针对 pickle.dump 的 all-use 覆盖测试。所有结果通过终端输出。"""
    obj = [1, 2, 3]  # 定义 obj，将被序列化
    file_path = tmp_path / f"dump_proto{protocol}.pkl"  # 定义文件路径

    with open(file_path, 'wb') as f:
        pickle.dump(obj, f, protocol=protocol)  # 使用了 obj
        f.flush()

    data = file_path.read_bytes()  # 使用 file_path 获取序列化数据
    assert isinstance(data, bytes)

    hash_ser = hashlib.sha256(data).hexdigest()  # 使用 data 计算哈希值
    save_test_result('dump', obj, protocol, hash_ser)  # 输出测试结果到终端


@pytest.mark.parametrize("protocol", range(0, 6))
def test_dumps_all_uses(tmp_path, protocol):
    """针对 pickle.dumps 的 all-use 覆盖测试。所有结果通过终端输出。"""
    obj = {'x': 1, 'y': 2}  # 定义 obj，将被序列化
    data = pickle.dumps(obj, protocol=protocol)  # 使用 obj 进行序列化
    assert isinstance(data, (bytes, bytearray))

    tmp_file = tmp_path / f"dumps_proto{protocol}.bin"  # 定义文件路径
    tmp_file.write_bytes(data)  # 使用 tmp_file 写入数据
    assert tmp_file.exists()

    hash_ser = hashlib.sha256(data).hexdigest()  # 使用 data 计算哈希值
    save_test_result('dumps', obj, protocol, hash_ser)  # 输出测试结果到终端


@pytest.mark.parametrize("protocol", range(0, 6))
def test_load_all_uses(tmp_path, protocol):
    """针对 pickle.load 的 all-use 覆盖测试。所有结果通过终端输出。"""
    original = (1, 2, 3)  # 定义 original 对象，将被序列化
    ser = pickle.dumps(original, protocol=protocol)  # 使用 original 进行序列化
    file_path = tmp_path / f"load_proto{protocol}.pkl"  # 定义文件路径
    with open(file_path, 'wb') as f:
        f.write(ser)

    with open(file_path, 'rb') as f:
        obj_back = pickle.load(f)  # 使用 file_path 恢复对象
        assert f.read() == b''  # 确保没有额外数据

    assert obj_back == original  # 验证反序列化后的对象是否一致

    hash_ser = hashlib.sha256(ser).hexdigest()  # 使用序列化数据计算哈希值
    save_test_result('load', original, protocol, hash_ser)  # 输出测试结果到终端


@pytest.mark.parametrize("protocol", range(0, 6))
def test_loads_all_uses(tmp_path, protocol):
    """针对 pickle.loads 的 all-use 覆盖测试。所有结果通过终端输出。"""
    original = 'pytest'  # 定义 original 对象，将被序列化
    ser = pickle.dumps(original, protocol=protocol)  # 使用 original 进行序列化
    obj_back = pickle.loads(ser)  # 使用序列化数据恢复对象
    assert obj_back == original  # 验证反序列化后的对象是否一致
    assert len(ser) > 0  # 验证序列化数据不为空

    hash_ser = hashlib.sha256(ser).hexdigest()  # 使用序列化数据计算哈希值
    save_test_result('loads', original, protocol, hash_ser)  # 输出测试结果到终端

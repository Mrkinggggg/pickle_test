# 先pip install pytest
import hashlib
import pickle
import multiprocessing
import os
import pytest

# 测试用例
test_cases = [
    # 基本数据类型（稳定类）
    ("Integer", 42),
    ("Negative Integer", -100),
    ("Large Integer", 10 ** 18),
    ("Float", 3.141592653589793),
    ("Scientific Notation Float", 1.23e-4),
    ("ASCII String", "hello"),
    ("Unicode String", "中文测试"),
    ("Boolean True", True),
    ("Boolean False", False),
    ("None", None),
    ("Bytes", b"\x01\x02\x03\xff"),
    ("Bytearray", bytearray(b"test")),

    # 有序容器（稳定类）
    ("Empty List", []),
    ("Simple List", [1, 2, 3]),
    ("Mixed Type List", [1, "a", 3.14, True]),
    ("Empty Tuple", tuple()),
    ("Simple Tuple", (1, 2, 3)),
    ("Single Element Tuple", (42,)),

    # 无序容器（需验证稳定性）
    ("Empty Set", set()),
    ("Simple Set With Ordered Elements", {'apple', 'banana', 'pear'}),
    ("Simple Set With Disordered Elements", {'banana', 'apple', 'pear'}),
    ("Mixed Type Set", {"a", 1, 3.14}),
    ("Empty Dict", {}),
    ("Simple Dict", {"a": 1, "b": 2}),
    ("Nested Keys Dict", {("a", "b"): 1}),

    # 嵌套结构（复杂类）
    ("Nested Dict-Set", {"set": {1, 2}, "list": [3, 4]}),
    ("Nested List-Dict", [{"a": 1}, {"b": 2}]),
    ("Nested List", [[1, [2]], [3, [4]]]),
    ("Nested Dict", {"outer": {"inner": {"key": "value"}}}),
    ("Mixed Nesting", {"list": [1, {"set": {2, 3}}]}),

    # Python内置对象
    ("Complex Number", complex(1, 2)),
    ("Range Object", range(10)),
    ("Frozenset", frozenset([1, 2, 3])),

    # 边界/异常类
    ("Empty Set", set()),
    ("Empty Dict", {}),
    ("Empty List", []),

    # 递归引用（稍后动态生成）
    ("Self-Referencing List", None),
    ("Mutual Reference", None),

    # 恶意构造数据
    ("Corrupted Pickle Data", b"corrupted_pickle_data"),
    ("Protocol Mismatch", b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x05hello\x94."),

    # 超大对象
    ("Large Binary", b"\x00" * (10 ** 5)),  # 减小大小以便更快测试
    ("Deeply Nested", None),

    # # os路径,在不同操作系统pickle的结果是不一样的
    ("Path", os.path.join("home", "study", "python")),
    ("Path in windows", r"home\study\python"),
    ("Path in Mac", r"home/study/python"),
]


def setup_dynamic_cases():
    # 自引用列表
    self_ref_list = []
    self_ref_list.append(self_ref_list)
    test_cases[36] = ("Self-Referencing List", self_ref_list)

    # 相互引用对象
    obj_a = {}
    obj_b = {"ref": obj_a}
    obj_a["ref"] = obj_b
    test_cases[37] = ("Mutual Reference", obj_a)

    # 深度嵌套结构
    deep_nested = []
    current = deep_nested
    for _ in range(100):  # 减少深度以便更快测试
        new_level = [current]
        current = new_level
    test_cases[41] = ("Deeply Nested", current)


def hash_pickle(data):
    pickled_data = pickle.dumps(data)
    return hashlib.sha256(pickled_data).hexdigest()


def run_single_test_case(name, data):
    manager = multiprocessing.Manager()
    results = manager.dict()
    unstable_flag = manager.dict()

    # 先运行基准测试
    worker(name, data, 0, results, unstable_flag)

    # 运行多次测试
    processes = []
    for run_id in range(1, 5):  # 运行4次比较
        p = multiprocessing.Process(
            target=worker, args=(name, data, run_id, results, unstable_flag)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    return not unstable_flag.get(name, False)


def worker(name, data, run_id, results, unstable_flag):
    try:
        hash_val = hash_pickle(data)

        if run_id == 0:
            results[name] = hash_val
            print(f"[{name} Run{run_id}] ✅ Baseline Hash: {hash_val[:8]}")
        else:
            baseline = results.get(name)
            if baseline is None:
                print(f"[{name} Run{run_id}] ⚠️ Baseline not ready.")
                return

            if hash_val != baseline:
                unstable_flag[name] = True
                print(f"[{name} Run{run_id}] ❌ MISMATCH! Got {hash_val[:8]}, expected {baseline[:8]}")
            else:
                print(f"[{name} Run{run_id}] ✅ Match: {hash_val[:8]}")
    except Exception as e:
        unstable_flag[name] = True
        print(f"[{name} Run{run_id}] ❌ Exception: {e}")


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    setup_dynamic_cases()


@pytest.mark.parametrize("name,data", test_cases)
def test_pickle_stability(name, data):
    """测试pickle在不同进程中的稳定性"""
    is_stable = run_single_test_case(name, data)
    assert is_stable, f"Pickle of {name} is not stable across processes"
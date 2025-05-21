# 直接运行
import hashlib
import pickle
import multiprocessing
import sys
import os

# 测试用例,通过等价类划分获得
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

    # 递归引用（先运行setup_dynamic_cases()来动态生成）
    ("Self-Referencing List", None),
    ("Mutual Reference", None),

    # 恶意构造数据
    ("Corrupted Pickle Data", b"corrupted_pickle_data"),
    ("Protocol Mismatch", b"\x80\x04\x95\x0b\x00\x00\x00\x00\x00\x00\x00\x8c\x05hello\x94."),

    # 超大对象
    ("Large Binary", b"\x00" * (10 ** 7)),
    ("Deeply Nested", None),

    # os路径,在不同操作系统pickle的结果是不一样的
    ("Path",os.path.join("home", "study", "python")),
    ("Path in windows",r"home\study\python"),
    ("Path in Mac",r"home/study/python"),

    # 以下对象无法pickle 会报错,先作注释处理
    # # 自定义对象
    # ("Custom Object", lambda: object()),

    # # 不可序列化对象
    # ("File Object", open(__file__, 'r')),
    # ("Socket Object", None),
    # ("Generator", (x for x in range(3)))
]

def setup_dynamic_cases():
    self_ref_list = []
    self_ref_list.append(self_ref_list)
    test_cases[36] = ("Self-Referencing List", self_ref_list)

    obj_a = {}
    obj_b = {"ref": obj_a}
    obj_a["ref"] = obj_b
    test_cases[37] = ("Mutual Reference", obj_a)

    deep_nested = []
    current = deep_nested
    for _ in range(1000):
        new_level = [current]
        current = new_level
    test_cases[41] = ("Deeply Nested", current)

def hash_pickle(data):
    pickled_data = pickle.dumps(data)
    return hashlib.sha256(pickled_data).hexdigest()

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

def run_stability_tests():
    manager = multiprocessing.Manager()
    results = manager.dict()
    unstable_flag = manager.dict()

    for name, data in test_cases:
        print(f"\n=== Testing: {name} ===")

        # 先运行第一个子进程并将其结果作为基准，后续的结果均与此进行比对
        p0 = multiprocessing.Process(
            target=worker, args=(name, data, 0, results, unstable_flag)
        )
        p0.start()
        p0.join()

        processes = []
        for run_id in range(1, 5):
            p = multiprocessing.Process(
                target=worker, args=(name, data, run_id, results, unstable_flag)
            )
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        if unstable_flag.get(name):
            print(f"⚠️  Result: {name} is NOT stable across processes.\n")
        else:
            print(f"✅  Result: {name} is stable.\n")


if __name__ == "__main__":
    setup_dynamic_cases()
    run_stability_tests()


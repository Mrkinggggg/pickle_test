# Pickle Test Suite 🥒

![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
[![Code Style: PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen)](https://www.python.org/dev/peps/pep-0008/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/your_username/pickle_test) <!-- 请将 your_username 替换为您的 GitHub 用户名 -->

A comprehensive test suite designed to evaluate the stability and correctness of Python's `pickle` module. 
**Primary Objective**: To verify that identical inputs consistently produce hash-identical serialized outputs, ensuring the reliability of the pickling process across different scenarios and Python versions.

---

## Table of Contents 📖
- [Features](#features-✨)
- [Project Structure](#project-structure-📂)
- [Installation](#installation-🛠️)
- [Usage](#usage-🚀)
  - [Running Black-Box Tests](#running-black-box-tests)
  - [Running White-Box Tests](#running-white-box-tests)
- [Test Strategies](#test-strategies-🧪)
  - [Black-Box Testing](#black-box-testing)
  - [White-Box Testing](#white-box-testing)
- [Contributing](#contributing-🤝)
- [License](#license-📄)
- [中文说明](#中文说明-🇨🇳)

---

## Features ✨
- **Stability Testing**: Ensures that pickling the same object multiple times or across different processes yields identical byte streams.
- **Correctness Testing**: Verifies that objects are correctly serialized and deserialized, maintaining their state and type.
- **Cross-Protocol Validation**: Tests pickling behavior across all supported pickle protocols (0 through 5).
- **Comprehensive Test Cases**: Covers a wide range of data types, including primitives, containers, nested structures, custom classes, and edge cases.
- **Black-Box and White-Box Approaches**: Employs both functional (black-box) and structural (white-box) testing methodologies for thorough validation.
- **PEP8 Compliance**: Code adheres to Python style guidelines for readability and maintainability.

---

## Project Structure 📂

```
pickle_test/
├── black_box_test/               # Tests for pickle stability and correctness from a user perspective
│   ├── pickle_test_stable.py     # Script for direct execution to test stability with various data types
│   ├── test_pickle_stability.py  # Pytest-based stability tests, runnable with pytest
│   └── black_box_tests.py        # (Legacy/Experimental) Initial black-box test ideas
├── white_box_tests/              # Tests focusing on the internal implementation of pickle
│   ├── my_pickle.py              # A local copy/version of the pickle module for testing purposes
│   ├── test_data_flow_coverage.py # Tests aiming for data-flow coverage (all-defs, all-uses)
│   └── test_pickle_StatementCoverage.py # Tests aiming for statement coverage
├── .gitignore
├── LICENSE
└── README.md
```

---

## Installation 🛠️

### Prerequisites
- Python 3.7+
- `pip` and `venv` (recommended for managing dependencies)

### Steps
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Mrkinggggg/pickle_test.git 
    cd pickle_test
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate    # On Windows
    ```

3.  **Install dependencies**:
    The primary dependency for running tests is `pytest`. 
    ```bash
    pip install pytest
    ```

---

## Usage 🚀

Tests are organized into black-box and white-box categories.

### Running Black-Box Tests

These tests verify the `pickle` module's external behavior without prying into its internal workings.

1.  **Stability Tests (Direct Execution)**:
    The `pickle_test_stable.py` script can be run directly to observe stability across multiple processes for various data types. It prints results to the console.
    ```bash
    python black_box_test/pickle_test_stable.py
    ```

2.  **Stability Tests (Pytest)**:
    The `test_pickle_stability.py` script uses `pytest` to perform similar stability checks.
    Navigate to the `black_box_test` directory or run from the project root:
    ```bash
    pytest black_box_test/test_pickle_stability.py
    ```

### Running White-Box Tests

These tests examine the internal logic of the `my_pickle.py` (a copy of the standard `pickle` module for isolated testing).

1.  **Statement Coverage Tests**:
    These tests aim to execute every statement in `my_pickle.py`.
    ```bash
    pytest white_box_tests/test_pickle_StatementCoverage.py
    ```

2.  **Data-Flow Coverage Tests**:
    These tests aim to cover definitions and uses of variables within `my_pickle.py`.
    ```bash
    pytest white_box_tests/test_data_flow_coverage.py
    ```

### Running All Tests (Pytest)

To run all `pytest` discoverable tests in the project:
```bash
pytest
```

--- 

## Test Strategies 🧪

This project employs a combination of black-box and white-box testing strategies.

### Black-Box Testing

Focuses on the input-output behavior of the `pickle` module.

-   **Equivalence Partitioning**: Test cases are derived from various data types (integers, floats, strings, lists, dicts, sets, custom objects, etc.) to cover different pickling behaviors.
-   **Boundary Value Analysis**: Includes testing with empty collections, large data, deeply nested structures, and special float values.
-   **Stability Across Processes**: `pickle_test_stable.py` and `test_pickle_stability.py` specifically check if pickling the same object in different processes yields the same byte string by comparing SHA-256 hashes.
-   **Protocol Testing**: Tests are parameterized to run across different pickle protocols (0-5).

### White-Box Testing

Focuses on the internal structure of the `my_pickle.py` module.

-   **Statement Coverage**: `test_pickle_StatementCoverage.py` aims to ensure that each line of executable code in `my_pickle.py` is executed at least once during testing.
-   **Data-Flow Coverage (All-Defs and All-Uses)**: `test_data_flow_coverage.py` aims to cover all possible paths from the definition of a variable to its uses, ensuring that data propagation is tested thoroughly.
-   **Custom `my_pickle.py`**: A local copy of the `pickle` module (`white_box_tests/my_pickle.py`) is used for white-box tests. This allows for isolated testing and potentially for instrumentation or modification if needed, without affecting the system's standard Python library.

--- 

## Contributing 🤝

Contributions are welcome! If you'd like to improve the test suite or add new test cases, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix: `git checkout -b feature/your-exciting-feature`.
3.  Make your changes and commit them: `git commit -m "Add your exciting feature"`.
4.  Push your changes to your fork: `git push origin feature/your-exciting-feature`.
5.  Open a Pull Request against the main repository.

--- 

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

# 中文说明 🇨🇳

## Pickle 测试套件 🥒

![Python 版本](https://img.shields.io/badge/Python-3.7%2B-blue)
![许可证](https://img.shields.io/badge/License-MIT-green)
[![代码风格: PEP8](https://img.shields.io/badge/code%20style-PEP8-brightgreen)](https://www.python.org/dev/peps/pep-0008/)
[![测试](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/your_username/pickle_test) <!-- 请将 your_username 替换为您的 GitHub 用户名 -->

一个全面的测试套件，旨在评估 Python `pickle` 模块的**稳定性**和**正确性**。
**主要目标**：验证相同的输入是否能持续生成哈希一致的序列化输出，确保在不同场景和 Python 版本中 pickle 过程的可靠性。

---

## 目录 📖
- [功能特性](#功能特性-✨)
- [项目结构](#项目结构-📂)
- [安装指南](#安装指南-🛠️)
- [使用方法](#使用方法-🚀)
  - [运行黑盒测试](#运行黑盒测试)
  - [运行白盒测试](#运行白盒测试)
- [测试策略](#测试策略-🧪)
  - [黑盒测试](#黑盒测试)
  - [白盒测试](#白盒测试)
- [贡献代码](#贡献代码-🤝)
- [许可证](#许可证-📄)
- [English Readme](#pickle-test-suite-)

---

## 功能特性 ✨
- **稳定性测试**：确保多次 pickle 同一个对象或在不同进程中 pickle 会产生相同的字节流。
- **正确性测试**：验证对象是否被正确序列化和反序列化，并保持其状态和类型。
- **跨协议验证**：测试所有支持的 pickle 协议（0 到 5）下的行为。
- **全面的测试用例**：覆盖广泛的数据类型，包括基本类型、容器、嵌套结构、自定义类和边界情况。
- **黑盒与白盒方法**：采用功能性（黑盒）和结构性（白盒）测试方法进行彻底验证。
- **PEP8 规范**：代码遵循 Python 风格指南，以提高可读性和可维护性。

---

## 项目结构 📂

```
pickle_test/
├── black_box_test/               # 从用户角度测试 pickle 稳定性和正确性
│   ├── pickle_test_stable.py     # 可直接运行的脚本，用于测试各种数据类型的稳定性
│   ├── test_pickle_stability.py  # 基于 Pytest 的稳定性测试，可通过 pytest 运行
│   └── black_box_tests.py        # (旧版/实验性) 初期的黑盒测试思路
├── white_box_tests/              # 关注 pickle 内部实现的测试
│   ├── my_pickle.py              # 用于测试目的的 pickle 模块的本地副本/版本
│   ├── test_data_flow_coverage.py # 旨在实现数据流覆盖（所有定义、所有使用）的测试
│   └── test_pickle_StatementCoverage.py # 旨在实现语句覆盖的测试
├── .gitignore
├── LICENSE
└── README.md
```

---

## 安装指南 🛠️

### 环境要求
- Python 3.7+
- `pip` 和 `venv` (推荐用于管理依赖项)

### 步骤
1.  **克隆仓库**：
    ```bash
    git clone https://github.com/Mrkinggggg/pickle_test.git
    cd pickle_test
    ```

2.  **创建并激活虚拟环境** (推荐)：
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS 系统
    # venv\Scripts\activate    # Windows 系统
    ```

3.  **安装依赖**：
    运行测试的主要依赖是 `pytest`。
    ```bash
    pip install pytest
    ```

---

## 使用方法 🚀

测试分为黑盒和白盒两大类。

### 运行黑盒测试

这些测试验证 `pickle` 模块的外部行为，而不探究其内部工作原理。

1.  **稳定性测试 (直接执行)**：
    `pickle_test_stable.py` 脚本可以直接运行，以观察各种数据类型在多个进程中的稳定性。结果会打印到控制台。
    ```bash
    python black_box_test/pickle_test_stable.py
    ```

2.  **稳定性测试 (Pytest)**：
    `test_pickle_stability.py` 脚本使用 `pytest` 执行类似的稳定性检查。
    切换到 `black_box_test` 目录或从项目根目录运行：
    ```bash
    pytest black_box_test/test_pickle_stability.py
    ```

### 运行白盒测试

这些测试检查 `my_pickle.py`（用于隔离测试的 pickle 标准模块副本）的内部逻辑。

1.  **语句覆盖率测试**：
    这些测试旨在执行 `my_pickle.py` 中的每一条语句。
    ```bash
    pytest white_box_tests/test_pickle_StatementCoverage.py
    ```

2.  **数据流覆盖率测试**：
    这些测试旨在覆盖 `my_pickle.py` 中变量的定义和使用。
    ```bash
    pytest white_box_tests/test_data_flow_coverage.py
    ```

### 运行所有测试 (Pytest)

要运行项目中所有 `pytest` 可发现的测试：
```bash
pytest
```

---

## 测试策略 🧪

本项目结合了黑盒和白盒测试策略。

### 黑盒测试

关注 `pickle` 模块的输入输出行为。

-   **等价类划分**：测试用例源自各种数据类型（整数、浮点数、字符串、列表、字典、集合、自定义对象等），以覆盖不同的 pickle 行为。
-   **边界值分析**：包括测试空集合、大数据、深度嵌套结构和特殊的浮点数值。
-   **跨进程稳定性**：<mcfile name="pickle_test_stable.py" path="/Users/mrkinggg/pycharm_projects/pickle_test/black_box_test/pickle_test_stable.py"></mcfile> 和 <mcfile name="test_pickle_stability.py" path="/Users/mrkinggg/pycharm_projects/pickle_test/black_box_test/test_pickle_stability.py"></mcfile> 通过比较 SHA-256 哈希值，专门检查在不同进程中 pickle 同一个对象是否产生相同的字节串。
-   **协议测试**：测试被参数化以在不同的 pickle 协议（0-5）下运行。

### 白盒测试

关注 `my_pickle.py` 模块的内部结构。

-   **语句覆盖**：<mcfile name="test_pickle_StatementCoverage.py" path="/Users/mrkinggg/pycharm_projects/pickle_test/white_box_tests/test_pickle_StatementCoverage.py"></mcfile> 旨在确保 `my_pickle.py` 中的每一行可执行代码在测试过程中至少被执行一次。
-   **数据流覆盖（所有定义和所有使用）**：<mcfile name="test_data_flow_coverage.py" path="/Users/mrkinggg/pycharm_projects/pickle_test/white_box_tests/test_data_flow_coverage.py"></mcfile> 旨在覆盖从变量定义到其使用的所有可能路径，确保数据传播得到彻底测试。
-   **自定义 `my_pickle.py`**：白盒测试使用 `pickle` 模块的本地副本 (<mcfile name="my_pickle.py" path="/Users/mrkinggg/pycharm_projects/pickle_test/white_box_tests/my_pickle.py"></mcfile>)。这允许进行隔离测试，并且如果需要，可以进行插桩或修改，而不会影响系统的标准 Python 库。

---

## 贡献代码 🤝

欢迎贡献！如果您希望改进测试套件或添加新的测试用例，请遵循以下步骤：

1.  Fork 本仓库。
2.  为您的功能或错误修复创建一个新分支：`git checkout -b feature/your-exciting-feature`。
3.  进行更改并提交：`git commit -m "Add your exciting feature"`。
4.  将您的更改推送到您的 fork：`git push origin feature/your-exciting-feature`。
5.  针对主仓库提交一个 Pull Request。

---

## 许可证 📄

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。


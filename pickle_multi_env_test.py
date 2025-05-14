import pickle
import platform
import subprocess
import sys
import hashlib
import tempfile
from typing import Any, Dict, List, Tuple


class PickleTester:
    """Testing tool for serialization consistency of Python pickle module across different environments"""

    def __init__(self):
        self.test_results = []

    def generate_test_objects(self) -> List[Tuple[str, Any]]:
        """Generate a diverse set of test objects"""
        test_objects = [
            ("basic_int", 42),
            ("basic_str", "Hello, pickle!"),
            ("basic_float", 3.14159265358979323846),
            ("list_simple", [1, 2, 3, 4, 5]),
            ("dict_simple", {"a": 1, "b": 2, "c": 3}),
            ("tuple_simple", (1, "two", 3.0)),
            ("set_simple", {1, 2, 2, 3}),
            ("complex_list", [{"a": [1, 2]}, (3, 4), {5, 6}]),
            ("recursive_list", []),
            ("nested_dict", {
                "level1": {
                    "level2": {
                        "level3": "deep value"
                    }
                }
            }),
        ]

        # Add a recursive object
        recursive_list = test_objects[8][1]
        recursive_list.append(recursive_list)

        return test_objects

    def get_environment_info(self) -> Dict[str, str]:
        """Retrieve key information about the current test environment"""
        return {
            "python_version": sys.version,
            "os": platform.platform(),
            "pickle_protocol": str(pickle.HIGHEST_PROTOCOL),
            "machine": platform.machine(),
            "processor": platform.processor()
        }

    def pickle_and_hash(self, obj: Any, protocol: int) -> str:
        """Pickle an object and compute its SHA-256 hash"""
        try:
            pickled_data = pickle.dumps(obj, protocol=protocol)
            return hashlib.sha256(pickled_data).hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def run_local_tests(self, protocols: List[int]) -> List[Dict]:
        """Run all test cases in the local environment"""
        test_objects = self.generate_test_objects()
        environment = self.get_environment_info()
        results = []

        for name, obj in test_objects:
            for protocol in protocols:
                test_result = {
                    "test_name": name,
                    "environment": environment.copy(),
                    "protocol": protocol,
                    "hash": self.pickle_and_hash(obj, protocol)
                }
                results.append(test_result)

        self.test_results.extend(results)
        return results

    def run_remote_test(self, python_executable: str, test_script_path: str) -> Dict:
        """Run tests in a remote/different Python environment"""
        result_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        result_file.close()

        cmd = [
            python_executable,
            test_script_path,
            "--output-file", result_file.name
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            with open(result_file.name, 'r') as f:
                import json
                return json.load(f)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "environment": {
                    "python_executable": python_executable
                },
                "results": []
            }

    def compare_results(self, baseline: List[Dict], target: List[Dict]) -> Dict:
        """Compare two sets of test results to identify inconsistent test cases"""
        mismatches = []

        # Group results by test name and protocol
        baseline_map = {(r["test_name"], r["protocol"]): r for r in baseline}
        target_map = {(r["test_name"], r["protocol"]): r for r in target}

        # Check all test cases
        for key in set(baseline_map.keys()).union(target_map.keys()):
            if key not in baseline_map:
                mismatches.append({
                    "test_name": key[0],
                    "protocol": key[1],
                    "status": "missing_in_baseline"
                })
            elif key not in target_map:
                mismatches.append({
                    "test_name": key[0],
                    "protocol": key[1],
                    "status": "missing_in_target"
                })
            else:
                base = baseline_map[key]
                tgt = target_map[key]
                if base["hash"] != tgt["hash"]:
                    mismatches.append({
                        "test_name": key[0],
                        "protocol": key[1],
                        "baseline_hash": base["hash"],
                        "target_hash": tgt["hash"],
                        "status": "hash_mismatch"
                    })

        return {
            "total_tests": len(baseline_map),
            "mismatches": mismatches
        }

    def export_results(self, filename: str) -> None:
        """Export test results to a JSON file"""
        import json
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)


if __name__ == "__main__":
    tester = PickleTester()

    # Run local tests (using all available pickle protocols)
    max_protocol = pickle.HIGHEST_PROTOCOL
    protocols = list(range(0, max_protocol + 1))
    local_results = tester.run_local_tests(protocols)

    # Example: Compare results across different Python versions
    # Note: Requires pre-configured paths to different Python environments
    # remote_python = "/path/to/python3.9"
    # remote_results = tester.run_remote_test(remote_python, __file__)

    # Example: Compare results
    # comparison = tester.compare_results(local_results, remote_results["results"])

    # Export results
    tester.export_results("pickle_test_results.json")

    print(f"Local tests completed. Results saved to pickle_test_results.json")
    print(f"Executed {len(local_results)} test cases")

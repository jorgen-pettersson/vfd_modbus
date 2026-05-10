#!/usr/bin/env python3
"""
VFD Test Runner - Run individual or all tests
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import subprocess
import argparse

def run_test(script_path, description):
    """Run a single test script."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"Script: {script_path}")
    print(f"{'='*60}")

    try:
        result = subprocess.run([sys.executable, script_path], capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running test: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='VFD Test Runner')
    parser.add_argument('--category', choices=['unit', 'integration', 'all'], default='all',
                       help='Test category to run')
    parser.add_argument('--test', help='Run specific test file')
    args = parser.parse_args()

    if args.test:
        # Run specific test
        test_path = f"tests/{args.test}"
        if not os.path.exists(test_path):
            print(f"Test file not found: {test_path}")
            return 1

        success = run_test(test_path, f"Specific test: {args.test}")
        return 0 if success else 1

    print("="*60)
    print("   VFD TEST RUNNER")
    print("="*60)

    test_suites = []

    if args.category in ['unit', 'all']:
        test_suites.extend([
            ("tests/unit/test_controller_setup.py", "Controller Setup Test"),
            ("tests/unit/test_interactive.py", "Interactive Controller Test"),
            ("tests/unit/test_input.py", "Input Handling Test"),
            ("tests/unit/test_simple.py", "Simple Controller Test"),
        ])

    if args.category in ['integration', 'all']:
        test_suites.extend([
            ("tests/integration/test_serial_comm.py", "Serial Communication Test"),
            ("tests/integration/test_basic_commands.py", "Basic VFD Commands Test"),
        ])

    if not test_suites:
        print("No tests to run!")
        return 0

    results = []

    for script_path, description in test_suites:
        if not os.path.exists(script_path):
            print(f"⚠ Test file not found: {script_path}")
            continue

        success = run_test(script_path, description)
        results.append((description, success))

    print("\n" + "="*60)
    print("   TEST RESULTS SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for description, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {description}")

    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
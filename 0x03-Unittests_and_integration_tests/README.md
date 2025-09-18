# 0x03. Unittests and Integration Tests

This project is part of the ALX Backend Python curriculum.  
It focuses on writing automated tests to verify that code works as expected, and that different components integrate correctly.

## Learning Objectives

By the end of this project, you should be able to explain:

- The difference between **unit tests** and **integration tests**
- How to use **mocking** to isolate code under test
- How to use **parameterized tests** to check multiple inputs/outputs
- How to use **fixtures** for integration testing
- How to run Python tests with the built-in `unittest` framework

## Files in this project

- `utils.py`: utility functions provided for testing
- `client.py`: `GithubOrgClient` class that interacts with the GitHub API
- `fixtures.py`: pre-defined payloads for integration testing
- `test_utils.py`: unit tests for functions in `utils.py`
- `test_client.py`: unit and integration tests for `client.py`

## Requirements

- Python 3.7 (Ubuntu 18.04 LTS environment)
- All files should be executable
- Code must follow **pycodestyle** (PEP8) style guide
- All functions, classes, and modules must include docstrings
- Tests must use the built-in `unittest` framework
- External HTTP/database calls should be mocked in unit tests

## Running Tests

From the project directory:

```bash
# Run all tests
python -m unittest discover -s 0x03-Unittests_and_integration_tests

# Run only utils tests
python -m unittest 0x03-Unittests_and_integration_tests.test_utils

# Run only client tests
python -m unittest 0x03-Unittests_and_integration_tests.test_client

# ALX Backend Python – 0x03: Unit Tests and Integration Tests

This repository contains Python unit and integration tests for various utility functions and the `GithubOrgClient` class. The exercises focus on **parameterization, mocking, patching, and fixtures** using `unittest`, `unittest.mock`, and `parameterized`.

---

## Repository Structure

---

## Tasks Overview

### 0. Parameterize a Unit Test
- Write `TestAccessNestedMap.test_access_nested_map`.
- Use `@parameterized.expand` to test `utils.access_nested_map` for:
  - `nested_map={"a": 1}`, `path=("a",)`
  - `nested_map={"a": {"b": 2}}`, `path=("a",)`
  - `nested_map={"a": {"b": 2}}`, `path=("a", "b")`
- Use `assertEqual` to check results.

---

### 1. Parameterize a Unit Test for Exceptions
- Implement `TestAccessNestedMap.test_access_nested_map_exception`.
- Test that `KeyError` is raised for:
  - `nested_map={}`, `path=("a",)`
  - `nested_map={"a": 1}`, `path=("a", "b")`
- Verify that the exception message matches expectations.

---

### 2. Mock HTTP Calls
- Implement `TestGetJson.test_get_json`.
- Mock `requests.get` using `unittest.mock.patch`.
- Parametrize tests with:
  - `test_url="http://example.com"`, `test_payload={"payload": True}`
  - `test_url="http://holberton.io"`, `test_payload={"payload": False}`
- Assert that:
  - The mocked `get` method is called once per test.
  - `utils.get_json` returns the correct payload.

---

### 3. Parameterize and Patch (Memoization)
- Implement `TestMemoize.test_memoize`.
- Test the `utils.memoize` decorator:
  - Ensure `a_method` is called only **once** even when `a_property` is accessed twice.

---

### 4. Parameterize and Patch as Decorators
- Implement `TestGithubOrgClient.test_org` in `test_client.py`.
- Use `@patch` and `@parameterized.expand`.
- Test `GithubOrgClient.org` for:
  - `"google"`
  - `"abc"`
- Ensure no external HTTP calls are made.

---

### 5. Mocking a Property
- Implement `test_public_repos_url`.
- Patch `GithubOrgClient.org` to return a known payload.
- Assert that `_public_repos_url` returns the expected URL.

---

### 6. More Patching
- Implement `TestGithubOrgClient.test_public_repos`.
- Mock `get_json` and `_public_repos_url`.
- Verify the returned list of repositories.
- Ensure each mocked method/property is called **once**.

---

### 7. Parameterize `has_license`
- Implement `TestGithubOrgClient.test_has_license`.
- Parametrize with:
  - `repo={"license": {"key": "my_license"}}`, `license_key="my_license"`
  - `repo={"license": {"key": "other_license"}}`, `license_key="my_license"`
- Test that the function returns the expected boolean value.

---

### 8. Integration Test: Fixtures
- Implement `TestIntegrationGithubOrgClient`.
- Use `@parameterized_class` with fixtures from `fixtures.py`:
  - `org_payload`, `repos_payload`, `expected_repos`, `apache2_repos`
- Mock `requests.get` to return the expected payloads.
- Use `setUpClass` and `tearDownClass` to manage patching.
- Test the integration of `public_repos` with actual fixture data.

---

## Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/your-username/alx-backend-python.git
cd alx-backend-python/0x03-Unittests_and_integration_tests


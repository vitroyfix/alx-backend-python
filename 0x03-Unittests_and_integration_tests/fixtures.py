#!/usr/bin/env python3
"""
Fixtures for testing the client
"""

# 1. Define payloads for 'google'
org_payload_google = {
    "login": "google",
    "id": 1342004,
    "repos_url": "https://api.github.com/orgs/google/repos",
}

repos_payload_google = [
    {"name": "protobuf", "license": {"key": "apache-2.0"}},
    {"name": "pytype", "license": {"key": "apache-2.0"}},
    {"name": "kubernetes", "license": {"key": "apache-2.0"}},
    {"name": "nomulus", "license": {"key": "apache-2.0"}},
    {"name": "google-test", "license": {"key": "bsd-3-clause"}},
    {"name": "flatbuffers", "license": {"key": "apache-2.0"}},
]

# 2. Define expected results for 'google'
expected_repos_google = [
    "protobuf",
    "pytype",
    "kubernetes",
    "nomulus",
    "google-test",
    "flatbuffers",
]

apache2_repos_google = [
    "protobuf",
    "pytype",
    "kubernetes",
    "nomulus",
    "flatbuffers",
]

# 3. Define payloads for 'abc'
org_payload_abc = {
    "login": "abc",
    "id": 12345,
    "repos_url": "https://api.github.com/orgs/abc/repos",
}

repos_payload_abc = [
    {"name": "repo1", "license": {"key": "mit"}},
    {"name": "repo2", "license": {"key": "apache-2.0"}},
]

# 4. Define expected results for 'abc'
expected_repos_abc = ["repo1", "repo2"]
apache2_repos_abc = ["repo2"]

# 5. Define the TEST_SETTING variable that test_client.py imports
TEST_SETTING = (
    (
        org_payload_google,
        repos_payload_google,
        expected_repos_google,
        apache2_repos_google
    ),
    (
        org_payload_abc,
        repos_payload_abc,
        expected_repos_abc,
        apache2_repos_abc
    ),
)
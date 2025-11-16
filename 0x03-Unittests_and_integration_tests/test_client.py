#!/usr/bin/env python3
"""
Unit tests for client.py
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_SETTING  # This import will now work
from requests import HTTPError
from typing import Dict, Any


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(
            self,
            org_name: str,
            expected_payload: Dict[str, Any],
            mock_get_json: Mock
    ) -> None:
        """
        Test that `GithubOrgClient.org` returns the correct value
        and `get_json` is called once.
        """
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self) -> None:
        """
        Test that `_public_repos_url` property returns the correct URL
        based on the mocked `org` payload.
        """
        known_payload = {"repos_url": "https.api.github.com/orgs/test/repos"}
        # Corrected indentation for E128
        with patch.object(GithubOrgClient,
                          'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = known_payload
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, known_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Test that `public_repos` returns the correct list of repo names.
        """
        json_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = json_payload

        # Corrected indentation for E128
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            known_repos_url = "https://api.github.com/orgs/test/repos"
            mock_public_repos_url.return_value = known_repos_url
            client = GithubOrgClient("test")
            repos = client.public_repos()
            expected_repos = ["repo1", "repo2"]
            self.assertEqual(repos, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(known_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(
            self,
            repo: Dict[str, Any],
            license_key: str,
            expected: bool
    ) -> None:
        """
        Test the `has_license` static method with parameterized inputs.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(TEST_SETTING)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for `GithubOrgClient` using fixtures."""

    @classmethod
    def setUpClass(
            cls,
            org_payload,
            repos_payload,
            expected_repos,
            apache2_repos
    ) -> None:
        """
        Set up class method to mock requests.get.
        Parameters are injected by @parameterized_class.
        """
        cls.org_payload = org_payload
        cls.repos_payload = repos_payload
        cls.expected_repos = expected_repos
        cls.apache2_repos = apache2_repos
        cls.org_name = org_payload["login"]

        url_payload_map = {
            f"https://api.github.com/orgs/{cls.org_name}": cls.org_payload,
            cls.org_payload["repos_url"]: cls.repos_payload,
        }

        def side_effect(url):
            """Side effect function for mocked requests.get."""
            mock_response = Mock()
            if url in url_payload_map:
                mock_response.json.return_value = url_payload_map[url]
            else:
                mock_response.raise_for_status.side_effect = HTTPError
            return mock_response

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class method to stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Integration test for `public_repos` (without license filter).
        """
        client = GithubOrgClient(self.org_name)
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Integration test for `public_repos` (with "apache-2.0" license).
        """
        client = GithubOrgClient(self.org_name)
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()

# This blank line at the end fixes W292 (no newline at end of file)
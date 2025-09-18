#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns the expected payload from get_json."""
        mock_get_json.return_value = {"org": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"org": org_name})

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the repos_url from org payload."""
        fake_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        with patch.object(
            GithubOrgClient, "org", new_callable=unittest.mock.PropertyMock
        ) as mock_org:
            mock_org.return_value = fake_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, fake_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns repo names list."""
        fake_url = "https://api.github.com/orgs/testorg/repos"
        fake_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = fake_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new=fake_url):
            client = GithubOrgClient("testorg")
            result = client.public_repos()

        self.assertEqual(result, ["repo1", "repo2"])
        mock_get_json.assert_called_once_with(fake_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns True only if license matches."""
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and set up side_effect."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return unittest.mock.Mock(json=lambda: cls.org_payload)
            if url == cls.org_payload.get("repos_url"):
                return unittest.mock.Mock(json=lambda: cls.repos_payload)
            return unittest.mock.Mock(json=lambda: {})

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration: public_repos returns expected repos."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration: public_repos filters repos by license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

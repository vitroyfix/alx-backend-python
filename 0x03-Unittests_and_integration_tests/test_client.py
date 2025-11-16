#!/usr/bin/env python3
"""
Unit tests for client.py
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_SETTING  # For Task 8


# --- Task 4 ---
class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that `GithubOrgClient.org` returns the correct value
        and `get_json` is called once.
        """
        # Define a test payload for the mock
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        # Instantiate the client
        client = GithubOrgClient(org_name)
        
        # Call the .org property
        result = client.org

        # Check that get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Check that the result is the expected payload
        self.assertEqual(result, test_payload)

    # --- Task 5 ---
    def test_public_repos_url(self):
        """
        Test that `_public_repos_url` property returns the correct URL
        based on the mocked `org` payload.
        """
        # Define a known payload that .org would return
        known_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        # Use patch.object with PropertyMock to mock the .org property
        with patch.object(GithubOrgClient, 'org',
                         new_callable=PropertyMock) as mock_org:
            
            # Set the return value of the mocked property
            mock_org.return_value = known_payload
            
            # Instantiate the client
            client = GithubOrgClient("test")
            
            # Access the _public_repos_url property
            result = client._public_repos_url

            # Check that the result is the 'repos_url' from the payload
            self.assertEqual(result, known_payload["repos_url"])

    # --- Task 6 ---
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that `public_repos` returns the correct list of repo names.
        """
        # Payload returned by get_json (a list of repo dicts)
        json_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = json_payload

        # Mock the _public_repos_url property
        with patch.object(GithubOrgClient, '_public_repos_url',
                         new_callable=PropertyMock) as mock_public_repos_url:
            
            # Set the return value for the property
            known_repos_url = "https://api.github.com/orgs/test/repos"
            mock_public_repos_url.return_value = known_repos_url
            
            # Instantiate the client
            client = GithubOrgClient("test")
            
            # Call the public_repos method
            repos = client.public_repos()

            # Test that the result is the list of repo names
            expected_repos = ["repo1", "repo2"]
            self.assertEqual(repos, expected_repos)

            # Test that the mocked property was called once
            mock_public_repos_url.assert_called_once()
            
            # Test that get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(known_repos_url)

    # --- Task 7 ---
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test the `has_license` static method with parameterized inputs.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# --- Task 8 ---
@parameterized_class(
    # This uses the TEST_SETTING fixture from fixtures.py
    # which is a list of tuples:
    # (org_name, org_payload, repos_payload, expected_repos, apache2_repos)
    TEST_SETTING
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for `GithubOrgClient` using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up class method to mock requests.get"""
        
        # Build a map of URLs to their expected payloads
        url_payload_map = {
            f"https://api.github.com/orgs/{cls.org_name}": cls.org_payload,
            cls.org_payload["repos_url"]: cls.repos_payload,
        }

        # Define the side_effect function for the patch
        def side_effect(url):
            """
            Side effect function for mocked requests.get.
            Returns a Mock response based on the URL.
            """
            mock_response = Mock()
            if url in url_payload_map:
                mock_response.json.return_value = url_payload_map[url]
            else:
                # Raise HTTPError for any unexpected URL
                mock_response.raise_for_status()
            return mock_response

        # Start the patcher
        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Integration test for `public_repos` (without license filter).
        """
        client = GithubOrgClient(self.org_name)
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Integration test for `public_repos` (with "apache-2.0" license).
        """
        client = GithubOrgClient(self.org_name)
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
#!/usr/bin/env python3
"""
A module for a GitHub Org Client.
"""
from utils import get_json
from typing import List, Dict, Any


class GithubOrgClient:
    """
    A client for interacting with the GitHub API for a specific organization.
    """
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str):
        """
        Initialize the client with the organization name.

        Args:
            org_name (str): The name of the GitHub organization.
        """
        self._org_name = org_name
        self._org = None  # For memoization

    @property
    def org(self) -> Dict[str, Any]:
        """
        Memoized property that fetches and returns the organization's details.
        """
        if self._org is None:
            url = self.ORG_URL.format(org=self._org_name)
            self._org = get_json(url)
        return self._org

    @property
    def _public_repos_url(self) -> str:
        """
        Property to get the URL for the organization's public repositories.
        """
        return self.org.get("repos_url", "")

    def public_repos(self, license: str = None) -> List[str]:
        """
        Get a list of public repository names for the organization.

        Can be filtered by license key.

        Args:
            license (str, optional): The license key to filter by
                                     (e.g., "apache-2.0").

        Returns:
            List[str]: A list of repository names.
        """
        repos_url = self._public_repos_url
        if not repos_url:
            return []

        repos_payload = get_json(repos_url)

        repo_names: List[str] = []
        for repo in repos_payload:
            if license is None:
                repo_names.append(repo["name"])
            elif self.has_license(repo, license):
                repo_names.append(repo["name"])

        return repo_names

    @staticmethod
    def has_license(repo: Dict[str, Any], license_key: str) -> bool:
        """
        Check if a repository has a specific license.

        Args:
            repo (Dict[str, Any]): The repository dictionary from the API.
            license_key (str): The license key to check for (e.g., "mit").

        Returns:
            bool: True if the license key matches, False otherwise.
        """
        if not repo or not isinstance(repo.get("license"), dict):
            return False
        return repo["license"].get("key") == license_key
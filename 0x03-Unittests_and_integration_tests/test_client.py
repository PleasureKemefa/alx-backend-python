#!/usr/bin/env python3
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock
import client
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test .org() calls get_json and returns expected value"""
        mock_get_json.return_value = {"login": org_name}
        gh = GithubOrgClient(org_name)

        self.assertEqual(gh.org(), {"login": org_name})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url retrieves repos_url from .org() payload"""
        gh = GithubOrgClient("test_org")
        fake_payload = {"repos_url": "https://api.github.com/test_org/repos"}

        with patch.object(GithubOrgClient, "org", return_value=fake_payload):
            url = gh._public_repos_url

        self.assertEqual(url, fake_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos fetches and returns repo names correctly"""
        gh = GithubOrgClient("test_org")
        repos_url = "https://api.github.com/test_org/repos"
        fake_repos = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = fake_repos

        with patch.object(GithubOrgClient, "_public_repos_url", repos_url):
            repo_names = gh.public_repos()

        mock_get_json.assert_called_once_with(repos_url)
        self.assertEqual(repo_names, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean based on license key"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(org_payload, repos_payload, expected_repos, apache2_repos)]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using fixture data, mocking HTTP calls only"""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()
        mock_resp = Mock()
        mock_resp.json.side_effect = [cls.org_payload, cls.repos_payload]
        mock_get.return_value = mock_resp

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repos"""
        gh = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(gh.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns filtered repos by license"""
        gh = GithubOrgClient(self.org_payload["login"])
        result = gh.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)

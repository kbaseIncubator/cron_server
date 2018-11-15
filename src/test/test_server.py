"""
Simple integration tests on the API itself.

We make actual ajax requests to the running docker container.
"""
import unittest
import requests
import os

url = os.environ.get('TEST_URL', 'http://web:5000')
# auth_token = os.environ.get('KBASE_TEST_AUTH_TOKEN', '')
# headers = {'Authorization': 'Bearer ' + auth_token}


class TestServer(unittest.TestCase):

    def test_server_status(self):
        resp = requests.get(url).json()
        self.assertTrue(len(resp['commit_hash']))
        self.assertTrue(len(resp['repo_url']))

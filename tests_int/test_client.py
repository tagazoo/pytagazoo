import unittest
import unittest.mock as mock
import time

from tagazoo.client import Client

# needed account
EMAIL = "foo.bar@gmail.com"
PASSWORD = "f_Azerty!1"

class TestClient(unittest.TestCase):

    def setUp(self):
        time.sleep(2)
        self.client = Client("http://blackwell:8888/v1/user")

    def test_signup(self):
        self.client.signup(EMAIL, PASSWORD)
        token = self.client.get_token()

        self.assertNotEqual(token,None)

    def test_renew(self):
        self.client.signup(EMAIL, PASSWORD)
        token_1 = self.client.get_token()
        time.sleep(2)
        self.client.renew_token()
        token_2 = self.client.get_token()

        self.assertNotEqual(token_1, token_2)

    def test_list_node(self):
        self.client.signup(EMAIL, PASSWORD)
        time.sleep(1)
        node_list = self.client.list_nodes()

        self.assertTrue(isinstance(node_list, list))

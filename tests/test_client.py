import unittest
import unittest.mock as mock

from tagazoo.client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.request = mock.Mock()
        self.client = Client(_requests=self.request)

    def test_signup(self):
        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 200
        response.json = mock.Mock(return_value={"token":"xxx.yyy.zzz"})
        self.client.signup("foo", "bar")

        result = self.client.get_token()
        self.assertEqual(result, "xxx.yyy.zzz")

    def test_signup_failed(self):
        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 404

        with self.assertRaises(Exception) as e:
            self.client.signup("foo", "bar")

    def test_add_node(self):
        response = mock.Mock()
        self.request.post = mock.Mock(return_value=response)
        response.status_code = 201
        response.json = mock.Mock(return_value={"node_id": "xxx.yyy.zzz"})

        result = self.client.add_node()

        self.assertEqual(result, "xxx.yyy.zzz")

    def test_add_node_authorization(self):
        response = mock.Mock()
        self.request.post = mock.Mock(return_value=response)
        response.status_code = 201
        response.json = mock.Mock(return_value={"node_id": "xxx.yyy.zzz"})

        self.client.add_node()

        args, kwargs = self.request.post.call_args_list[0]
        self.assertTrue("headers" in kwargs)

    def test_add_node_failed(self):
        response = mock.Mock()
        self.request.post = mock.Mock(return_value=response)
        response.status_code = 400

        with self.assertRaises(Exception):
            self.client.add_node()

    def test_renew_token(self):
        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 200
        response.json = mock.Mock(return_value={"token": "xxx.yyy.zzz"})

        self.client.renew_token()
        result = self.client.get_token()
        self.assertEqual(result, "xxx.yyy.zzz")

    def test_renew_token_fail(self):
        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 400

        with self.assertRaises(Exception):
            self.client.renew_token()

    def test_list_nodes(self):
        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 200
        response.json = mock.Mock(return_value={"nodes": [{"node_id" : "xxx.yyy.zzz"}]})

        result = self.client.list_nodes()
        expected = [{"node_id": "xxx.yyy.zzz"}]
        self.assertEqual(result, expected)

    def test_get_node_token(self):
        response = mock.Mock()
        self.request.post = mock.Mock(return_value=response)
        response.status_code = 200
        response.json = mock.Mock(return_value={"token": "aaa.bbb.ccc"})

        result = self.client.get_node_token("xxx.yyy.zzz")

        self.assertEqual(result, "aaa.bbb.ccc")

    def test_get_node_token_no_node(self):
        response = mock.Mock()
        self.request.post = mock.Mock(return_value=response)
        response.status_code = 404

        with self.assertRaises(Exception):
            self.client.get_node_token("xxx.yyy.zzz")

    def test_job_request(self):
        response = mock.Mock()
        self.request.post = mock.Mock(return_value=response)
        response.status_code = 201
        response.json = mock.Mock(return_value={"job_id": "aaa.bbb.ccc"})

        result = self.client.job_request("ping", ip="127.0.0.1")

        self.assertEqual(result, "aaa.bbb.ccc")

    def test_job_request_failed(self):
        response = mock.Mock()
        self.request.post = mock.Mock(return_value=response)
        response.status_code = 403

        with self.assertRaises(Exception):
            self.client.job_request("ping", ip="127.0.0.1")

    def test_job_result(self):
        
        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 200
        response.json = mock.Mock(return_value={
            "status": "success",
            "job": {
                "result": {
                    "packet_transmitted": 3,
                    "packet_received": 3,
                    "scan_time": 2002,
                    "ttl": [
                        53,
                        53,
                        53
                    ],
                    "time": [
                        28.3,
                        32.8,
                        34.2
                    ]
                }
            }
        })

        status, result = self.client.job_result("aaa.bbb.ccc")

        self.assertEqual(status, "success")

    def test_job_result_2(self):

        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 200
        response.json = mock.Mock(return_value={
            "status": "success",
            "job": {
                "result": {
                    "packet_transmitted": 3,
                    "packet_received": 3,
                    "scan_time": 2002,
                    "ttl": [
                        53,
                        53,
                        53
                    ],
                    "time": [
                        28.3,
                        32.8,
                        34.2
                    ]
                }
            }
        })

        expected = {
            "packet_transmitted": 3,
            "packet_received": 3,
            "scan_time": 2002,
            "ttl": [
                53,
                53,
                53
            ],
            "time": [
                28.3,
                32.8,
                34.2
            ]
        }

        status, result = self.client.job_result("aaa.bbb.ccc")

        self.assertEqual(result, expected)


    def test_job_result_abort(self):

        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 200
        response.json = mock.Mock(return_value={"status": "abort"})

        status, result = self.client.job_result("aaa.bbb.ccc")

        self.assertEqual(status, "abort")

    def test_job_result_no_job_id(self):

        response = mock.Mock()
        self.request.get = mock.Mock(return_value=response)
        response.status_code = 404

        with self.assertRaises(Exception):
            self.client.job_result("aaa.bbb.ccc")        

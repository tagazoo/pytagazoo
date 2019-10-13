import requests

class Client:
    def __init__(self, _default_path="https://api.tagazoo.com/v1/user", _requests=requests):
        self._default_path = _default_path
        self._requests = _requests
        self._token = None

    def _header(self)->str:
        return {"Authorization": "Bearer {}".format(self._token)}

    def set_token(self, token:str)->None:
        # set the user token
        self._token = token

    def get_token(self) -> str:
        # set the user token
        return self._token

    def get_header(self):
        return {"Authorization": "Bearer {}".format(self._token)}

    def signup(self, email:str, password:str)->None:
        # signup on tagazoo and get the token
        path = self._default_path + '/token'
        body = {"email": email, "password":password}
        reponse = self._requests.get(path, json=body)
        body = reponse.json()
        
        if reponse.status_code != 200:
            raise Exception("Email or password are invalid ({})".format(body))

        self._token = body["token"]

    def add_node(self)->str:
        # add a node to the account
        path = self._default_path + '/node'
        header = self.get_header()
        reponse = self._requests.post(path, headers=header)

        if reponse.status_code != 201:
            message = "Can't add a node (http code : {})".format(reponse.status_code)
            raise Exception(message)

        body = reponse.json()
        return body["node_id"]

    def renew_token(self) -> str:
        # Renew the token. Need an valid token
        path = self._default_path + '/renew'
        header = self.get_header()
        reponse = self._requests.get(path, headers=header)

        if reponse.status_code != 200:
            message = "Can't renew the token (http code : {})".format(reponse.status_code)
            raise Exception(message)

        body = reponse.json()
        self._token = body["token"]

    def list_nodes(self)->dict:
        # Returns the list of nodes properties
        path = self._default_path + '/node'
        header = self.get_header()
        reponse = self._requests.get(path, headers=header)

        if reponse.status_code != 200:
            message = "Can't get the node list (http code : {})".format(
                reponse.status_code)
            raise Exception(message)

        body = reponse.json()
        return body["nodes"]

    def get_node_token(self, node_id:str):
        data = {"node_id":node_id}
        path = self._default_path + '/node/token'
        header = self.get_header()
        reponse = self._requests.post(path, headers=header, data=data)

        if reponse.status_code != 200:
            message = "Can't get the token for the node {} (http code : {})".format(
                node_id, reponse.status_code)
            raise Exception(message)

        body = reponse.json()
        return body["token"]

    def job_request(self, action:str, **kwargs)->str:
        data = {"action": action, "parameters": kwargs}
        path = self._default_path + '/job'
        header = self.get_header()
        reponse = self._requests.post(path, headers=header, data=data)

        if reponse.status_code != 201:
            message = "Can't request for this job (http code : {})".format(
                node_id, reponse.status_code)
            raise Exception(message)

        body = reponse.json()
        return body["job_id"]

    def job_result(self, job_id:str)->(str, dict):
        data = {"job_id": job_id}
        path = self._default_path + '/job'
        header = self.get_header()
        reponse = self._requests.get(path, headers=header, data=data)

        if reponse.status_code != 200:
            message = "Can't get the job (http code : {})".format(
                node_id, reponse.status_code)
            raise Exception(message)

        body = reponse.json()
        status = body["status"]
        result = None
        if status == "success":
            result = body["job"]["result"]
        return status, result

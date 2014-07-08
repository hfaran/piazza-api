import requests
import json
import getpass


class AuthenticationError(Exception):
    """AuthenticationError"""


class NotAuthenticatedError(Exception):
    """NotAuthenticatedError"""


class PiazzaAPI(object):

    """Tiny wrapper around Piazza's Internal API

    Example:
        >>> p = PiazzaAPI("hl5qm84dl4t3x2")
        >>> p.user_auth()
        Email: ...
        Password: ...
        >>> p.get(181)
        ...
    """

    def __init__(self, network_id):
        """
        - Get user's password
        - Authenticate with Piazza and get session cookie

        :type  network_id: str
        :param network_id: This is the ID of the network (or class) from which
            to query posts
        :type  email: str
        "param email: Email address with which to authenticate (log in) with
        """
        self._nid = network_id
        self.base_api_url = 'https://piazza.com/logic/api'
        self.cookies = None

    def user_auth(self, email=None, password=None):
        """Login with email, password and get back a session cookie

        :type  email: str
        :param email: The email used for authentication
        :type  password: str
        :param password: The password used for authentication
        """
        email = raw_input("Email: ") if email is None else email
        password = getpass.getpass() if password is None else password

        login_url = self.base_api_url
        login_data = {
            "method": "user.login",
            "params": {
                "email": email,
                "pass": password
            }
        }
        login_params = {"method": "user.login"}
        # If the user/password match, the server respond will contain a
        #  session cookie that you can use to authenticate future requests.
        r = requests.post(
            login_url,
            data=json.dumps(login_data),
            params=login_params
        )
        if r.json()["result"] not in ["OK"]:
            raise AuthenticationError(
                "Could not authenticate.\n{}".format(r.json())
            )
        self.cookies = r.cookies

    def demo_auth(self, auth=None, url=None):
        """Authenticate with a "Share Your Class" URL using a demo user.

        You may provide either the entire ``url`` or simply the ``auth`` parameter.

        :param url: Example - "https://piazza.com/demo_login?nid=hbj11a1gcvl1s6&auth=06c111b"
        :param auth: Example - "06c111b"
        """
        assert all([
            auth or url,  # Must provide at least one
            not (auth and url)  # Cannot provide more than one
        ])
        if url is None:
            url = "https://piazza.com/demo_login"
            params = dict(nid=self._nid, auth=auth)
            res = requests.get(url, params=params)
        else:
            res = requests.get(url)
        self.cookies = res.cookies

    def get(self, cid, nid=None):
        """Get data from post `cid` in network `nid`

        :type  nid: str
        :param nid: This is the ID of the network (or class) from which
            to query posts. This is optional and only to override the existing
            `network_id` entered when created the class
        :type  cid: str|int
        :param cid: This is the post ID which we grab
        :returns: Python object containing returned data
        """
        if self.cookies is None:
            raise NotAuthenticatedError("You must authenticate before making any other requests.")

        nid = nid if nid else self._nid
        content_url = self.base_api_url
        content_params = {"method": "get.content"}
        content_data = {
            "method": "content.get",
            "params": {
                "cid": cid,
                "nid": nid
            }
        }
        return requests.post(
            content_url,
            data=json.dumps(content_data),
            params=content_params,
            cookies=self.cookies
        ).json()

"""Inspired by: https://gist.github.com/alexjlockwood/6797443"""

import requests
import json
import getpass


class AuthenticationError(Exception):

    """AuthenticationError"""


class PiazzaAPI(object):

    """Tiny wrapper around Piazza's Internal REST API

    Example:
        >>> p = PiazzaAPI("hl5qm84dl4t3x2")
        Email: ...
        Password: ...
        >>> p.get(181)
        ...
    """

    def __init__(self, network_id, email=None):
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

        email = email if email else raw_input("Email: ")
        password = getpass.getpass()
        self.cookies = self._authenticate(email, password)

    def _authenticate(self, email, password):
        """Login with email, password and get back a session cookie

        :type  email: str
        :param email: The email used for authentication
        :type  password: str
        :param password: The password used for authentication
        """
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
        return r.cookies

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

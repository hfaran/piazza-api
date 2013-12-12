"""Inspired by: https://gist.github.com/alexjlockwood/6797443"""

import urllib2
import json
import getpass
from cookielib import CookieJar


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
        self._cj = CookieJar()
        self._opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self._cj))

        if not email:
            email = raw_input("Email: ")
        password = getpass.getpass()
        self._authenticate(email, password)
        self._nid = network_id

    def _authenticate(self, email, password):
        """Login with email, password and get back a session cookie

        :type  email: str
        :param email: The email used for authentication
        :type  password: str
        :param password: The password used for authentication
        """
        login_url = 'https://piazza.com/logic/api?method=user.login'
        login_data = ('{{"method":"user.login","params":{{"email":"{}",'
                      '"pass":"{}"}}}}'.format(email, password))
        # If the user/password match, the server respond will contain a
        #  session cookie that you can use to authenticate future requests.
        login_resp = json.loads(
            self._opener.open(login_url, login_data).read())
        if login_resp["result"] != "OK":
            raise AuthenticationError(
                "Could not authenticate.\n{}".format(login_resp))

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
        if not nid:
            nid = self._nid
        content_url = 'https://piazza.com/logic/api?method=get.content'
        content_data = ('{{"method":"content.get","params":{{"cid":"{}",'
                        '"nid":"{}"}}}}'.format(cid, nid))
        return json.loads(self._opener.open(content_url, content_data).read())

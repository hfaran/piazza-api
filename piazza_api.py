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
        
    :type  network_id: str
    :param network_id: This is the ID of the network (or class) from which
        to query posts
    """
    def __init__(self, network_id):
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

    def enroll_students(self, student_emails, nid=None):
        """Enroll students in a network `nid`

        :type  student_emails: list of str
        :param student_emails: A listing of email addresses to enroll
            in the network (or class). This can be a list of length one.
        :type  nid: str
        :param nid: This is the ID of the network to add students
            to. This is optional and only to override the existing
            `network_id` entered when created the class
        """
        if self.cookies is None:
            raise NotAuthenticatedError("You must authenticate before making any other requests.")

        nid = nid if nid else self._nid

        content_url = self.base_api_url
        content_params = {"method": "network.update"}
        content_data = {
            "method": "network.update",
            "params": {
                "id": nid,
                "from": "ClassSettingsPage",
                "add_students": json.dumps(student_emails)
            }
        }

        return requests.post(
            content_url,
            data=json.dumps(content_data),
            params=content_params,
            cookies=self.cookies
        ).json()

    def get_all_users(self, nid=None):
        """Get a listing of each user in a network `nid`

        :type  nid: str
        :param nid: This is the ID of the network to add students
            to. This is optional and only to override the existing
            `network_id` entered when created the class
        :returns: Python object containing returned data
        """
        if self.cookies is None:
            raise NotAuthenticatedError("You must authenticate before making any other requests.")

        nid = nid if nid else self._nid

        content_url = self.base_api_url
        content_params = {"method": "network.get_all_users"}
        content_data = {
           "method": "network.get_all_users",
           "params": {
                "nid": nid
           }
        }

        r = requests.post(
            content_url,
            data=json.dumps(content_data),
            params=content_params,
            cookies=self.cookies
        ).json()

        if r.get(u'error'):
            raise Exception("Could not get users.\n{}".format(r))
        else:
            return r.get(u'result')

    def remove_users(self, user_ids, nid=None):
        """Remove users from a network `nid`

        :type  user_ids: list of str
        :param user_ids: a list of user ids. These are the same
            ids that are returned by get_all_users.
        :type  nid: str
        :param nid: This is the ID of the network to add students
            to. This is optional and only to override the existing
            `network_id` entered when created the class
        :returns: Python object containing returned data, a list
            of dicts of user data of all of the users remaining in
            the network after users are removed.
        """
        if self.cookies is None:
            raise NotAuthenticatedError("You must authenticate before making any other requests.")

        nid = nid if nid else self._nid

        content_url = self.base_api_url
        content_params = {"method": "network.update"}
        content_data = {
           "method": "network.update",
           "params": {
                "id": nid,
                "remove_users": user_ids
           }
        }

        r = requests.post(
            content_url,
            data=json.dumps(content_data),
            params=content_params,
            cookies=self.cookies
        ).json()

        if r.get(u'error'):
            raise Exception("Could not remove users.\n{}".format(r))
        else:
            return r.get(u'result')

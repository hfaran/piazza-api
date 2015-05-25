import getpass
import json

import requests

from piazza_api.exceptions import AuthenticationError, NotAuthenticatedError, \
    RequestError


class PiazzaRPC(object):
    """Unofficial Client for Piazza's Internal API

    Example:
        >>> p = PiazzaRPC("hl5qm84dl4t3x2")
        >>> p.user_login()
        Email: ...
        Password: ...
        >>> p.content_get(181)
        ...

    :type  network_id: str|None
    :param network_id: This is the ID of the network (or class) from which
        to query posts
    """
    def __init__(self, network_id=None):
        self._nid = network_id
        self.base_api_urls = {
            "logic": "https://piazza.com/logic/api",
            "main": "https://piazza.com/main/api",
        }
        self.cookies = None

    def user_login(self, email=None, password=None):
        """Login with email, password and get back a session cookie

        :type  email: str
        :param email: The email used for authentication
        :type  password: str
        :param password: The password used for authentication
        """
        email = raw_input("Email: ") if email is None else email
        password = getpass.getpass() if password is None else password

        login_data = {
            "method": "user.login",
            "params": {"email": email,
                       "pass": password}
        }
        # If the user/password match, the server respond will contain a
        #  session cookie that you can use to authenticate future requests.
        r = requests.post(
            self.base_api_urls["logic"],
            data=json.dumps(login_data),
        )
        if r.json()["result"] not in ["OK"]:
            raise AuthenticationError("Could not authenticate.\n{}"
                                      .format(r.json()))
        self.cookies = r.cookies

    def demo_login(self, auth=None, url=None):
        """Authenticate with a "Share Your Class" URL using a demo user.

        You may provide either the entire ``url`` or simply the ``auth``
        parameter.

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

    def content_get(self, cid, nid=None):
        """Get data from post `cid` in network `nid`

        :type  nid: str
        :param nid: This is the ID of the network (or class) from which
            to query posts. This is optional and only to override the existing
            `network_id` entered when created the class
        :type  cid: str|int
        :param cid: This is the post ID which we grab
        :returns: Python object containing returned data
        """
        r = self.request(
            method="content.get",
            data={"cid": cid},
            nid=nid
        )
        return self._handle_error(r, "Could not get post {}.".format(cid))

    def content_create(self, params):
        """Create a post or followup.

        :type  params: dict
        :param params: A dict of options to pass to the endpoint. Depends on
            the specific type of content being created.
        :returns: Python object containing returned data
        """
        r = self.request(
            method="content.create",
            data=params
        )
        return self._handle_error(r, "Could not create object {}.".format(
                                     repr(params)))

    def add_students(self, student_emails, nid=None):
        """Enroll students in a network `nid`.

        Piazza will email these students with instructions to
        activate their account.

        :type  student_emails: list of str
        :param student_emails: A listing of email addresses to enroll
            in the network (or class). This can be a list of length one.
        :type  nid: str
        :param nid: This is the ID of the network to add students
            to. This is optional and only to override the existing
            `network_id` entered when created the class
        :returns: Python object containing returned data, a list
            of dicts of user data of all of the users in the network
            including the ones that were just added.
        """
        r = self.request(
            method="network.update",
            data={
                "from": "ClassSettingsPage",
                "add_students": student_emails
            },
            nid=nid,
            nid_key="id"
        )
        return self._handle_error(r, "Could not add users.")

    def get_all_users(self, nid=None):
        """Get a listing of data for each user in a network `nid`

        :type  nid: str
        :param nid: This is the ID of the network to get users
            from. This is optional and only to override the existing
            `network_id` entered when created the class
        :returns: Python object containing returned data, a list
            of dicts containing user data.
        """
        r = self.request(
            method="network.get_all_users",
            nid=nid
        )
        return self._handle_error(r, "Could not get users.")

    def get_users(self, user_ids, nid=None):
        """Get a listing of data for specific users `user_ids` in
        a network `nid`

        :type  user_ids: list of str
        :param user_ids: a list of user ids. These are the same
            ids that are returned by get_all_users.
        :type  nid: str
        :param nid: This is the ID of the network to get students
            from. This is optional and only to override the existing
            `network_id` entered when created the class
        :returns: Python object containing returned data, a list
            of dicts containing user data.
        """
        r = self.request(
            method="network.get_users",
            data={"ids": user_ids},
            nid=nid
        )
        return self._handle_error(r, "Could not get users.")

    def remove_users(self, user_ids, nid=None):
        """Remove users from a network `nid`

        :type  user_ids: list of str
        :param user_ids: a list of user ids. These are the same
            ids that are returned by get_all_users.
        :type  nid: str
        :param nid: This is the ID of the network to remove students
            from. This is optional and only to override the existing
            `network_id` entered when created the class
        :returns: Python object containing returned data, a list
            of dicts of user data of all of the users remaining in
            the network after users are removed.
        """
        r = self.request(
            method="network.update",
            data={"remove_users": user_ids},
            nid=nid,
            nid_key="id"
        )
        return self._handle_error(r, "Could not remove users.")

    def get_my_feed(self, limit=150, offset=20, sort="updated", nid=None):
        """Get my feed

        :type limit: int
        :param limit: Number of posts from feed to get, starting from ``offset``
        :type offset: int
        :param offset: Offset starting from bottom of feed
        :type sort: str
        :param sort: How to sort feed that will be retrieved; only current
            known value is "updated"
        :type  nid: str
        :param nid: This is the ID of the network to get the feed
            from. This is optional and only to override the existing
            `network_id` entered when created the class
        """
        r = self.request(
            method="network.get_my_feed",
            nid=nid,
            data=dict(
                limit=limit,
                offset=offset,
                sort=sort
            )
        )
        return self._handle_error(r, "Could not retrieve your feed.")

    def filter_feed(self, updated=False, following=False, folder=False,
                    filter_folder="", sort="updated", nid=None):
        """Get filtered feed

        Only one filter type (updated, following, folder) is possible.

        :type  nid: str
        :param nid: This is the ID of the network to get the feed
            from. This is optional and only to override the existing
            `network_id` entered when created the class
        :type sort: str
        :param sort: How to sort feed that will be retrieved; only current
            known value is "updated"
        :type updated: bool
        :param updated: Set to filter through only posts which have been updated
            since you last read them
        :type following: bool
        :param following: Set to filter through only posts which you are
            following
        :type folder: bool
        :param folder: Set to filter through only posts which are in the
            provided ``filter_folder``
        :type filter_folder: str
        :param filter_folder: Name of folder to show posts from; required
            only if ``folder`` is set
        """
        assert sum([updated, following, folder]) == 1
        if folder:
            assert filter_folder

        if updated:
            filter_type = dict(updated=1)
        elif following:
            filter_type = dict(following=1)
        else:
            filter_type = dict(folder=1, filter_folder=filter_folder)

        r = self.request(
            nid=nid,
            method="network.filter_feed",
            data=dict(
                sort=sort,
                **filter_type
            )
        )
        return self._handle_error(r, "Could not retrieve filtered feed.")

    def search(self, query, nid=None):
        """Search for posts with ``query``

        :type  nid: str
        :param nid: This is the ID of the network to get the feed
            from. This is optional and only to override the existing
            `network_id` entered when created the class
        :type query: str
        :param query: The search query; should just be keywords for posts
            that you are looking for
        """
        r = self.request(
            method="network.search",
            nid=nid,
            data=dict(query=query)
        )
        return self._handle_error(r, "Search with query '{}' failed."
                                  .format(query))

    def get_stats(self, nid=None):
        """Get statistics for class

        :type  nid: str
        :param nid: This is the ID of the network to get stats
            from. This is optional and only to override the existing
            `network_id` entered when created the class
        """
        r = self.request(
            api_type="main",
            method="network.get_stats",
            nid=nid,
        )
        return self._handle_error(r, "Could not retrieve stats for class.")

    def get_user_profile(self):
        """Get profile of the current user"""
        r = self.request(method="user_profile.get_profile")
        return self._handle_error(r, "Could not get user profile.")

    def request(self, method, data=None, nid=None, nid_key='nid',
                api_type="logic", return_response=False):
        """Get data from arbitrary Piazza API endpoint `method` in network `nid`

        :type  method: str
        :param method: An internal Piazza API method name like `content.get`
            or `network.get_users`
        :type  data: dict
        :param data: Key-value data to pass to Piazza in the request
        :type  nid: str
        :param nid: This is the ID of the network to which the request
            should be made. This is optional and only to override the
            existing `network_id` entered when creating the class
        :type  nid_key: str
        :param nid_key: Name expected by Piazza for `nid` when making request.
            (Usually and by default "nid", but sometimes "id" is expected)
        :returns: Python object containing returned data
        :type return_response: bool
        :param return_response: If set, returns whole :class:`requests.Response`
            object rather than just the response body
        """
        self._check_authenticated()

        nid = nid if nid else self._nid
        if data is None:
            data = {}

        response = requests.post(
            self.base_api_urls[api_type],
            data=json.dumps({
                "method": method,
                "params": dict({nid_key: nid}, **data)
            }),
            cookies=self.cookies
        )
        return response if return_response else response.json()

    ###################
    # Private Methods #
    ###################

    def _check_authenticated(self):
        """Check that we're logged in and raise an exception if not.

        :raises: NotAuthenticatedError
        """
        if self.cookies is None:
            raise NotAuthenticatedError("You must authenticate before "
                                        "making any other requests.")

    def _handle_error(self, result, err_msg):
        """Check result for error

        :type result: dict
        :param result: response body
        :type err_msg: str
        :param err_msg: The message given to the :class:`RequestError` instance
            raised
        :returns: Actual result from result
        :raises RequestError: If result has error
        """
        if result.get(u'error'):
            raise RequestError("{}\nResponse: {}".format(
                err_msg,
                json.dumps(result, indent=2)
            ))
        else:
            return result.get(u'result')

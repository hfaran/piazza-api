from .rpc import PiazzaRPC


class Network(object):
    """Abstraction for a Piazza "Network" (or class)

    :param network_id: ID of the network
    :param cookies: RequestsCookieJar containing cookies used for authentication
    """
    def __init__(self, network_id, cookies):
        self._nid = network_id
        self._rpc = PiazzaRPC(network_id=self._nid)
        self._rpc.cookies = cookies

    #########
    # Posts #
    #########

    def get_post(self, cid):
        """Get data from post `cid`

        :type  cid: str|int
        :param cid: This is the post ID to get
        :rtype: dict
        :returns: Dictionary with all data on the post
        """
        return self._rpc.content_get(cid)

    def iter_all_posts(self):
        """
        TODO implement and remove
        Can do this by looking at the feed and grabbing all ids
        of posts from feed; the ids, work for getting posts
        :return:
        """
        pass

    #########
    # Users #
    #########

    def get_users(self, user_ids):
        """Get a listing of data for specific users ``user_ids`` in
        this network

        :type  user_ids: list of str
        :param user_ids: a list of user ids. These are the same
            ids that are returned by get_all_users.
        :returns: Python object containing returned data, a list
            of dicts containing user data.
        :rtype: list
        """
        return self._rpc.get_users(user_ids)

    def iter_users(self, user_ids):
        """Same as ``Network.get_users``, but returns an iterable instead

        :rtype: listiterator
        """
        return iter(self.get_users(user_ids=user_ids))

    def get_all_users(self):
        """Get a listing of data for all users in this network

        :rtype: list
        :returns: Python object containing returned data, a list
            of dicts containing user data.
        """
        return self._rpc.get_all_users()

    def iter_all_users(self):
        """Same as ``Network.get_all_users``, but returns an iterable instead

        :rtype: listiterator
        """
        return iter(self.get_all_users())

    def add_students(self, student_emails):
        """Add students with ``student_emails`` to the network

        Piazza will email these students with instructions to
        activate their account.

        :type  student_emails: list of str
        :param student_emails: A listing of email addresses to enroll
            in the network (or class). This can be a list of length one.
        :rtype: list
        :returns: Python object containing returned data, a list
            of dicts of user data of all of the users in the network
            including the ones that were just added.
        """
        return self._rpc.add_students(student_emails)

    def remove_users(self, user_ids):
        """Remove users with ``user_ids`` from this network

        :type  user_ids: list of str
        :param user_ids: a list of user ids. These are the same
            ids that are returned by get_all_users.
        :rtype: list
        :returns: Python object containing returned data, a list
            of dicts of user data of all of the users remaining in
            the network after users are removed.
        """
        return self._rpc.remove_users(user_ids)

    ########
    # Feed #
    ########

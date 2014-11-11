from .rpc import PiazzaRPC


class Piazza(object):
    """Unofficial Client for Piazza's Internal API"""
    def __init__(self):
        self._rpc_api = None

    def user_login(self, email=None, password=None):
        """Login with email, password and get back a session cookie

        :type  email: str
        :param email: The email used for authentication
        :type  password: str
        :param password: The password used for authentication
        """
        self._rpc_api = PiazzaRPC()
        self._rpc_api.user_login(email=email, password=password)

    def demo_login(self, auth=None, url=None):
        """Authenticate with a "Share Your Class" URL using a demo user.

        You may provide either the entire ``url`` or simply the ``auth``
        parameter.

        :param url: Example - "https://piazza.com/demo_login?nid=hbj11a1gcvl1s6&auth=06c111b"
        :param auth: Example - "06c111b"
        """
        self._rpc_api = PiazzaRPC()
        self._rpc_api.demo_login(auth=auth, url=url)

    def network(self, network_id):
        """Returns Network instance for ``network_id``

        :type  nid: str
        :param nid: This is the ID of the network (or class) from which
            to query posts. This can be found by visiting your class page
            on Piazza's web UI and grabbing it from
            https://piazza.com/class/{network_id}
        """
        pass

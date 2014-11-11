from .rpc import PiazzaRPC
from .exceptions import NotAuthenticatedError
from .network import Network


class Piazza(object):
    """Unofficial Client for Piazza's Internal API"""
    def __init__(self):
        self._cookies = None

    def user_login(self, email=None, password=None):
        """Login with email, password and get back a session cookie

        :type  email: str
        :param email: The email used for authentication
        :type  password: str
        :param password: The password used for authentication
        """
        rpc_api = PiazzaRPC()
        rpc_api.user_login(email=email, password=password)
        self._cookies = rpc_api.cookies

    def demo_login(self, auth=None, url=None):
        """Authenticate with a "Share Your Class" URL using a demo user.

        You may provide either the entire ``url`` or simply the ``auth``
        parameter.

        :param url: Example - "https://piazza.com/demo_login?nid=hbj11a1gcvl1s6&auth=06c111b"
        :param auth: Example - "06c111b"
        """
        rpc_api = PiazzaRPC()
        rpc_api.demo_login(auth=auth, url=url)
        self._cookies = rpc_api.cookies

    def network(self, network_id):
        """Returns Network instance for ``network_id``

        :type  nid: str
        :param nid: This is the ID of the network (or class) from which
            to query posts. This can be found by visiting your class page
            on Piazza's web UI and grabbing it from
            https://piazza.com/class/{network_id}
        """
        self._ensure_authenticated()
        return Network(network_id, self._cookies)

    def _ensure_authenticated(self):
        if self._cookies is None:
            raise NotAuthenticatedError("You must log in first.")

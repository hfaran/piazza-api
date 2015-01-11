from .rpc import PiazzaRPC
from .network import Network


class Piazza(object):
    """Unofficial Client for Piazza's Internal API

    :type piazza_rpc: :class:`PiazzaRPC`
    """
    def __init__(self, piazza_rpc=None):
        self._rpc_api = piazza_rpc if piazza_rpc else None

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
        """Returns :class:`Network` instance for ``network_id``

        :type  network_id: str
        :param network_id: This is the ID of the network.
            This can be found by visiting your class page
            on Piazza's web UI and grabbing it from
            https://piazza.com/class/{network_id}
        """
        self._ensure_authenticated()
        return Network(network_id, self._rpc_api.cookies)

    def get_user_profile(self):
        """Get profile of the current user

        :returns: Profile of currently authenticated user
        :rtype: dict
        """
        return self._rpc_api.get_user_profile()

    def get_user_classes(self):
        """Get list of the current user's classes. This is a subset of
        ``get_user_profile``.

        :returns: Classes of currently authenticated user
        :rtype: list
        """
        raw_classes = self.get_user_profile().get('all_classes').values()

        classes = []
        for rawc in raw_classes:
            c = {k: rawc[k] for k in ['name', 'num', 'term']}
            c['nid'] = rawc['id']
            c['is_ta'] = rawc.get('is_ta', False)
            classes.append(c)

        return classes

    def _ensure_authenticated(self):
        self._rpc_api._check_authenticated()

class RequestError(Exception):
    """RequestError"""


class AuthenticationError(Exception):
    """AuthenticationError"""


class NotAuthenticatedError(Exception):
    """NotAuthenticatedError"""


class NoNetworkIDError(Exception):
    """No Network ID (nid) provided"""

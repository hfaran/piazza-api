from .rpc import PiazzaRPC


class Network(object):
    def __init__(self, network_id, cookies):
        self._nid = network_id
        self._rpc = PiazzaRPC(network_id=self._nid)
        self._rpc.cookies = cookies

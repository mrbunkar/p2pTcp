from abc import ABC, abstractmethod

"""
Templates for handshake and OnPeer classes. User can decide how they want to
handle handshake and on peer.
"""

class Handshake(ABC):

    @abstractmethod
    def do(self, peer) -> None:
        """
        Will be implemented by users of this class.
        """
        return None
    
    def default_do(peer) -> None:
        """
        Default handshake function. Does nothing
        """
        return
    
class OnPeer(ABC):

    @abstractmethod
    def on_peer(self, peer) -> None:
        """
        Will be implemented by users of this class
        """
        return None
    
    def default_on_peer(peer) -> None:
        """
        Default on peer function. Does nothing
        """
        return
    
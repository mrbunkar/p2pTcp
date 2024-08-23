from abc import ABC, abstractmethod

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
    
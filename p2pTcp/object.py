from abc import ABC, abstractmethod

class Handshake(ABC):

    @abstractmethod
    async def do(self, peer) -> None:
        """
        Will be implemented by users of this class.
        """
        return None
    
    async def default_do(peer) -> None:
        """
        Default handshake function. Does nothing
        """
        return
    
class OnPeer(ABC):

    @abstractmethod
    async def on_peer(self, peer) -> None:
        """
        Will be implemented by users of this class
        """
        return None
    
    async def default_on_peer(peer) -> None:
        """
        Default on peer function. Does nothing
        """
        return
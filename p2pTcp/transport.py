import asyncio
import io
import logging
from p2pTcp.object import Handshake, OnPeer
from p2pTcp.peer import TcpPeer

class TcpOpts:

    def __init__(self, handShake = Handshake.default_do, on_peer = OnPeer.default_on_peer):
        self.hand_shake = handShake
        self.on_peer = on_peer

class TcpTransport:
    
    def __init__(self, host = "localhost", port = 3030, opts = TcpOpts()):
        self.host = host
        self.port = port
        self.opts = opts
        self.rpc_queue = asyncio.Queue()

    async def listen(self):
        """
        Opens the given port for listing upcoming connections. Server is in passive open
        mode.
        """

        self.server = await asyncio.start_server(self._handle_connection,self.host, self.port)

        logging.info("listening on port: %s" % self.port)
        async with self.server:
            await self.server.serve_forever()
    
    async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        """
        Handle upcoming connection and will provide TcpPeer object. 
        """
        peer = TcpPeer(reader, writer, self)
        logging.info(f"Connected to PEER: {writer.get_extra_info('peername')}")
        try:
            self.opts.hand_shake(peer)
            self.opts.on_peer(peer)
        except Exception as e:
            logging.error(f"Error handling connection from {writer.get_extra_info('peername')}: {e}")
            peer.close()
            return
        
        asyncio.create_task(peer.read())

    async def make_connection(self, host, port):
        try:
            reader, writer = await asyncio.open_connection(host, port)
            await self._handle_connection(reader, writer)
        except asyncio.TimeoutError:
            return ConnectionError(f"Failed to connect to {self.host}:{self.port}")

    async def close(self):
        print("Closing the server")
        try:
            self.server.close()
            # await self.server.wait_closed()
            # @TODO: gracefully shutdown
            logging.info(f"Server running on port: {self.host}:{self.port} is closed")
        except Exception as err:
            raise Exception

    async def consume(self):
        return await self.rpc_queue.get()
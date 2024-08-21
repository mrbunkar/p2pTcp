import asyncio
import io
import logging
from p2pTcp.object import Handshake, OnPeer
from p2pTcp.data_type import RPC
from p2pTcp.encoding import Encoder

logging.basicConfig(level = logging.INFO)

class WaitGroup:
    def __init__(self):
        self.counter = 0
        self.lock = asyncio.Lock()
        self.condition = asyncio.Condition(self.lock)

    async def add(self, count=1):
        async with self.lock:
            self.counter += count

    async def done(self):
        
        async with self.lock:
            self.counter -= 1
            if self.counter == 0:
                self.condition.notify_all()

    async def wait(self):
        async with self.condition:
            while self.counter > 0:
                await self.condition.wait()

class TcpPeer:

    """
    TcpPeer represents the remote node to which server is connected.
    Will be used for reading and writing the data from the remote node.
    """

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.wg = WaitGroup()
        self.rpc_queue = asyncio.Queue()
        self.addr = self.writer.get_extra_info("peername")

    async def write(self, data: io.BytesIO):
        pass

    async def read(self):
        while True:
            rpc = RPC()
            err = await Encoder.decode(self,rpc)

            if isinstance(err, EOFError):
                logging.info(f"Connection closed by peer: {self.addr}")
                break

            if err is not None:
                logging.error(f"Error decoding message from:[{self.addr}], error:{err}")
                continue

            rpc.From = self.addr
            await self.rpc_queue.put(rpc)
            
            if rpc.Stream:
                await self.wg.add(1)
                logging.info("Incoming stream, waiting for the stream to process")
                await self.wg.wait()
                logging.info("Stream processed, lock released")
                continue

    async def consume(self):

        """
        Consume function will give access to RPC, And accordingly user can process the input message
        """
        return await self.rpc_queue.get()

    def close(self):
        self.writer.close()

class TcpOpts:

    def __init__(self, handShake = Handshake.default_do, on_peer = OnPeer.default_on_peer):
        self.hand_shake = handShake
        self.on_peer = on_peer

class TcpTransport:
    
    def __init__(self, host = "localhost", port = 3030, opts = TcpOpts()):
        self.host = host
        self.port = port
        self.opts = opts

    async def listen(self):
        """
        Opens the given port for listing upcoming connections. Server is in passive open
        mode.
        """

        self.server = await asyncio.start_server(self._handle_incoming_connection,self.host, self.port)

        logging.info("listening on port: %s" % self.port)
        async with self.server:
            await self.server.serve_forever()
    
    async def _handle_incoming_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

        """
        Handle upcoming connection and will provide TcpPeer object. 
        """
        peer = TcpPeer(reader, writer)
        logging.info(f"Connected to PEER: {writer.get_extra_info('peername')}")
        try:
            await self.opts.hand_shake(peer)
            await self.opts.on_peer(peer)
        except Exception as e:
            logging.error(f"Error handling connection from {writer.get_extra_info('peername')}: {e}")
            peer.close()
            return
        
        await peer.read()
        
    async def _handle_outgoing_connection(self,reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = TcpPeer(reader, writer)
        logging.info(f"Connected to PEER: {writer.get_extra_info('peername')}")
        try:
            await self.opts.hand_shake(peer)
            await self.opts.on_peer(peer)
        except Exception as e:
            logging.error(f"Error handling connection from {writer.get_extra_info('peername')}: {e}")
            peer.close()
            return
        
        await peer.read()

    async def make_connection(self, host, port):
        try:
            reader, writer = await asyncio.open_connection(host, port)
            await self._handle_outgoing_connection(reader, writer)
        except asyncio.TimeoutError:
            return ConnectionError(f"Failed to connect to {self.host}:{self.port}")

    async def close(self):
        self.server.close()
        await self.server.wait_closed()
        logging.info(f"Server running on port: {self.host}:{self.port} is closed")

    
import asyncio
import logging
from p2pTcp.encoding import Encoder
from p2pTcp.data_type import RPC
import io
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

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, transport):
        self.reader = reader
        self.writer = writer
        self.wg = WaitGroup()
        self.transport = transport
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
            await self.transport.rpc_queue.put(rpc)
            
            if rpc.Stream:
                await self.wg.add(1)
                logging.info("Incoming stream, waiting for the stream to process")
                await self.wg.wait()
                logging.info("Stream processed, lock released")
                continue

    async def read_stream(self, expected_length) -> io.BytesIO:
        stream_data = io.BytesIO()
        while expected_length > 0:
            chunk = await self.reader.read(min(1024, expected_length))
            if not chunk:
                break
            stream_data.write(chunk)
            expected_length -= len(chunk)
        stream_data.seek(0)
        return stream_data

    def close(self):
        self.writer.close()
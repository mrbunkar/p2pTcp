import io
import asyncio
from p2pTcp.data_type import RPC, Message, IncomingStream
import json

class Encoder:
    async def encode(peer, data: io.BytesIO):
        

        pass

    async def decode(peer, rpc: RPC) -> io.BytesIO:

        try:
            data = await peer.reader.read(1024)

            if not data:
                return EOFError("Connection closed")

            message = json.loads(data.decode())
            print(type(message))
            print(message)

            if message["stream"] == IncomingStream:
                rpc.Peer = peer
        except Exception as err:
            return err
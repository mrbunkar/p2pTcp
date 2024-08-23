import io
import asyncio
from p2pTcp.data_type import RPC, Message, IncomingStream
import json

class Encoder:
    async def encode(peer, data: io.BytesIO):
        
        try:
            peer.writer.write(data.getvalue()) 
            await peer.writer.drain()
            return None
        except Exception as err:
            return err

    async def decode(peer):

        try:
            data = await peer.reader.read(1024)

            if not data:
                return None,EOFError("Connection closed")
            
            rpc = RPC.deserialize(data)
            rpc.Stream = False
            if rpc.Type == IncomingStream:
                rpc.Peer = peer
                rpc.Stream = True
            return rpc, None
        except Exception as err:
            return None,err
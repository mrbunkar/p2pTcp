import unittest
import asyncio
from p2pTcp.transport import TcpTransport, TcpOpts
from p2pTcp.data_type import RPC, MessageType


class TestP2PStream(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.peers = {}
        self.opts = TcpOpts(on_peer=self.on_peer)
        
        self.server1 = TcpTransport(host="localhost", port=3030, opts=self.opts)
        self.server2 = TcpTransport(host="localhost", port=3000, opts=self.opts)
        
        asyncio.create_task(self.server1.listen())
        asyncio.create_task(self.server2.listen())
        await asyncio.sleep(1)
        
        await self.server2.make_connection("localhost", 3030)
        await asyncio.sleep(1)

    def on_peer(self,peer):
        self.peers[peer.Addr] = peer

    async def test_streaming(self):
        pass

    async def asyncTearDown(self):
        await self.server1.close()
        await self.server2.close()

if __name__ == "__main__":
    unittest.main()
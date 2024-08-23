import unittest
import asyncio
from p2pTcp.transport import TcpTransport, TcpOpts
from p2pTcp.data_type import RPC, MessageType

class TestP2PCommunication(unittest.IsolatedAsyncioTestCase):

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

    def on_peer(self, peer):
        self.peers[peer.addr] = peer

    async def test_message_sending(self):
        """Test sending a message between peers."""
        
        for addr, peer in self.peers.items():
            rpc = RPC(Payload=b"testing the stream messages", Type=MessageType)
            await peer.writeMessage(rpc)
            print(f"Message sent to {addr}")

        await asyncio.sleep(1)  # Give some time for the message to be processed

        # Consume the message from the server1's queue
        rpc = await self.server1.consume()
        print(rpc.Payload.decode())
        self.assertEqual(rpc.Payload.decode(), "testing the stream messages")

    async def asyncTearDown(self):
        await self.server1.close()
        await self.server2.close()

if __name__ == "__main__":
    unittest.main()

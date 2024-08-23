from p2pTcp.transport import TcpTransport, TcpOpts
from p2pTcp.data_type import RPC, IncomingStream, MessageType
import asyncio
import io

peers = {}
def on_peer(peer):
    peers[peer.addr] = peer

async def run_server2():
    await asyncio.sleep(1)

    opts = TcpOpts(
        on_peer=on_peer,
    )
    server = TcpTransport(
        host="localhost",
        port = 3000,
        opts=opts,
    )
    asyncio.create_task(server.listen())
    await server.make_connection("localhost", 3030)
    await asyncio.sleep(1)

    for addr,peer in peers.items():
        rpc = RPC(
            Payload= b"testing the stream messages",
            Type = MessageType,
        )
        # data = io.BytesIO(b"testing the stream messages")
        await peer.writeMessage(rpc)
        print(f"Message sent to {addr}")

async def _loop(server):
    await asyncio.sleep(3)
    while True:
        print("Waiting for RPC")
        rpc = await server.consume()
        print(f"Received message: {rpc.Payload.decode()}")

async def run(server: TcpTransport):

    await asyncio.gather(server.listen(), run_server2(), _loop(server))


if __name__ == "__main__":
    server1 = TcpTransport(
        host = "localhost",
        port = 3030
    )
    asyncio.run(run(server1))

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
            Payload= b"Upcoming stream",
            Type = IncomingStream,
            Size = 28
        )
        
        await peer.writeMessage(rpc)
        data = io.BytesIO(b"Testing the contnouse stream")
        print(f"Message sent to {addr}")
        await asyncio.sleep(0.5)
        await peer.writeStream(data)
        print("Stream send over the network")

    await server.close()

async def _loop(server):
    await asyncio.sleep(3)
    while True:
        print("Waiting for RPC")
        rpc = await server.consume()
        print(f"Received message: {rpc.Payload.decode()}, {rpc.Size}")
        
        if rpc.Type == IncomingStream:
            peer = rpc.Peer
            print(peer)
            data = await peer.read_stream(rpc.Size)
            print(data.getvalue().decode())
        await asyncio.sleep(1)
        print(1)
        await server.close()
        break

async def run(server: TcpTransport):

    await asyncio.gather(server.listen(), run_server2(), _loop(server))


if __name__ == "__main__":
    server1 = TcpTransport(
        host = "localhost",
        port = 3030
    )
    asyncio.run(run(server1))

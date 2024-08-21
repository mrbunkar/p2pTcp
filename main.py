from p2pTcp.transport import TcpTransport, TcpOpts
import asyncio


if __name__ == "__main__":
    server1 = TcpTransport(
        host = "localhost",
        port = 3030
    )
    asyncio.run(server1.listen())

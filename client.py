from p2pTcp.transport import TcpTransport
import asyncio

async def main(server: TcpTransport):
    await server.make_connection("localhost", 3030)

if __name__ == "__main__":
    server1 = TcpTransport(
        host = "localhost",
        port = 3000
    )
    asyncio.run(main(server1))
    

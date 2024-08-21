
# p2pTcp: A Simple Peer-to-Peer Connection Library 

Overview

p2pTcp is a Python library designed to facilitate peer-to-peer (P2P) communication. It simplifies the process of establishing, managing, and interacting with P2P connections, allowing for easy message and stream handling between peers.

## Feature

- Easy to Use: Simple API to establish and manage P2P connections.
- Asynchronous Operations: Built using Python's asyncio, enabling non-blocking I/O.
- Message and Stream Handling: Handles both message passing and stream processing between peers.
- Customizable Handshake and Peer Event Handling: Customize how your application interacts with new peers and manages connections.

## Installation


To install the library, simply clone the repository:

```bash
Copy code
git clone https://github.com/your-repo/p2pTcp.git
cd p2pTcp
```

## Usage

Below is a basic example demonstrating how to set up a simple TCP server using the p2pTcp library:

# Server Example
Below is a basic example demonstrating how to set up a simple TCP server using the p2pTcp library:

```python
from p2pTcp.transport import TcpTransport
import asyncio

if __name__ == "__main__":
    server = TcpTransport(
        host="localhost",
        port=3030
    )
    asyncio.run(server.listen())
```
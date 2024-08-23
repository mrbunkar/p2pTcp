from typing import Any
import io


IncomingStream = b'\x01'
Message = b'\x02'
"""
User can define different types of message types and process them accordingly.
"""

class Message(object):
    From = Any
    Payload = bytes

from typing import Any
import io

# Message types
IncomingStream = b'\x01'
MessageType = b'\x02'

class RPC:
    def __init__(self, From: str = "", Payload: bytes = b"", Type: bytes = MessageType, Size: int = 0):
        self.From = From
        self.Payload = Payload
        self.Type = Type
        self.Size = Size

    def serialize(self) -> io.BytesIO:
        """
        Converts the RPC object into a bytes stream for sending over the network.
        The format will be: Payload\r\nType\r\nSize (if it's a stream)
        """
        raw_data = self.Payload + b"\r\n" + self.Type
        
        if self.Type == IncomingStream:
            raw_data += b"\r\n" + self.Size.to_bytes(4, byteorder='big')  # Assuming Size is a 4-byte integer

        return io.BytesIO(raw_data)

    @classmethod
    def deserialize(cls, data: bytes):
        """
        Given the bytes, convert them back to an RPC object.
        The format should match what was serialized: Payload\r\nType\r\nSize (if applicable)
        """
        parts = data.split(b"\r\n")
        
        if len(parts) < 2:
            raise ValueError("Invalid data format for RPC deserialization")

        payload = parts[0]
        type_ = parts[1]
        size = 0

        if type_ == IncomingStream:
            if len(parts) < 3:
                raise ValueError("Invalid data format for stream RPC deserialization")
            size = int.from_bytes(parts[2], byteorder='big')

        return cls(Payload=payload, Type=type_, Size=size)

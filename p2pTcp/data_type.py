from typing import Any

IncomingStream = b'\x01'
"""
User can define different types of message types and process them accordingly.
"""

class Message(object):
    From = Any
    Payload = bytes

class RPC(object):
    From: str = ""
    Payload = b""
    Stream = False
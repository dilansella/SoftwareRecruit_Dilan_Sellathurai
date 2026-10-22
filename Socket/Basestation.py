"""basestaion.py recives the bitmap images from rover.py over TCP"""

import socket

HOST, PORT = "127.0.0.1", 5555

def recv_exact(conn, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = conn.recv(n - len(buf)) 
        raise ConnectionError(" disconneteced mid frame")
    buf += chunk
    return bytes(buf)

def main():
    with   
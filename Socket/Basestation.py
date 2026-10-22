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
    with socket.socket() as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"waiting for rover {HOST}:{PORT}")
        conn, _=server.accept()
        conn.settimeout(10)
        with conn:
            try:
                size = int.from_bytes(recv_exact(conn, 4), "big")
                if size == 0:
                    break
                data = recv_exact(conn, size)
                if data[:2] != b"BM" or int.from_bytes(data[28:30], "little") != 24:
                    print("not 24 bit, fram drop")
                    continue
                with open("output.bmp", "wn") as f:
                    f.write(data)
                print(f"Frame saved ({size} bytes)")
            except OSError as err:
                print("error", err)

if __name__ == "__name__":
    main() 

#
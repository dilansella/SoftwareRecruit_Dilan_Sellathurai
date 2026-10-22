"""rover.py streams the png of the flower (utah) to basestation.py as a framed image over TCP, reasoning for TCP explained in README file"""

import socket

HOST, PORT = "127.0.0.1", 5555
IMAGE_FILE = "Utah.bmp"
FRAMES = 3
RECIEVERS = ["192.168.16.2", "192.168.16.4", "192.168.16.5", "192.168.16.9", "192.168.16.10"]


def send_stream(host, image):
    with socket.socket() as s:
        s.settimeout(5)
        s.connect((host, PORT))
        for i in range(FRAMES):
            s.sendall(len(image).to_bytes(4, "big") + image)
            print(f"Sent frame {i+1} to {host}")
        s.sendall((0).to_bytes(4, "big"))

def broadcastImage(image):
    for ip in RECIEVERS:
        try:
            send_stream(ip, image)
        except OSError as err:
            print(f"{ip} failed: {err}")

def main():
    try:
        with open(IMAGE_FILE, "rb") as f:
            image = f.read()
        send_stream(HOST, image)
    except FileNotFoundError:
        print(f"Cannot find {IMAGE_FILE} in this folder")
    except ConnectionRefusedError:
        print("Conncection refused - start basestation first")
    except socket.timeout:
        print("Timed out Talking to the base station")

if __name__ == "__main__":
    main()
import socket

HOST = "127.0.0.1"
PORT = 65000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sckt:
    sckt.bind((HOST, PORT))
    sckt.listen()
    print(f"Server listenning on {HOST}:{PORT}")
    conn, addr = sckt.accept()
    # for now it's handling with only one connection, later it will be improved to deal with more than one
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                print(f'Received data from {addr}: {data}')
            conn.sendall(data)
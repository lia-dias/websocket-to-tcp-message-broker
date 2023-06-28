import socket
import hashlib
import base64

HOST = "127.0.0.1"
PORT = 65000

def parseHandshakeProtocol(handshake_message: str):
    handshake_headers = {}
    handshake_headers_list = handshake_message.split("\\r\\n")
    for header in handshake_headers_list:
        if( ":" in header):
            key, value = header.split(":", 1)
            handshake_headers[key] = value.strip()
    return handshake_headers

def validadeWSHandshakeHeaders(handshake_headers: dict):
    connection_header = handshake_headers.get('Connection', None)
    upgrade_header = handshake_headers.get('Upgrade', None)
    web_socket_key_header = handshake_headers.get('Sec-WebSocket-Key', None)

    if( connection_header != "Upgrade" or upgrade_header != "websocket"):
        raise Exception("Aborted: No WS connection provided")
    if ( web_socket_key_header  == None or len(web_socket_key_header) == 0 ):
        raise Exception("Aborted: No WS key provided")

def generateWSAcceptanceHeader(handshake_web_socket_key: str):
    WS_HASH_PROTOCOL = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    handshake_web_socket_acceptance = bytes(handshake_web_socket_key + WS_HASH_PROTOCOL, "utf-8")
    handshake_web_socket_acceptance = hashlib.sha1(handshake_web_socket_acceptance).digest()
    handshake_web_socket_acceptance = base64.b64encode(handshake_web_socket_acceptance)
    return str(handshake_web_socket_acceptance, "utf-8")


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sckt:
        sckt.bind((HOST, PORT))
        sckt.listen()
        print(f"Server listenning on {HOST}:{PORT}")
        conn, addr = sckt.accept()
        # for now it's handling with only one connection, later it will be improved to deal with more than one
        with conn:
            print(f"Connected by {addr}")
            handshake_message = str(conn.recv(1024))
            handshake_headers = parseHandshakeProtocol(handshake_message)
            try:
                validadeWSHandshakeHeaders(handshake_headers)
                handshake_web_socket_acceptance = generateWSAcceptanceHeader(handshake_headers['Sec-WebSocket-Key'])
                handshake_response = 'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n' % handshake_web_socket_acceptance
                conn.sendall(bytes(handshake_response, "utf-8"))
            except Exception as e:
                print(e)
                conn.sendall(bytes(str(e), "utf-8"))
                sckt.close()
                exit()
            
            while True:
                data = conn.recv(1024)
                if not data:
                    sckt.close()
                    break
                else:
                    key = data[2:6]
                    value = data[6:]
                    final_message = bytearray()
                    for i in range(len(data[6:])):
                        final_message.append(value[i] ^ key[i & 0x3])
                    print(final_message)
                    response = bytearray()
                    response_body = bytes('Message received', "utf-8")
                    response.append(0x1)
                    response.append(len(response_body))
                    for byte in response_body:
                        response.append(byte)
                    print(response)
                    conn.sendall(response)
                # conn.sendall(data)
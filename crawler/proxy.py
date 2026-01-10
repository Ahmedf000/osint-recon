import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receiver_first):
    server = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except socket.error as msg:
        print(f"Bind failed. Error Code : {msg}")
        sys.exit(1)
    except Exception as err:
        print(f"Bind failed. Error Code: {err}")
        sys.exit(1)

    print(f"[*]Listening on {local_host}:{local_port}")
    server.listen(5)

    while True:
        client_addr, addr = server.accept()
        print(f"[*]Connected {addr}")
        proxy_thread = threading.Thread(target=proxy_handler(), args=(client_socket,remote_host,remote_port,receive_first))

        proxy_thread.start()






def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    pass

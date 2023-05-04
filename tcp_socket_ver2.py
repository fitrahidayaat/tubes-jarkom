import socket
import os

HOST = '127.0.0.1'  # Alamat IP localhost
PORT = 8080        # Port yang digunakan

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Web server berjalan di http://{HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print('Terhubung dengan', addr)
            request = conn.recv(1024)
            request_str = request.decode('utf-8')
            print(request_str.split(' '))

            filename = request_str.split(' ')[1][1:] # mengambil nama file dari request
            try:
                with open(filename, 'rb') as f:
                    content = f.read()
                    response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + content
            except FileNotFoundError:
                response = b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>'
            conn.sendall(response)
            conn.close()

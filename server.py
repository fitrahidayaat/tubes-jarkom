#import socket module
from socket import * 
import sys 

# In order to terminate the program 
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket 
serverPort = 8080
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)
print ('the web server is up on port:',serverPort)

# Geting matched content type
def get_content_type(filename):
    content_type = filename.split('.')[-1]
    mp = {
        'image' : ['jpg', 'png', 'ico', 'jpeg', 'gif', 'svg+xml', 'tiff', 'webp', 'bmp', 'x-icon'],
        'text' : ['html', 'css', 'js'],
        'application' : ['pdf', 'json', 'xml', 'zip', 'gzip', 'x-tar', 'x-rar-compressed', 'x-7z-compressed', 'x-bzip', 'x-bzip2', 'x-rar', 'x-tar', 'x-zip-compressed', 'x-zip', 'x-zip-compr'],
        'audio' : ['mpeg', 'ogg', 'wav', 'webm', 'x-aac', 'x-flac', 'x-ma'],
        'video' : ['mpeg', 'mp4', 'quicktime', 'x-msvideo', 'webm'],
        'multipart' : ['mixed', 'alternative', 'related', 'form-data', 'signed', 'encrypted']
    }
    for key, value in mp.items():
        if content_type in value:
            return key + '/' + content_type
    

while True: 
    #Establish the connection 
    print('Ready to serve...') 
    connectionSocket, addr = serverSocket.accept() 
    try: 
        # Receives the request message from the client
        message = connectionSocket.recv(1024).decode()   
        filename = message.split(' ')[1] if message.split(' ')[0] == 'GET' else ''
        f = open(filename[1:], 'rb')                   
        outputdata = f.read()        
          
        #Send one HTTP header line into socket 
        response = 'HTTP/1.1 200 OK\r\n'
        response += f'Content-Type: {get_content_type(filename)}\r\n'
        response += '\r\n'
        connectionSocket.send(response.encode())
   
        #Send the content of the requested file to the client 
        connectionSocket.sendall(outputdata)
        #Close client socket
        connectionSocket.close() 
    except IOError: 
        #Send response message for file not found 
        response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>'
        connectionSocket.send(response.encode())

        #Close client socket 
        connectionSocket.close()
serverSocket.close() 
sys.exit() #Terminate the program after sending the corresponding data 
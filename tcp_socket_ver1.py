#import socket module
from socket import * 
import sys 
# In order to terminate the program 
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket 
# Fill in start 
serverPort = 8080
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)
print ('the web server is up on port:',serverPort)
# Fill in end 

while True: 
    #Establish the connection 
    print('Ready to serve...') 
    connectionSocket, addr = serverSocket.accept() 
    try: 
        message = connectionSocket.recv(1024).decode()   
        filename = message.split(' ')[1]    
        f = open(filename[1:])                     
        outputdata = f.read()          
        #Send one HTTP header line into socket 
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
        connectionSocket.send(response.encode())
   
        #Send the content of the requested file to the client 
        connectionSocket.send(outputdata.encode())
        connectionSocket.close() 
    except IOError: 
        #Send response message for file not found 
     
        connectionSocket.send('HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>'.encode())

        #Close client socket 
        connectionSocket.close()
serverSocket.close() 
sys.exit() #Terminate the program after sending the corresponding data 
import socket
import threading
import os

def print_progress(completed, total, message_prefix):
    width = 50  
    progress_percentage = int((completed * 100) / total)
    progress = (progress_percentage * width) // 100
    
    bar = f"{message_prefix} ["
    for i in range(width):
        if i < progress:
            bar += "#"
        else:
            bar += " "
    bar += f"] {progress_percentage}%"
    print("\r" + bar, end='')
    if completed == total:
        print() 

def handleClient(clientSocket):
    try:
        fileNameSize = int(clientSocket.recv(10).decode('utf-8'))
        print(f"Receiving filename size: {fileNameSize}")
        fileName = clientSocket.recv(fileNameSize).decode('utf-8')
        print(f"Receiving filename: {fileName}")
        
        fileSize = int(clientSocket.recv(10).decode('utf-8'))
        print(f"Receiving file size: {fileSize}")

        currentDir = os.path.dirname(os.path.realpath(__file__))

        filePath = os.path.join(currentDir, fileName)

        with open(filePath, 'wb') as f:
            bytesReceived = 0
            while bytesReceived < fileSize:
                chunk = clientSocket.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                bytesReceived += len(chunk)
                print_progress(bytesReceived, fileSize, "Receiving")
            print(f"\nFile {fileName} saved in {currentDir}.\n")
    except Exception as e:
        print(f"Error: {e}")

def listenOnPort(port=3000):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    serverSocket.bind(('', port))
    serverSocket.listen()
    print(f"Listening on port {port} for incoming files...")
    while True:
        clientSocket, address = serverSocket.accept()
        threading.Thread(target=handleClient, args=(clientSocket,)).start()

def sendFile(targetIp, filePath, port=3000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((targetIp, port))
            fileName = os.path.basename(filePath)
            fileSize = os.path.getsize(filePath)
        
            sock.send(str(len(fileName)).zfill(10).encode('utf-8'))
            sock.send(fileName.encode('utf-8'))
        
            sock.send(str(fileSize).zfill(10).encode('utf-8'))

            with open(filePath, 'rb') as f:
                bytesSent = 0
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    sock.sendall(chunk)
                    bytesSent += len(chunk)
                    print_progress(bytesSent, fileSize, "Sending")
            print("File sent successfully.")
        except Exception as e:
            print(f"Could not send file to {targetIp}: {e}")

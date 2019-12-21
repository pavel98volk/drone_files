import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 9123
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
  
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)) # STRANGE THINGS MADE ME DISCOVER THIS is much needed

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", ord(data[0]),ord(data[1]),ord(data[2]), ord(data[3])

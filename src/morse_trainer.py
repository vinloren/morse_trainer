import socket
target_host = "192.168.1.5"
target_port = 8888
# create a socket connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# let the client connect
client.connect((target_host, target_port))
# send some data
client.send("SYN")
# get some data
response = client.recv(4096)
print response
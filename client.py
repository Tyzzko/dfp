import socket
from server import IP as server_ip
#import machine


class Machine():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def rotate(self, x, y, z):
        self.x += (self.x - x)
        self.y += (self.y - y)
        self.z += (self.z - z)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IPs = server_ip
PORT = 11111
client.connect((IPs, PORT))
rd = client.recv(1024)
client.send("i'm OK too".encode('utf8'))
flag = True
raspb_con = Machine()

while flag:
    data_output = ''
    for i in range(3):
        data = client.recv(2048)
        data_output += data
        if not data:
            flag = False
    x, y, z = [float(j) for j in data_output.split()]
    raspb_con.rotate(x, y, z)



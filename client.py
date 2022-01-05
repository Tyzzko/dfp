import socket
from server import IP as server_ip


# import machine


class Machine():  # абстрактный класс, обеспечивающий сообщение между контроллером и поворотным механизмом
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def rotate(self, x, y, z):
        self.x += (self.x - x)
        self.y += (self.y - y)
        self.z += (self.z - z)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # инициализация клиента
IPs = server_ip
PORT = 11111
client.connect((IPs, PORT))
rd = client.recv(1024)
client.send("i'm OK too".encode('utf8'))
flag = True
rotator = Machine()

while flag:  # реализация приема данных с сервера клиенту
    data_output = ''
    for i in range(3):
        data = client.recv(2048)
        data_output += data
        if not data:
            flag = False
    x, y, z = [float(j) for j in data_output.split()]
    if x or y or z:
        rotator.rotate(x, y, z)

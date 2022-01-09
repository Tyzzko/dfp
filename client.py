import socket


class Machine:
    '''Инициализация методов класса, управляещего поворотным устройством - начальных координат'''

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def work(self, x, y, z):
        '''Функция рассчета изменения координат поворотного устройства. В последствии внедрение инструментов
        управления устройством'''
        self.x += (x - self.x)
        self.y += (y - self.y)
        self.z += (z - self.z)


class Client:
    '''Инициализация атрибутов класса клиента: настройка семьи адресов, максимальный
     объем количества получаемой информации. Создание объекта класса Machine, для передачи ему координат'''

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 11111
        self.client.connect((self.IP, self.PORT))
        self.data = ''
        self.client.send("i'm OK too".encode('utf8'))
        self.machine = Machine()

    def data_reception(self):
        '''Метод, реализующий прием данных с сервера'''
        self.data = self.client.recv(1024).decode('utf-8')
        if self.data:
            print(self.data)
            self.machine.work([float(i) for i in self.data.split()])

        else:
            self.client.close()


if __name__ == '__main__':
    client = Client()
    client.data_reception()

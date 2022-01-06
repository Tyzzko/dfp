import socket


class Client:
    '''Инициализация атрибутов класса клиента: настройка семьи адресов, максимальный
     объем количества получаемой информации'''
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 11111
        self.client.connect((self.IP, self.PORT))
        self.data = ''

    def data_reception(self):
        '''Метод, реализующий прием данных с сервера'''
        self.data = self.client.recv(1024).decode('utf-8')
        if self.data:
            pass
        else:
            self.client.close()

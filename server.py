import socket
from datetime import datetime
from pyorbital.orbital import Orbital
from requests import get
from math import sin, cos
from time import sleep  # импорт необходимых библиотек


def update_tle():  # функция, обновляющая tle-файл
    file = open('tle.txt', 'ab')
    file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)
    file.close()


def return_tle():  # функция, возвращающая tle-файл
    file = open('tle.txt', 'ab')
    file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)
    file.close()
    return file


class СalculationOfSpans():  # класс спутника
    def __init__(self, name):
        self.sats_name = name
        self.sat = Orbital(self.sats_name, tle_file='tle.txt')
        self.length = 24
        self.lon = 43.8399
        self.lat = 55.3949
        self.alt = 162
        self.utc_time = datetime.now()

    def get_next_passes(self):  # метод, возвращающий кортеж объектов datetime - времени пролетов спутника
        return self.sat.get_next_passes(self.utc_time, self.lon, self.lat, self.alt, tool=0.001, horizon=0)

    def update_utc_time(self): #метод, обновляющий время по utc
        self.utc_time = datetime.now()

    def get_lonlatalt(
            self):  # метод, возвращающий кортеж величин - широты, долготы, высоты над уровнем моря спутника в данное
        # время
        return self.sat.get_lonlatalt()


sats = ['NOAA 18', 'NOAA 19', 'METEOR-M 2', 'METEOR-M2 2', 'METOP-B', 'METOP-C', 'FENGYUN 3B', 'FENGYUN 3C']
print(*sats, sep=', ')
print('Выберите спутник из списка (используйте ctrl+c - ctrl+v)')
name_of_sat = input()
while name_of_sat not in sats:
    print('Неверно набрано имя спутника')
    name_of_sat = input()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # инициализация сервера
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP = socket.gethostbyname(socket.gethostname())
PORT = 11111
server.bind((IP, PORT))
server.listen(1)
connection, address = server.accept()
connection.send('OK'.encode('utf8'))

tle_file = return_tle()
sat = СalculationOfSpans(name_of_sat)
passes = sat.get_next_passes()[0]
flag = True
R = 6371

while flag:
    if datetime.now() == passes[0]:
        while datetime.now() != passes[-1]:
            sat.update_utc_time()
            lon, lat, alt = sat.get_lonlatalt()
            x = R * cos(lat) * cos(lon)
            y = R * cos(lat) * sin(lon)
            z = R * sin(lat)
            connection.send(f'{x} {y} {z}'.encode('utf-8'))
            #print(x, y, z)
        flag = False
    else:
        connection.send('None'.encode('utf-8'))
        sleep(passes[0] - datetime.now())

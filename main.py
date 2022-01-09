import socket
from datetime import datetime
from pyorbital.orbital import Orbital
from requests import get
from time import sleep  # импорт необходимых библиотек


def update_tle():  # функция, возвращающая tle-файл
    file = open('tle.txt', 'ab')
    file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)
    file.close()


class СalculationOfSpans:
    '''Инициализация атрибутов класса спутника: координат местности, длительности рассчета пролетов,
    времени местности по utc и создание объекта Orbital для получения данных о его местоположении'''

    def __init__(self, name):
        self.sats_name = name
        self.sat = Orbital(self.sats_name, tle_file='tle.txt')
        self.length = 24
        self.lon = 43.8399
        self.lat = 55.3949
        self.alt = 162
        self.utc_time = datetime.now()

    def get_next_passes(self):
        ''' Метод, возвращающий кортеж объектов datetime - времени пролетов спутника '''
        return self.sat.get_next_passes(self.utc_time, self.length, self.lon, self.lat, self.alt, horizon=0)[0]

    def get_required_data(self):
        ''' Метод-получение данных для управления поворотным мехинизмом: азимута и высоты спутника.
        Запрашиваются посредством передачи необходимых параметров (текущего времени,
        широты, высоты, над уровнем моря) методу get_observer_look() объекту класса Orbital библиотеки pyorbital '''
        self.utc_time = datetime.now()
        self.current_sat_lon, self.current_sat_lat, self.current_sat_alt = self.sat.get_lonlatalt()
        self.azimuth, self.elevation = self.sat.get_observer_look(self.utc_time, self.current_sat_lon,
                                                                  self.current_sat_lat, self.current_sat_alt)
        return self.azimuth, self.elevation


class Server:
    '''Инициализация атрибутов класса сервера: настройка семьи адресов, количества пользователей'''

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 11111
        self.server.bind((self.IP, self.PORT))
        self.server.listen(1)
        self.connection, self.address = self.server.accept()
        self.checkConnect = True
        self.connection.send('OK'.encode('utf8'))

    def data_dispatching(self, data1):
        '''Метод, раелизующий передачу данных клиенту'''
        if self.checkConnect:
            if not data1:
                self.server.close()
                self.checkConnect = False
            else:
                self.connection.send(data1.encode('utf-8'))

    def close(self):
        '''Метод, закрывающий дескриптор файла сокета'''
        self.server.close()


if __name__ == '__main__':
    '''Основное тело программы: пользователю предоставляется возможность выбрать интересующий его спутник, 
    далее происходит инициализация объектов классов Server и СalculationOfSpans, запрашиивается обновление 
    tle-файла и открывется цикл while, в котором происходят необходимые рассчеты и передача данных
    с сервера клиенту. Завершается цикл после истечения времени пролета спутника, и тогда же закрывается сообщение
    сервера и клиента.'''
    sats = ['NOAA 18', 'NOAA 19', 'METEOR-M 2', 'METEOR-M2 2', 'METOP-B', 'METOP-C', 'FENGYUN 3B', 'FENGYUN 3C']
    print(*sats, sep=', ')
    print('Выберите спутник из списка (используйте ctrl+c - ctrl+v)')
    name_of_sat = input()
    while name_of_sat not in sats:
        print('Неверно набрано имя спутника')
        name_of_sat = input()

    server = Server()  # инициализация сервера
    sat = СalculationOfSpans(name_of_sat)

    update_tle()
    passes = sat.get_next_passes()
    server.data_dispatching('ыыыыыыы')

    if datetime.now() == passes[0]:
        while datetime.now() != passes[1]:
            az, el = sat.get_required_data()
            server.data_dispatching(f'{az} {el}')
    else:
        print('спутника не ма((((')
        s = passes[0] - datetime.now()
        s = s.minute * 60 + s.second
        sleep(s)
        # sleep(passes[0] - datetime.now())

    server.close()

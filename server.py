import socket
from datetime import datetime
from pyorbital.orbital import Orbital
from requests import get
from time import sleep
from math import sin, cos

class NonExistentError(Exception):
    def __init__(self):
        pass


def update_tle():
    file = open('tle.txt', 'ab')
    file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)
    file.close()


class СalculationOfSpans():
    def __init__(self):
        self.length = 24
        self.lon = 43.8399
        self.lat = 55.3949
        self.alt = 162
        '''self.file = open("tle.txt", "ab")
        self.file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)'''
        self.utc_time = datetime.now()
        self.noaa_18 = Orbital('NOAA-18', tle_file='tle.txt')
        self.noaa_19 = Orbital('NOAA-19', tle_file='tle.txt')
        self.noaa_15 = Orbital('NOAA-15', tle_file='tle.txt')
        self.meteor_m2 = Orbital('METEOR-M 2', tle_file='tle.txt')
        self.meteor_m2_2 = Orbital('METEOR-M2 2', tle_file='tle.txt')
        self.metop_b = Orbital('METOP-B', tle_file='tle.txt')
        self.metop_c = Orbital('METOP-C', tle_file='tle.txt')
        self.fengyun_3c = Orbital('FENGYUN 3B', tle_file='tle.txt')
        self.fengyun_3b = Orbital('FENGYUN 3C', tle_file='tle.txt')

    def update_tle(self):
        file = open("tle.txt", "ab")
        file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)
        file.close()

    def update_time(self):
        self.utc_time = datetime.now()

    def time_calculations(self):
        self.noaa_18_passes_time = self.noaa_18.get_next_passes(self.utc_time, self.length, self.lon,
                                                                self.lat, self.alt, tol=0.001, horizon=0)
        self.noaa_19_passes_time = self.noaa_19.get_next_passes(self.utc_time, self.length, self.lon,
                                                                self.lat, self.alt, tol=0.001, horizon=0)
        self.noaa_15_passes_time = self.noaa_15.get_next_passes(self.utc_time, self.length, self.lon,
                                                                self.lat, self.alt, tol=0.001, horizon=0)
        self.meteor_m2_passes_time = self.meteor_m2.get_next_passes(self.utc_time, self.length, self.lon,
                                                                    self.lat, self.alt, tol=0.001, horizon=0)
        self.meteor_m2_2_passes_time = self.meteor_m2_2.get_next_passes(self.utc_time, self.length, self.lon,
                                                                        self.lat, self.alt, tol=0.001, horizon=0)
        self.metop_b_passes_time = self.metop_b.get_next_passes(self.utc_time, self.length, self.lon,
                                                                self.lat, self.alt, tol=0.001, horizon=0)
        self.metop_c_passes_time = self.metop_c.get_next_passes(self.utc_time, self.length, self.lon,
                                                                self.lat, self.alt, tol=0.001, horizon=0)
        self.fengyun_3c_passes_time = self.fengyun_3c.get_next_passes(self.utc_time, self.length, self.lon,
                                                                      self.lat, self.alt, tol=0.001, horizon=0)
        self.fengyun_3b_passes_time = self.fengyun_3b.get_next_passes(self.utc_time, self.length, self.lon,
                                                                      self.lat, self.alt, tol=0.001, horizon=0)

   ''' def lonlatalt_calcultions(self):
        if self.noaa_19_passes_time:
            self.noaa_19_lonlatalt = (self.noaa_19.get_lonlatalt(self.noaa_19_passes_time[0][0]),
                                      self.noaa_19.get_lonlatalt(self.noaa_19_passes_time[0][1]),
                                      self.noaa_19.get_lonlatalt(self.noaa_19_passes_time[0][2]))
        if self.noaa_18_passes_time:
            self.noaa_18_lonlatalt = (self.noaa_18.get_lonlatalt(self.noaa_18_passes_time[0][0]),
                                      self.noaa_18.get_lonlatalt(self.noaa_18_passes_time[0][1]),
                                      self.noaa_18.get_lonlatalt(self.noaa_18_passes_time[0][2]))
        if self.noaa_15_passes_time:
            self.noaa_15_lonlatalt = (self.noaa_15.get_lonlatalt(self.noaa_15_passes_time[0][0]),
                                      self.noaa_15.get_lonlatalt(self.noaa_15_passes_time[0][1]),
                                      self.noaa_15.get_lonlatalt(self.noaa_15_passes_time[0][2]))
        if self.metop_b_passes_time:
            self.metop_b_lonlatalt = (self.metop_b.get_lonlatalt(self.metop_b_passes_time[0][0]),
                                      self.metop_b.get_lonlatalt(self.metop_b_passes_time[0][1]),
                                      self.metop_b.get_lonlatalt(self.metop_b_passes_time[0][2]))
        if self.metop_c_passes_time:
            self.metop_c_lonlatalt = (self.metop_c.get_lonlatalt(self.metop_c_passes_time[0][0]),
                                      self.metop_c.get_lonlatalt(self.metop_c_passes_time[0][1]),
                                      self.metop_c.get_lonlatalt(self.metop_c_passes_time[0][2]))
        if self.meteor_m2_passes_time:
            self.meteor_m2_lonlatalt = (self.meteor_m2.get_lonlatalt(self.meteor_m2_passes_time[0][0]),
                                        self.meteor_m2.get_lonlatalt(self.meteor_m2_passes_time[0][1]),
                                        self.meteor_m2.get_lonlatalt(self.meteor_m2_passes_time[0][2]))
        if self.meteor_m2_2_passes_time:
            self.meteor_m2_2_lonlatalt = (self.meteor_m2_2.get_lonlatalt(self.meteor_m2_2_passes_time[0][0]),
                                          self.meteor_m2_2.get_lonlatalt(self.meteor_m2_2_passes_time[0][1]),
                                          self.meteor_m2_2.get_lonlatalt(self.meteor_m2_2_passes_time[0][2]))
        if self.fengyun_3c_passes_time:
            self.fengyun_3c_lonlatalt = (self.fengyun_3c.get_lonlatalt(self.fengyun_3c_passes_time[0][0]),
                                         self.fengyun_3c.get_lonlatalt(self.fengyun_3c_passes_time[0][1]),
                                         self.fengyun_3c.get_lonlatalt(self.fengyun_3c_passes_time[0][2]))
        if self.fengyun_3b_passes_time:
            self.fengyun_3b_lonlatalt = (self.fengyun_3b.get_lonlatalt(self.fengyun_3b_passes_time[0][0]),
                                         self.fengyun_3b.get_lonlatalt(self.fengyun_3b_passes_time[0][1]),
                                         self.fengyun_3b.get_lonlatalt(self.fengyun_3b_passes_time[0][2]))'''

   ''' def dict_formation(self):
        self.sats = {'NOAA 18': {self.noaa_18_passes_time[0][0]: self.noaa_18_lonlatalt[0],
                                 self.noaa_18_passes_time[0][1]: self.noaa_18_lonlatalt[1],
                                 self.noaa_18_passes_time[0][2]: self.noaa_18_lonlatalt[2]},
                     'NOAA 19': {self.noaa_19_passes_time[0][0]: self.noaa_19_lonlatalt[0],
                                 self.noaa_19_passes_time[0][1]: self.noaa_19_lonlatalt[1],
                                 self.noaa_19_passes_time[0][2]: self.noaa_19_lonlatalt[2]},
                     'METEOR-M 2': {self.meteor_m2_passes_time[0][0]: self.meteor_m2_lonlatalt[0],
                                    self.meteor_m2_passes_time[0][1]: self.meteor_m2_lonlatalt[1],
                                    self.meteor_m2_passes_time[0][2]: self.meteor_m2_lonlatalt[2]},
                     'METEOR-M2 2': {self.meteor_m2_2_passes_time[0][0]: self.meteor_m2_2_lonlatalt[0],
                                     self.meteor_m2_2_passes_time[0][1]: self.meteor_m2_2_lonlatalt[1],
                                     self.meteor_m2_2_passes_time[0][2]: self.meteor_m2_2_lonlatalt[2]},
                     'METOP-B': {self.metop_b_passes_time[0][0]: self.metop_b_lonlatalt[0],
                                 self.metop_b_passes_time[0][1]: self.metop_b_lonlatalt[1],
                                 self.metop_b_passes_time[0][2]: self.metop_b_lonlatalt[2]},
                     'METOP-C': {self.metop_c_passes_time[0][0]: self.metop_c_lonlatalt[0],
                                 self.metop_c_passes_time[0][1]: self.metop_c_lonlatalt[1],
                                 self.metop_c_passes_time[0][2]: self.metop_c_lonlatalt[2]},
                     'FENGYUN 3B': {self.fengyun_3b_passes_time[0][0]: self.fengyun_3b_lonlatalt[0],
                                    self.fengyun_3b_passes_time[0][1]: self.fengyun_3b_lonlatalt[1],
                                    self.fengyun_3b_passes_time[0][2]: self.fengyun_3b_lonlatalt[2]},
                     'FENGYUN 3C': {self.fengyun_3c_passes_time[0][0]: self.fengyun_3c_lonlatalt[0],
                                    self.fengyun_3c_passes_time[0][1]: self.fengyun_3c_lonlatalt[1],
                                    self.fengyun_3c_passes_time[0][2]: self.fengyun_3c_lonlatalt[2]}}'''

    def get_informatiion_about_sat(self, name):
        return self.sats[name]


sats = ['NOAA 18', 'NOAA 19', 'METEOR-M 2', 'METEOR-M2 2', 'METOP-B', 'METOP-C', 'FENGYUN 3B', 'FENGYUN 3C']
spans = СalculationOfSpans()
spans.time_calculations()
spans.lonlatalt_calcultions()
spans.dict_formation()
print(*sats, sep=', ')
print('Выберите спутник из списка (используйте ctrl+c - ctrl+v)')
name_of_sat = input()
while name_of_sat not in sats:
    print('Неверно набрано имя спутника')
    name_of_sat = input()
information = spans.get_informatiion_about_sat(name_of_sat)
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP = socket.gethostbyname(socket.gethostname())
PORT = 11111
listener.bind((IP, PORT))
listener.listen(0)
'''connection, address = listener.accept()
connection.send('OK'.encode('utf8'))'''

R = 6371
for i in information:
    lon, lat, alt = information[i]
    x = R * cos(lat) * cos(lon)
    y = R * cos(lat) * sin(lon)
    z = R * sin(lat)
    print(x, y, z)

'''
current_time = datetime.now()
delta = datetime.timedelta(hours=1)
if current_time + delta == datetime.now:
    current_time = datetime.now()
    spans.update_time()
    spans.update_tle()
    spans.time_calculations()
    spans.lonlatalt_calcultions()
    spans.dict_formation()'''

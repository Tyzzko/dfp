from datetime import datetime
from pyorbital.orbital import Orbital
from requests import get
from math import cos, sin, tan


class Satellite_Bot:
    hou = 72
    pitch = 45
    long_poz = 43.4796
    lat_poz = 43.6311
    height_poz = 0
    update_time = 0

    def update_tle(self):
        file = open("tle.txt", "ab")
        file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)
        file.close()

    def return_tle(self):
        file = open("tle.txt", "ab")
        file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)
        file.close()
        return file

    def calculation_satellite(self):
        if Satellite_Bot.update_time == 0 or \
                str((Satellite_Bot.update_time - (datetime.date(datetime.now())))).split('-')[-1] == '03':
            Satellite_Bot.update_time = (datetime.date(datetime.now()))
            self.update_tle()
        self.utc_time = datetime.utcnow()

        self.noaa_18 = Orbital("NOAA-18", tle_file='tle.txt')
        self.noaa_19 = Orbital("NOAA-19", tle_file='tle.txt')
        self.noaa_20 = Orbital("NOAA-20", tle_file='tle.txt')
        self.meteor_m2 = Orbital("METEOR-M 2", tle_file='tle.txt')
        self.meteor_m2_2 = Orbital("METEOR-M2 2", tle_file='tle.txt')
        self.fengyun_3b = Orbital("FENGYUN 3B", tle_file='tle.txt')
        self.fengyun_3c = Orbital("FENGYUN 3C", tle_file='tle.txt')

        self.plans_noaa18 = self.noaa_18.get_next_passes(self.utc_time, Satellite_Bot.hou,
                                                         Satellite_Bot.long_poz, Satellite_Bot.lat_poz,
                                                         Satellite_Bot.height_poz, tol=0.001,
                                                         horizon=Satellite_Bot.pitch)
        self.plans_noaa20 = self.noaa_20.get_next_passes(self.utc_time, Satellite_Bot.hou,
                                                         Satellite_Bot.long_poz, Satellite_Bot.lat_poz,
                                                         Satellite_Bot.height_poz, tol=0.001,
                                                         horizon=Satellite_Bot.pitch)
        self.plans_noaa19 = self.noaa_19.get_next_passes(self.utc_time, Satellite_Bot.hou, Satellite_Bot.long_poz,
                                                         Satellite_Bot.lat_poz, Satellite_Bot.height_poz, tol=0.001,
                                                         horizon=Satellite_Bot.pitch)
        self.plans_meteor_m2 = self.meteor_m2.get_next_passes(self.utc_time, Satellite_Bot.hou, Satellite_Bot.long_poz,
                                                              Satellite_Bot.lat_poz, Satellite_Bot.height_poz,
                                                              tol=0.001,
                                                              horizon=Satellite_Bot.pitch)
        self.plans_meteor_m2_2 = self.meteor_m2_2.get_next_passes(self.utc_time, Satellite_Bot.hou,
                                                                  Satellite_Bot.long_poz,
                                                                  Satellite_Bot.lat_poz, Satellite_Bot.height_poz,
                                                                  tol=0.001,
                                                                  horizon=Satellite_Bot.pitch)
        self.fengyun_3b = self.fengyun_3b.get_next_passes(self.utc_time, Satellite_Bot.hou, Satellite_Bot.long_poz,
                                                          Satellite_Bot.lat_poz, Satellite_Bot.height_poz,
                                                          tol=0.001,
                                                          horizon=Satellite_Bot.pitch)
        self.fengyun_3c = self.fengyun_3c.get_next_passes(self.utc_time, Satellite_Bot.hou, Satellite_Bot.long_poz,
                                                          Satellite_Bot.lat_poz, Satellite_Bot.height_poz,
                                                          tol=0.001,
                                                          horizon=Satellite_Bot.pitch)

        self.passes = {'NOAA 18': self.plans_noaa18,
                       'NOAA 19': self.plans_noaa19,
                       'NOAA 20': self.plans_noaa20,
                       'METEOR-M 2': self.plans_meteor_m2,
                       'METEOR-M2 2': self.plans_meteor_m2_2,
                       'FENGYUN 3B': self.fengyun_3b,
                       'FENGYUN 3C': self.fengyun_3c}
        return self.passes


satellite = Satellite_Bot()
file = satellite.return_tle()
passes = satellite.calculation_satellite()
# for i in passes:
#     print(i, *passes[i], sep='\n')
for i in passes:
    file = open('tle.txt').readlines()
    file = [i.strip() for i in file]
    tle1, tle2 = file[file.index(i) + 1], file[file.index(i) + 2]
    for j in passes[i]:
        while 0 < int(str(datetime.time(j[1])).split(':')[1]) - int(str(datetime.time(datetime.now())).split(':')[1]) \
                < 3:
            orb = Orbital(i, line1=tle1, line2=tle2)
            lon, lat, el = orb.get_lonlatalt(datetime.now())
            az = orb.get_observer_look(datetime.now(), lon, lat, el)[0]
            x = 1.449 / tan(el) * cos(az)
            y = 1.449 / tan(el) * sin(az)
            print(x, y)

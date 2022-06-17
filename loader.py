from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from db import Database
db = Database()
# Захарденные переменные для работы с массивом
date_time = 3
browser_num = -3
country_num = 4
device_num = -2
city_num = 6


def analyse_info(rows):  #анализ полученного массива строк из БД
    date_visit = {}
    date_unique_visit = {}
    users_browser = {}
    users_country = {}
    users_cities = {}
    devices = {}
    uid_set = set()
    for row in rows:

        date = row[date_time].strftime("%m/%d/%Y")
        if date in date_visit.keys():
            date_visit.update({date: date_visit.get(date)+1})
        else:
            date_visit.update({date: 1})

        if row[browser_num] in users_browser.keys() and not row[-1] in uid_set: # Добавление браузера в словарь
            users_browser.update({row[browser_num]: users_browser.get(row[browser_num])+1})
        elif not row[browser_num] in users_browser.keys():   # условие на первое добавление
            users_browser.update({row[browser_num]: 1})

        if row[country_num] in users_country.keys() and not row[-1] in uid_set: # Добавление страны в словарь
            users_country.update({row[country_num]: users_country.get(row[country_num])+1})
        elif not row[country_num] in users_country.keys():
            users_country.update({row[country_num]: 1})

        if row[device_num] in devices.keys() and not row[-1] in uid_set:  # Добавление устройства в словарь
            if row[device_num] == "Other":
                devices.update({"PC": devices.get(row[device_num]) + 1})
            else:
                devices.update({row[device_num]: devices.get(row[device_num])+1})
        elif not row[device_num] in devices.keys():
            if row[device_num] == "Other":
                devices.update({"PC": 1})
            else:
                devices.update({row[device_num]: 1})

        if row[city_num] in users_cities.keys() and not row[-1] in uid_set: # Добавление города в словарь
            users_cities.update({row[city_num]: users_cities.get(row[city_num])+1})
        elif not row[city_num] in users_cities.keys():
            users_cities.update({row[city_num]: 1})

        if date in date_unique_visit.keys() and not row[-1] in uid_set:  # Добавление уникального посещения в словарь
            uid_set.add(row[-1])
            date_unique_visit.update({date: len(uid_set)})
        elif not date in date_unique_visit.keys():
            date_unique_visit.update({date: 1})
        uid_set.add(row[-1])
    return date_visit, date_unique_visit, users_browser, users_country, devices, users_cities, len(uid_set)

class MplCanvas(FigureCanvasQTAgg):    #Класс фигуры для графиков
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


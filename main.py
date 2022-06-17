# This Python file uses the following encoding: utf-8
# подключение библиотек
import webbrowser
from Custom_Widgets.Widgets import *
from PySide2.QtWidgets import QApplication, QMainWindow
import config
from form import *
from loader import db, analyse_info, MplCanvas
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.main_page.setCurrentWidget(self.ui.getstat_page)
        self.ui.getstat_btn.clicked.connect(lambda: self.ui.main_page.setCurrentWidget(self.ui.getstat_page))
        self.ui.analyse_btn.clicked.connect(lambda: self.ui.main_page.setCurrentWidget(self.ui.analyse_page))
        self.ui.about_btn.clicked.connect(lambda: self.ui.main_page.setCurrentWidget(self.ui.about_page))
        self.ui.feedback_btn.clicked.connect(lambda: self.ui.main_page.setCurrentWidget(self.ui.feedback_page))
        self.ui.get_stat.clicked.connect(self.update_graph)
        self.ui.connectDB_btn.clicked.connect(self.connect_to_db)
        self.ui.start_date_btn.clicked.connect(self.open_close_calendar)
        self.ui.download_btn.clicked.connect(self.download_pdf)
        self.open_close_calendar()
        #*****************************************
        self.ui.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ui.server_lineEdit.setMaxLength(32)
        self.ui.user_lineEdit.setMaxLength(32)
        self.ui.table_lineEdit.setMaxLength(32)
        self.ui.password_lineEdit.setMaxLength(32)
        # *****************************************
        self.ui.vk_btn.clicked.connect(lambda: webbrowser.open_new("https://vk.com/bestpointguard")) # ссылка на вк
        self.ui.github_btn.clicked.connect(lambda: webbrowser.open_new("https://github.com/xaban3r"))# ссылка на гитхаб
        self.ui.mail_btn.clicked.connect(lambda: webbrowser.open_new("mailto:nstr3@mail.ru"))        # ссылка на почту
        self.ui.tg_btn.clicked.connect(lambda: webbrowser.open_new("https://t.me/bestpointguard"))   # ссылка на тг
        self.show()
        loadJsonStyle(self, self.ui)    # добавление json стилей

    def open_close_calendar(self):      # окно календаря
        if self.ui.dateEdit.isHidden(): # отображается по нажатию если скрыто и скрывается, если открыто
            self.ui.dateEdit.show()
            self.ui.dateEdit_2.show()
            self.ui.start_date_label_2.show()
        else:
            self.ui.dateEdit.hide()
            self.ui.dateEdit_2.hide()
            self.ui.start_date_label_2.hide()

    def download_pdf(self): # метод создания и загрузки пдф файла со статистикой
        figures = [self.ui.MplWidget.canvas.figure, self.ui.MplWidget_2.canvas.figure,
                   self.ui.MplWidget_3.canvas.figure, self.ui.MplWidget_4.canvas.figure,
                   self.ui.MplWidget_5.canvas.figure, self.ui.MplWidget_6.canvas.figure]
        c = canvas.Canvas("Statistic.pdf")
        c.setTitle("stat")
        indent = 1.5
        height = indent
        for figure in figures:
            image = BytesIO()
            figure.savefig(image, format="png")
            image.seek(0)
            image = ImageReader(image)
            figureSize = figure.get_size_inches() * 2.54
            # A4 210×297 мм
            # Если выходим за пределы листа, то добавляем новый лист
            if height + figureSize[1] + indent > 29.7:
                height = indent
                c.showPage()
            # Добавляем image в pdf
            c.drawImage(image, (10.5 - figureSize[0] / 2) * cm, height * cm,
                        figureSize[0] * cm, figureSize[1] * cm)
            height += figureSize[1]
        c.save()
        self.create_attention(label="Успех!", isWarning=False)

    def create_attention(self, label="Неизвестная ошибка", isWarning=True): # окно уведомления об успехе операции
        attention = QMessageBox(self)
        attention.setText(label)
        attention.setIcon(QMessageBox.Warning)
        attention.setIcon(QMessageBox.Warning) if isWarning else attention.setIcon(QMessageBox.NoIcon)
        attention.setWindowTitle("Attention")
        attention.setStandardButtons(QMessageBox.Ok)
        attention.setWindowModality(QtCore.Qt.WindowModal)
        attention.setStyleSheet("QLabel{min-width:500 px; font-size: 24px;} QPushButton{ width:250px; font-size: 18px; }")
        attention.show()

    def connect_to_db(self):
        # Подключение к БД
        config.host = self.ui.server_lineEdit.text()
        config.user = self.ui.user_lineEdit.text()
        config.db_name = self.ui.table_lineEdit.text()
        config.password = self.ui.password_lineEdit.text()
        try: # попытка подключения к БД
            db.connect()
            self.create_attention(label="Успех!", isWarning=False)
        except Exception as e: # вызов окна ошибки в случае неудачи
            self.create_attention(label="Ошибка подключения")


    def update_graph(self):
        try:
            if self.ui.dateEdit.isHidden():
                all_str = db.take_all_info()       # получение всех данных из БД, если нет включенного календаря
            else:
                first_date = self.ui.dateEdit.text().split(".")     # парс даты из календаря для выборки по периоду
                second_date = self.ui.dateEdit_2.text().split(".")
                first = first_date[-1] + "-" + first_date[1] + "-" + first_date[0]  # преобразование к нужному виду
                second = second_date[-1] + "-" + second_date[1] + "-" + second_date[0]
                all_str = db.take_info_by_date(first, second)   # выборка данных по периоду
            # Анализ данных и их вывод в необходимые структуры данных
            date_visit, date_unique_visit, users_browser, users_country, devices, users_cities, all_uid = analyse_info(all_str)
            # *********************************
            self.ui.all_views.clear()
            self.ui.all_views.setText(str(len(all_str)))
            self.ui.all_views.setStyleSheet(u"color: black; font-size: 14;")
            self.ui.all_views.show()
            # *********************************
            self.ui.all_unique_views.clear()
            self.ui.all_unique_views.setText(str(all_uid))
            self.ui.all_unique_views.setStyleSheet(u"color: black; font-size: 14;")
            self.ui.all_unique_views.show() # отображение общего кол-во уникальынх посещений
            # *********************************
            lists = sorted(date_visit.items())  # сортировка элементов
            x, y = zip(*lists)
            self.ui.MplWidget.canvas.axes.clear()

            self.ui.MplWidget.canvas.axes.plot(x, y, '--', x, y, '.') #  отрисовка графика
            for i in zip(x, y): # Отрисовка цифр у вершин на графике
                self.ui.MplWidget.canvas.axes.annotate(i[1], (i[0], i[1]), fontsize=12)
            self.ui.MplWidget.canvas.axes.tick_params(axis='x', which='major', rotation=45)
            self.ui.MplWidget.canvas.axes.set_xmargin(-0.1)
            self.ui.MplWidget.canvas.axes.set_title("Посещения/день")
            self.ui.MplWidget.canvas.draw()     # Отрисовка
            # *********************************
            lists = sorted(date_unique_visit.items())
            x, y = zip(*lists)
            self.ui.MplWidget_2.canvas.axes.clear()
            self.ui.MplWidget_2.canvas.axes.plot(x, y, '--', x, y, '.') #  отрисовка графика
            for i in zip(x, y): # Отрисовка цифр у вершин на графике
                self.ui.MplWidget_2.canvas.axes.annotate(i[1], (i[0], i[1]), fontsize=12)
            self.ui.MplWidget_2.canvas.axes.tick_params(axis='x', which='major', rotation=45)
            self.ui.MplWidget_2.canvas.axes.set_xmargin(-0.1)       # устновка отступа
            self.ui.MplWidget_2.canvas.axes.set_title("Уник. посещения/день")
            self.ui.MplWidget_2.canvas.draw()       # Отрисовка
            # *********************************
            names, quantity = zip(*users_browser.items())
            self.ui.MplWidget_3.canvas.axes.clear()
            self.ui.MplWidget_3.canvas.axes.pie(quantity, labels=names, autopct='%1.2f%%') # установление вида диаграммы
            self.ui.MplWidget_3.canvas.axes.legend(loc=2)    # добавление легенды
            self.ui.MplWidget_3.canvas.axes.set_title("Браузеры")
            self.ui.MplWidget_3.canvas.draw()   # Отрисовка круговой диаграммы
            # *********************************
            names, quantity = zip(*users_country.items())
            self.ui.MplWidget_4.canvas.axes.clear()
            self.ui.MplWidget_4.canvas.axes.pie(quantity, labels=names, autopct='%1.2f%%')
            self.ui.MplWidget_4.canvas.axes.legend(loc=2)
            self.ui.MplWidget_4.canvas.axes.set_title("Страны")
            self.ui.MplWidget_4.canvas.draw()     # Отрисовка круговой диаграммы
            # *********************************
            names, quantity = zip(*devices.items())
            self.ui.MplWidget_5.canvas.axes.clear()
            self.ui.MplWidget_5.canvas.axes.pie(quantity, labels=names, autopct='%1.2f%%')
            self.ui.MplWidget_5.canvas.axes.legend(loc=2)
            self.ui.MplWidget_5.canvas.axes.set_title("Устройства")
            self.ui.MplWidget_5.canvas.draw()     # Отрисовка круговой диаграммы
            # *********************************
            names, quantity = zip(*users_cities.items())
            self.ui.MplWidget_6.canvas.axes.clear()
            self.ui.MplWidget_6.canvas.axes.pie(quantity, labels=names, autopct='%1.2f%%')
            self.ui.MplWidget_6.canvas.axes.legend(loc=2)
            self.ui.MplWidget_6.canvas.axes.set_title("Города")
            self.ui.MplWidget_6.canvas.draw()     # Отрисовка круговой диаграммы

        except Exception as e:
            if type(e) == AttributeError:
                self.create_attention(label="Приложение не подключено к БД")        # создание окна результата действия
            else:
                self.create_attention(label="Неверно выбрана дата или данных за выбранный период нет")
                print(e)


if __name__ == "__main__":
    app = QApplication()
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())

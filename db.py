import config
import psycopg2


class Database:
    def connect(self):
        self.conn = psycopg2.connect(database=config.db_name,
                                     user=config.user,
                                     password=config.password,
                                     host=config.host)
        self.conn.set_session(autocommit=True)
        print("Successfully connection")

    def take_all_info(self):   # метод выборки всех строк из таблицы
        cursor = self.conn.cursor()
        sql = "SELECT * FROM visitors"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def take_info_by_date(self, first_date, second_date):
        cursor = self.conn.cursor()
        # sql команада выборки по дате
        sql = f"""SELECT * FROM visitors WHERE (date BETWEEN '{first_date}' AND '{second_date}')"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        return rows


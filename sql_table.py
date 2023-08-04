import sqlite3, logging
from datetime import datetime


class TableWriter:
    def __init__(self):
        self.connect = sqlite3.connect('google_play_apps_stats.db')
        self.coursor = self.connect.cursor()

    def create_table(self):
        """ Шаблончик таблицы appsdata с полями
        (id, average, reviews, downloads, domain)"""
        try:
            self.coursor.execute("""CREATE TABLE IF NOT EXISTS appsstats (
            id INTEGER PRIMARY KEY,
            average FLOAT NOT NULL,
            reviews INT NOT NULL,
            downloads INT NOT NULL,
            latest_update DATETIME NOT NULL,
            domain TEXT NOT NULL);""")
            self.connect.commit()
        except sqlite3.Error as error:
            logging.info("ERROR", error)

    def add_record(self, average, reviews, downloads, latest_update, domain):
        try:
            latest_update_date = datetime.strptime(latest_update, "%b %d, %Y")
            # Format the datetime object to a string suitable for SQL (assuming the SQL column is of type DATE)
            latest_update_sql_format = latest_update_date.strftime("%Y-%m-%d")
            if self.coursor.execute(f"SELECT domain FROM appsstats"
                                    f" WHERE domain = ?", (domain,)).fetchone() is None:
                self.coursor.execute("INSERT INTO appsstats "
                                     "(average, reviews, downloads, latest_update, domain)"
                                     " VALUES (?, ?, ?, ?, ?)",
                                     (average, reviews, downloads, latest_update_sql_format, domain))
                logging.info(f'{(average, reviews, downloads, domain)} added to data base\n')
                print(f'{(average, reviews, downloads, domain)} added to data base\n')
                self.connect.commit()
            else:
                self.update_record(average, reviews, downloads, latest_update_sql_format, domain)
        except sqlite3.Error as error:
            logging.info("Error", error)
            print(error)

    def update_record(self, average, reviews, downloads, latest_update, domain):
        try:
            self.coursor.execute("UPDATE appsstats SET "
                                 "average = ?, reviews = ?, downloads = ?, latest_update = ?"
                                 " WHERE domain = ?",
                                 (average, reviews, downloads, latest_update, domain))
            logging.info(f"data {(average, reviews, downloads, latest_update, domain)} updated  in table 'appsstats' "
                         f"where domain = {domain}\n")
            print(f"data {(average, reviews, downloads)} updated  in table 'appsstats' where domain = {domain}\n")
            self.connect.commit()
        except sqlite3.Error as error:
            logging.info("Error", error)

    def clear_table(self):
        """  На всякий случай, чтоб удобнее очищать таблицу """
        self.coursor.execute(f"DELETE FROM appsstats")
        logging.info(f"table appsstats cleared")
        self.connect.commit()

    def del_record(self, domain):
        """  Если понадобится удалить запись по домену """
        self.coursor.execute(f"DELETE FROM appsstats WHERE domain = ?", (domain,))
        self.connect.commit()


object = TableWriter()
object.create_table()

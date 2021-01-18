import sqlite3


class Database:
    def __init__(self, path_to_db="data/database.sqlite"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql_query: str, params: tuple = None, fetchone=False, fetchall=False, commit=True):
        def logger(statement):
            print("=" * 80, f"Выполняем запрос к БД: \n{statement}", "=" * 80, sep="\n")

        if not params:
            params = tuple()
        data = None
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        cursor.execute(sql_query, params)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()
        return data

    def create_table_users(self):
        sql_query = "CREATE TABLE IF NOT EXISTS users (" \
                    "id INTEGER PRIMARY KEY);"
        self.execute(sql_query, commit=True)

    def create_table_gazzetta(self):
        sql_query = "CREATE TABLE IF NOT EXISTS gazzetta (" \
                    "post_id INTEGER PRIMARY KEY, " \
                    "post_link TEXT UNIQUE, " \
                    "image_link TEXT, " \
                    "original_text TEXT, " \
                    "translated_text TEXT, " \
                    "valid_translation TEXT);"
        self.execute(sql_query, commit=True)

    def create_table_sent_messages(self):
        sql_query = "CREATE TABLE IF NOT EXISTS sent_messages (" \
                    "id INTEGER PRIMARY KEY, " \
                    "user_id INTEGER NOT NULL, " \
                    "post_link TEXT);"
        self.execute(sql_query, commit=True)

    def drop_table_gazzetta(self):
        sql_query = "DROP TABLE IF EXISTS gazzetta;"
        self.execute(sql_query, commit=True)

    def add_user(self, id: int):
        sql_query = "INSERT INTO users VALUES(?);"
        self.execute(sql_query, params=(id,), commit=True)

    def count_users(self):
        sql_query = "SELECT COUNT(*) FROM users;"
        return self.execute(sql_query, fetchone=True)[0]

    @staticmethod
    def format_args(sql_request: str, params: dict):
        sql_request += " AND ".join([f"{item} = ?" for item in params])
        sql_request += ";"
        return sql_request, tuple(params.values())

    def select_user(self, **kwargs):
        sql_request = "SELECT * FROM users WHERE "
        sql_request, params = self.format_args(sql_request, kwargs)
        return self.execute(sql_request, params, fetchone=True)

    def del_user(self, id):
        self.execute("DELETE FROM users WHERE id=?;", params=(id,), commit=True)

    def gazzetta_posts_links(self):
        sql_query = "SELECT post_link FROM gazzetta;"
        links = self.execute(sql_query, fetchall=True)
        return [link[0] for link in links]

    def add_gazzetta_post(self, post_link: str, original_text: str, translated_text: str):
        sql_query = "INSERT INTO gazzetta (post_link, original_text, translated_text) VALUES (?,?,?);"
        self.execute(sql_query, params=(post_link, original_text, translated_text), commit=True)

    def add_gazzetta_translation(self, post_link: str, translated_text: str):
        sql_query = "UPDATE gazzetta SET valid_translation = ? WHERE post_link = ?;"
        self.execute(sql_query, params=(translated_text, post_link), commit=True)

    def add_to_sent_messages(self, user_id: int, post_link: str):
        sql_query = "INSERT INTO sent_messages (user_id, post_link) VALUES (?,?);"
        self.execute(sql_query, params=(user_id, post_link), commit=True)

    def get_sent_messages(self, user_id):
        sql_query = "SELECT post_link FROM sent_messages WHERE user_id=?;"
        sent_links = self.execute(sql_query, params=(user_id,), fetchall=True)
        return [link[0] for link in sent_links]

    def get_gazzetta_translation(self, post_link):
        sql_query = "SELECT translated_text FROM gazzetta WHERE post_link=?;"
        return self.execute(sql_query, params=(post_link, ), fetchone=True)[0]

    def alter_posts_table(self):
        sql_query = "ALTER TABLE gazzetta ADD COLUMN valid_translation TEXT;"
        self.execute(sql_query, commit=True)


if __name__ == "__main__":
    db = Database()
    db.create_table_users()

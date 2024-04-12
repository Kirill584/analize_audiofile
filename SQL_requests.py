import db_connect as dbc
from prettytable import PrettyTable

class Requests:

    def get_column_names(self):
        sql_name_columns = """SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'musics'
        ORDER BY ordinal_position ASC;"""

        column_names = []
        dbc.cur.execute(sql_name_columns)
        dbc.db.commit()
        data = dbc.cur.fetchall()
        for i in data:
            column_names.append(i[0])
        return(column_names)

    def get_musics_date(self, date):
        sql_date = f"SELECT title, artist, date FROM musics WHERE date > '{date}' and date != 'Нет'" 
        ta = PrettyTable()
        ta.clear()
        ta.field_names = ['title', 'artist', 'date']
        try:
            dbc.cur.execute(sql_date)
            dbc.db.commit()
            data = dbc.cur.fetchall()
            print(f'Песни, выпущенные после {date} года:')
            for i in data:
                ta.add_row(i)
            print(ta)
        except Exception as e:
            dbc.db.rollback()
            print(e)

    def get_musics_artist(self, artist):
        sql_artist = f"Select title, artist, album, genre from musics where artist = '{artist}'" 
        ta = PrettyTable()
        ta.clear()
        ta.field_names = ['title', 'artist', 'album', 'genre']
        try:
            dbc.cur.execute(sql_artist)
            dbc.db.commit()
            data = dbc.cur.fetchall()
            print(f'Песни автора {artist}')
            for i in data:
                ta.add_row(i)
            print(ta)        
        except Exception as e:
            dbc.db.rollback()
            print(e)

    def get_musics_sort_by(self, attr, boul=True):
        if boul:
            sql_sort = f"SELECT * FROM musics ORDER BY {attr};" 
        else:
            sql_sort = f"SELECT * FROM musics ORDER BY {attr} desc;" 
        ta = PrettyTable()
        ta.clear()
        ta.field_names = self.get_column_names()
        try:
            dbc.cur.execute(sql_sort)
            dbc.db.commit()
            data = dbc.cur.fetchall()
            print(f'Сортировка песен по {attr}')
            for i in data:
                ta.add_row(i)
            print(ta)
        except Exception as e:
            dbc.db.rollback()
            print(e)
            
    def get_musics_genre(self, genre):
        sql_genre = f"SELECT title, artist, genre FROM musics where lower(genre) LIKE '%{genre}%'" 
        ta = PrettyTable()
        ta.clear()
        ta.field_names = ['title', 'artist', 'genre']
        try:
            dbc.cur.execute(sql_genre)
            dbc.db.commit()
            data = dbc.cur.fetchall()
            print(f'Песни жанра {genre}')
            for i in data:
                ta.add_row(i)
            print(ta)
        except Exception as e:
            dbc.db.rollback()
            print(e)
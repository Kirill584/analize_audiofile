import dis
import os
import matplotlib.pyplot as plt
import db_connect as dbc

class Data:
    def search_path_files(folder_path):
        files = []
        for file_name in os.listdir(folder_path):
            files.append(os.path.join(folder_path, file_name))
        return(files)

    SQL_SHEMA = """CREATE TABLE IF NOT EXISTS musics
        (path VARCHAR, 
        title VARCHAR,
        artist VARCHAR,
        album VARCHAR,
        number VARCHAR,
        number_d VARCHAR,
        genre VARCHAR,
        date VARCHAR,
        composer VARCHAR,
        author VARCHAR,
        album_type VARCHAR,
        duration FLOAT,
        size INT,
        text VARCHAR,
        params VARCHAR,
        frames VARCHAR,
        framrate VARCHAR,
        channels VARCHAR,
        sampwidth VARCHAR,
        temp VARCHAR,
        code VARCHAR,
        format VARCHAR,
        groupe VARCHAR,
        publish VARCHAR)"""

    try:
        dbc.cur.execute(SQL_SHEMA)
        dbc.db.commit()
    except Exception as e:
        dbc.db.rollback()
        print(e)

    # file = 'musics\MACAN - ASPHALT 8.mp3'
    def get_data_for_file(file_path):
        import librosa
        import librosa.display
        import IPython.display as ipd

        print()
        print("Получение информации...")
        file = file_path
        format = file.split('.')[-1]
        file_name = file.split('/')[-1].replace('\\', '')
        y, sr = librosa.load(file)
        y, sr = librosa.load(file, duration=20)
        plt.figure(figsize=(14, 5))
        librosa.display.waveshow(y, sr=sr)
        plt.get('Monophonic')
        # plt.savefig(f'spect/spect_{file_name}.png') 
        # print(f"Спектрограмма сохранена в папку spect под названием spect_{file_name}.png")
        # plt.show()

        X = librosa.stft(y)
        Xdb = librosa.amplitude_to_db(abs(X))
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
        plt.colorbar()
        librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
        # plt.colorbar()
        with open(file, 'rb') as f:
            md = f.read(5)
        md
        if format == 'flac' or format == 'aiff':
            import librosa
            y, sr = librosa.load(file, sr=44100)

            ipd.Audio(y, rate=sr)
        else:
            import IPython.display as ipd
            ipd.Audio(file)
        # from mutagen import File
        # audio = File(file)
        # print("Все данные:")
        # for key, value in audio.items():
        #     print(key, ':', value)
        # mp3
        import eyed3
        from mutagen import File

        # audiofile = eyed3.load("music.mp3")
        # audiofile.tag.artist = "Token Entry"
        # audiofile.tag.album = "Free For All Comp LP"
        # audiofile.tag.album_artist = "Various Artists"
        # audiofile.tag.title = "The Edge"
        # audiofile.tag.track_num = 3
        # audiofile.tag.save()
        if format == 'mp3':
            name = eyed3.load(file)
            audio = File(file)

            if name.tag.title:
                title = name.tag.title
                title = str(title).replace("'", "")
                print('Название песни:', title)
            else:
                title = 'Нет'
                print('Название песни не найдено')
                
            if name.tag.artist:
                artist = name.tag.artist
                artist = str(artist).replace("'", "")
                print('Исполнитель:', artist)
            else:
                artist = 'Нет'
                print('Исполнитель не найден')
                
            if name.tag.album:
                album = name.tag.album
                album = str(album).replace("'", "")
                print('Альбом:', album)
            else:
                album = 'Нет'
                print('Альбом не найден')
            if name.tag.track_num[0]:
                number = name.tag.track_num[0]
                print('Номер трека:', number)
            else:
                number = 'Нет'
                print('Номер трека не найден')
            if name.tag.disc_num[0]:
                number_d = name.tag.disc_num[0]
                print('Номер диска:', number_d)
            else:
                number_d = 'Нет'
                print('Номер диска не найден')
            if name.tag.genre:
                genre = name.tag.genre
                print('Жанр:', genre)
            else:
                genre = 'Нет'
                print('Жанр не найден')
            if name.tag.getBestDate():
                date = name.tag.getBestDate()
                print('Дата релиза:', date)
            else:
                date = 'Нет'
                print('Дата не найдена')
            if name.tag.composer:
                composer  = name.tag.composer
                composer = str(composer).replace("'", "")
                print('Композиторы:', composer )
            else:
                composer = 'Нет'
                print('Композитор не найден')
            if name.tag.album_type:
                album_type  = name.tag.album_type
                print('Тип альбома:', album_type )
            else:
                album_type = 'Нет'
                print('Тип альбома не найден')

            y, sr = librosa.load(file)

            duration = librosa.get_duration(y=y, sr=sr)
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

            print('Длительность аудиофайла:', duration, 'секунд')
            print('Темп музыки:', tempo)
            size = os.path.getsize(file)

            if 'APIC:' in audio.tags:
                picture = audio.tags['APIC:'].data
                with open(f'covers/album_cover_{title}.jpg', 'wb') as f:
                    f.write(picture)
                print(f'Обложка альбома сохранена в папку covers под названием album_cover_{title}.jpg')
            else:
                print('Обложка альбома не найдена')

            if 'USLT:' in audio.tags:
                lyrics = audio.tags['USLT:'].text
                recognizer = sr.Recognizer()
                text = recognizer.recognize_sphinx(lyrics)
                print('Текст песни:', text)
            else:
                text = 'Нет'
                print('Текст песни не найден')
            try:
                dbc.cur.execute(f"select count(title)>0 from musics where title = '{title}'")
                exists = dbc.cur.fetchone()[0]
                dbc.db.commit()
                if not exists:
                    dbc.cur.execute(f"INSERT INTO musics (path, title, artist, album, number, number_d, genre, date, composer, album_type, duration, size, text) VALUES ('{file}', '{title}', '{artist}', '{album}', '{number}', '{number_d}', '{genre}', '{str(date)}', '{composer}', '{album_type}', '{duration}', '{size}', '{text}')")
                    dbc.db.commit()
                    s = file.split('\\')[-1]
                    print(f"Данные об аудиофайле {s} добавлены в БД.")
                else:
                    s = file.split('\\')[-1]
                    print(f"Данные об {s} уже добавлены.")
            except Exception as e:
                dbc.db.rollback()
                print(e)

        # flac
        from mutagen import File
        if format =='flac':
            audio = File(file)

            # Извлечение метаданных
            if 'title' in audio:
                title = audio['title'][0]
                title = str(title).replace("'", "")
                print('Название песни:', title)
            else:
                title = 'Нет'
                print('Название песни не найдено')
                
            if 'artist' in audio:
                artist = audio['artist'][0]
                artist = str(artist).replace("'", "")
                print('Исполнитель:', artist)
            else:
                artist = 'Нет'
                print('Исполнитель не найден')
                
            if 'album' in audio:
                album = audio['album'][0]
                album = str(album).replace("'", "")
                print('Альбом:', album)
            else:
                album = 'Нет'
                print('Альбом не найден')
            if 'tracknumber' in audio:
                number = audio['tracknumber'][0]
                print('Номер трека:', number)
            else:
                number = 'Нет'
                print('Номер трека не найден') 
            if 'discnumber' in audio:
                number_d = audio['discnumber'][0]
                print('Номер диска:', number_d)
            else:
                number_d = 'Нет'
                print('Номер диска не найден')
            if 'genre' in audio:
                genres = audio['genre']
                print('Жанр:', genres)
            else:
                genre = 'Нет'
                print('Жанр не найден')
            genre = ''
            if isinstance(genres, (list, tuple, dict)):
                for i in genres:
                    genre += i + ', '
            else:
                genre = genres
            if 'date' in audio:
                date = audio['date'][0]
                print('Дата релиза:', date)
            else:
                date = 'Нет'
                print('Дата не найдена')
            if 'author' in audio:
                authors = audio['author']
                print('Авторы:', authors)
            else:
                author = 'Нет'
                print('Автор не найден')
            author = ''
            if isinstance(authors, (list, tuple, dict)):
                for i in authors:
                    i = str(i).replace("'", "")
                    author += i + ', '
            else:
                author = authors
            if 'composer' in audio:
                composer  = audio['composer'][0]
                print('Композиторы:', composer )
            else:
                composer  = 'Нет'
                print('Композитор не найден')
            duration = audio.info.length
            print('Длительность аудиофайла:', duration, 'секунд')
            size = os.path.getsize(file)
            # Получение обложки альбома
            if 'APIC:' in audio.tags:
                picture = audio.tags['APIC:'].data
                with open(f'covers/album_cover_{title}.jpg', 'wb') as f:
                    f.write(picture)
                print(f'Обложка альбома сохранена в папку covers под названием album_cover_{title}.jpg')
            else:
                print('Обложка альбома не найдена')

            if 'USLT:' in audio.tags:
                lyrics = audio.tags['USLT:'].text
                recognizer = sr.Recognizer()
                text = recognizer.recognize_sphinx(lyrics)
                print('Текст песни:', text)
            else:
                text = 'Нет'
                print('Текст песни не найден')

            try:
                dbc.cur.execute(f"select count(title)>0 from musics where title = '{title}'")
                exists = dbc.cur.fetchone()[0]
                dbc.db.commit()
                if not exists:
                    dbc.cur.execute(f"INSERT INTO musics (path, title, artist, album, number, number_d, genre, date, author, composer, duration, size, text) VALUES ('{file}', '{title}', '{artist}', '{album}', '{number}', '{number_d}', '{str(genre)}', '{date}', '{author}', '{composer}', '{duration}', '{size}', '{text}')")
                    dbc.db.commit()
                    s = file.split('\\')[-1]
                    print(f"Данные об аудиофайле {s} добавлены в БД.")
                else:
                    s = file.split('\\')[-1]
                    print(f"Данные об {s} уже добавлены.")
            except Exception as e:
                dbc.db.rollback()
                print(e)
        # wav

        # import wave
        # with wave.open(file, 'r') as wav_file:
        #     print("Number of channels:", wav_file.getnchannels())
        #     print("Sample width:", wav_file.getsampwidth())
        #     print("Frame rate:", wav_file.getframerate())
        #     print("Number of frames:", wav_file.getnframes())
        #     print("Compression type:", wav_file.getcompname())
        #     frames = wav_file.getnframes()
        #     rate = wav_file.getframerate()
        #     duration = frames / float(rate)
        #     print("Duration:", duration, "seconds")

        import wave
        if format == 'wav':
            w = wave.open(file, 'r')

            # from mutagen.wavpack import WavPack

            # wav_file = WavPack('musics/music.wav')
            # print("Название песни:", wav_file['title'][0])

            import tinytag

            audio = tinytag.TinyTag.get(file)

            if audio.title:
                title = audio.title
                title = str(title).replace("'", "")
                print("Название песни:", audio.title)
            else:
                title = 'Нет'
                print("Название песни не найдено")
            if audio.artist:
                artist = audio.artist
                artist = str(artist).replace("'", "")
                print("Исполнитель:", audio.artist)
            else:
                artist = 'Нет'
                print("Исполнитель не найден")
            if audio.album: 
                album = audio.album
                album = str(album).replace("'", "")
                print("Альбом:", audio.album)
            else:
                album = 'Нет'
                print("Альбом не найден")
            if audio.track:
                number = audio.track
                print("Номер трека:", audio.track)
            else:
                number = 'Нет'
                print("Номер трека не найден")
            if audio.genre:
                genre = audio.genre
                print("Жанр:", audio.genre)
            else:
                genre = 'Нет'
                print("Жанр не найден")
            if audio.year:
                date = audio.year
                print("Год выпуска:", audio.year)
            else:
                date = 'Нет'
                print("Год выпуска не найден")

            # параметры аудиофайла
            if w.getparams():
                params_d = w.getparams()
                print("Параметры аудиофайла:", w.getparams())
            else:
                params_d = 'Нет'
                print("Параметры не найдены")
            params = ''  
            for i in params_d:
                params += str(i) + ' ,' 
            # количество фреймов
            if w.getnframes():
                frames = w.getnframes()
                print("Количество фреймов:", w.getnframes())
            else:
                frames = 'Нет'
                print("Количество фреймов не найдено")     
            # частота дискретизации
            if w.getframerate():
                framrate = w.getframerate()
                print("Частота дискретизации:", w.getframerate())
            else:
                framrate = 'Нет'
                print("Частота дискретизации не найдена")     
            # количество каналов
            if w.getnchannels():
                channels = w.getnchannels()
                print("Количество каналов:", w.getnchannels())
            else:
                channels = 'Нет'
                print("Количество каналов не найдено")     
            # битность
            if w.getsampwidth():
                sampwidth = w.getsampwidth()
                print("Битность:", w.getsampwidth())
            else:
                sampwidth = "Нет"
                print("Битность не найдена")     
            # продолжительность аудиофайла в секундах
            duration = w.getnframes() / float(w.getframerate())
            print("Продолжительность аудиофайла:", round(duration, 2), "секунд")
            # данные о каждом фрейме аудиофайла
            # frames = audio.readframes(file.getnframes())
            # print("Данные о каждом фрейме аудиофайла:", frames)

            w.close()
            size = os.path.getsize(file)
            try:
                dbc.cur.execute(f"select count(title)>0 from musics where title = '{title}'")
                exists = dbc.cur.fetchone()[0]
                dbc.db.commit()
                if not exists:
                    dbc.cur.execute(f"INSERT INTO musics (path, title, artist, album, number, genre, date, params, frames, framrate, channels, sampwidth, duration, size) VALUES ('{file}', '{title}', '{artist}', '{album}', '{number}', '{genre}', '{date}', '{params}', '{frames}', '{framrate}', '{channels}', '{sampwidth}', '{duration}', '{size}')")
                    dbc.db.commit()
                    s = file.split('\\')[-1]
                    print(f"Данные об аудиофайле {s} добавлены в БД.")
                else:
                    s = file.split('\\')[-1]
                    print(f"Данные об {s} уже добавлены.")
            except Exception as e:
                dbc.db.rollback()
                print(e)

        # aiff
        from mutagen import File
        if format == 'aiff':
            audio = File(file)

            # Извлечение метаданных
            if 'TALB' in audio:
                album = audio['TALB']
                album = str(album).replace("'", "")
                print('Альбом:', album)
            else:
                album = 'Нет'
                print('Альбом не найден')
            if 'TBPM' in audio:
                temp = str(audio['TBPM'])
                print('Темп:', temp)
            else:
                temp = 'Нет'
                print('Темп не найден')
            if 'TCON' in audio:
                genre = audio['TCON']
                print('Жанр:', genre)
            else:
                genre = 'Нет'
                print('Жанр не найден')
            if 'TDOR' in audio:
                date = audio['TDOR']
                print('Дата релиза:', date)
            else:
                date = 'Нет'
                print('Дата не найдена')
            if 'TENC' in audio:
                code = audio['TENC']
                print('Кодировка:', code)
            else:
                code = "Нет"
                print('Кодировка не найдена')
            if 'TFLT' in audio:
                format = audio['TFLT']
                print('Формат:', format)
            else:
                format = "Нет"
                print('Формат не найден')
            if 'TIT1' in audio:
                groupe = audio['TIT1']
                groupe = str(groupe).replace("'", "")
                print('Группа:', groupe)
            else:
                groupe = "Нет"
                print('Группа не найдена')
            if 'TIT2' in audio:
                title = audio['TIT2']
                title = str(title).replace("'", "")
                print('Название песни:', title)
            else:
                title = "Нет"
                print('Название песни не найдено')    
            if 'TPE1' in audio:
                artist = audio['TPE1']
                artist = str(artist).replace("'", "")
                print('Исполнитель:', artist)
            else:
                artist = "Нет"
                print('Исполнитель не найден')
            if 'TPUB' in audio:
                publish = audio['TPUB']
                print('Издательство:', publish)
            else:
                publish = "Нет"
                print('Издательство не найден')
            if 'TRCK' in audio:
                number = audio['TRCK']
                print('Номер трека:', number)
            else:
                number = "Нет"
                print('Номер трека не найден')
            duration = audio.info.length
            print('Длительность аудиофайла:', duration, 'секунд')
            size = os.path.getsize(file)
            # Получение обложки альбома
            if 'APIC:' in audio.tags:
                picture = audio.tags['APIC:'].data
                with open(f'covers/album_cover_{title}.jpg', 'wb') as f:
                    f.write(picture)
                print(f'Обложка альбома сохранена в папку covers под названием album_cover_{title}.jpg')
            else:
                print('Обложка альбома не найдена')

            if 'USLT:' in audio.tags:
                lyrics = audio.tags['USLT:'].text
                recognizer = sr.Recognizer()
                text = recognizer.recognize_sphinx(lyrics)
                print('Текст песни:', text)
            else:
                text = "Нет"
                print('Текст песни не найден')

            try:
                dbc.cur.execute(f"select count(title)>0 from musics where title = '{title}'")
                exists = dbc.cur.fetchone()[0]
                dbc.db.commit()
                if not exists:
                    dbc.cur.execute(f"INSERT INTO musics (path, album, temp, genre, date, code, format, groupe, title, artist, publish, number, duration, size, text) VALUES ('{file}', '{album}', '{temp}', '{genre}', '{date}', '{code}', '{format}', '{groupe}', '{title}', '{artist}', '{publish}', '{number}', '{duration}', '{size}', '{text}')")
                    dbc.db.commit()
                    s = file.split('\\')[-1]
                    print(f"Данные об аудиофайле {s} добавлены в БД.")
                else:
                    s = file.split('\\')[-1]
                    print(f"Данные об {s} уже добавлены.")
            except Exception as e:
                dbc.db.rollback()
                print(e)

    # type = input("Выберите что хотите вводить: 'file' - файл или 'folder' - папку. ")
    # if type == 'folder':
    #     file = input("Введите путь к папке: ")
    #     files = search_path_files(file)
    #     for file in files:
    #         get_data_for_file(file)
    # else: 
    #     file = input("Введите путь к файлу: ")
    #     get_data_for_file(file)

    def get_spect(file):
        import librosa
        y, sr = librosa.load(file)
        plt.figure(figsize=(14, 5))
        librosa.display.waveshow(y, sr=sr)
        plt.get('Monophonic')
        plt.show()

    def get_cover(file):
        from mutagen import File
        import IPython.display as ipd
        from PIL import Image
        import io
        import base64
        audio = File(file)
        if 'APIC:' in audio.tags:
            picture = audio.tags['APIC:'].data
            img = Image.open(io.BytesIO(picture))
            ipd.display(img)
        else:
            print('Обложка альбома не найдена')

    def get_date(date):
        from SQL_requests import Requests
        r = Requests()
        r.get_musics_date(date)

    def get_artist(artist):
        from SQL_requests import Requests
        r = Requests()
        r.get_musics_artist(artist)

    def get_sort(attr):
        from SQL_requests import Requests
        r = Requests()
        r.get_musics_sort_by(attr)

    def get_genre(genre):
        from SQL_requests import Requests
        r = Requests()
        r.get_musics_genre(genre)

    import sys
    import argparse
    
    if __name__ == '__main__':
        parse = argparse.ArgumentParser(
            prog = 'Программа для вывода информации об аудиофайле',
            description = 'Если на вход программы подаётся путь к файлу - выдается информация об этом файле и данные записываются в БД. Если на вход программы подаётся путь к папке - выдается информация о каждом файле в этой папке и данные о каждом файле записываются в БД. Так же с помощью некоторых параметров можно получить выборку песен из БД. Для работы программы нужны определенные папки: covers - в эту папку будут сохраняться обложки песен, musics - папка, в которой будут храниться песни для анализа, spect - в эту папку будут сохраняться спектограммы песен.',
            epilog = '(c) Крайнов Кирилл',
            add_help = False
        )
        parse.add_argument('-h', '--help', action='help', help='Показать справку и выйти')
        parse.add_argument('-f','--file', help="Путь к файлу")
        parse.add_argument('-fl','--folder', help="Путь к папке")
        parse.add_argument('-d','--date', help="Дата, после которой вышли песни")
        parse.add_argument('-a','--artist', help="Песни определенного артиста", default="")
        parse.add_argument('-s','--sort', help="Сортировка песен по любому критерию")
        parse.add_argument('-g','--genre', help="Песни определенного жанра")
        
        args = parse.parse_args(sys.argv[1:])
        print(args)
        if args.folder:
            files = search_path_files(args.folder)
            for file in files:
                get_data_for_file(file)
        elif args.file:
            get_data_for_file(args.file)
        if args.date:
            get_date(args.date)
        if args.artist:
            get_artist(args.artist)
        if args.sort:
            get_sort(args.sort)
        if args.genre:
            get_genre(args.genre)

    
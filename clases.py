# Конфиги
from config import song_folder, first_bpm

# библиотеки
import os
import re
from random import randint

class Folder:
    def __init__(self, song_folder):
        """Работа с папками и файлами"""
        self.folder = song_folder
        pass

    def get_all_songs(self) -> list:
        """Полчает список всех песен которые есть в папке"""
        response = os.listdir(self.folder)
        return response

class Songs(Folder):
    def __init__(self, song_folder):
        """Методы работы с песнями"""
        super().__init__(song_folder)
        pass

    # Проверки
    def rus_name_song(self, name:str) -> bool:
        """Проверяет российская песня или нет"""
        pattern_name = re.compile(r'^\d+ - [0-9A-Z]+ - [^_]+_pn\.mp3$')

        #проверить патерн названия всего трека
        if bool(pattern_name.match(name)):
            if self.rus_artist_name(name):
                return True  
            else:
                if self.rus_song_name(name):
                    return True
                else:
                    return False
        else:
            print(f'Братик, с этим именем проблемка:\n{name}\nподшамань и я норм отработаю')
          
    def rus_artist_name(self, name:str) -> bool:
        """Проверяет имя артиста на руские буквы"""
        pattern = re.compile(r'[А-Яа-яЁё]')

        artist_name = name.split("-")
        artist_name = artist_name[2].lower()
        artist_name = ''.join(artist_name.split())
        #КОСТЫЛЬ
        if artist_name == 'gorkypark':
            return True
        else:
            return bool(pattern.match(artist_name))
         
    def rus_song_name(self, name:str) -> bool:
        """Проверяет навзвание песни артиста на содержание русских букв"""
        pattern = re.compile(r'[А-Яа-яЁё]')

        song_name = name.split("-")
        song_name = song_name[3].lower()
        song_name = ''.join(song_name.split())

        return bool(pattern.search(song_name))
    

    # Формирования списков и словарей
    def all_songs_dict(self) -> dict:
        """Формируем словарь с песнями, присваивает им id"""
        response = {}
        all_songs = self.get_all_songs()
        id = 1
        for i in all_songs:
            data = self.songs_data(i)
            if data != None:
                response[id] = self.songs_data(i)
                id +=1
            else:
                pass
        return response
    
    def songs_data(self, song_name:str) -> dict:
        """Возвращает словарь с данными песни """
        pattern = re.compile(r'(?P<bpm>\d+) - (?P<ton>[0-9A-Z]+) - (?P<artist>[^-]+) - (?P<song>[^_]+)_pn\.mp3')
        match = pattern.match(song_name)
        if match:
            bpm = int(match.group('bpm'))
            ton = match.group('ton')
            artist = match.group('artist')
            song = match.group('song')
            all_name = song_name
            
            lang = 'ru' if self.rus_name_song(song_name) else 'eng'

            return {'bpm': bpm, 'ton': ton, 'lang': lang, 'name': artist.lower(), 'song': song.lower(), 'all_name':all_name}

        return None

    def rus_song(self) -> list:
        """"Формирует список id российских песен"""
        all_songs = self.all_songs_dict()
        response = []

        for i in all_songs:
            if self.rus_name_song(all_songs[i]) == True:
                response.append(i)
        return response

    def eng_song(self) -> list:
        """Формирует список из id зарубежных песен"""
        all_songs = self.all_songs_dict()
        response = []

        for i in all_songs:
            if self.rus_name_song(all_songs[i]) == False:
                response.append(i)
        return response

    def lang_songs(self, lang: str) -> list:
        """Собирает список id псен по языкам. Метки: 'ru'/'eng'"""
        all_song = self.all_songs_dict()
        response = []
        for i in all_song.keys():
            if all_song[i]['lang'] == lang:
                response.append(i)
            else:
                pass
        return response




    def bpm_eng_song(self) -> dict:
        """Формирует словарь с bpm зарубежных песен"""
        eng_song_list = self.eng_song()
        all_song = self.all_songs_dict()
        response = {}
        for i in eng_song_list:
            all_name = all_song[i]
            end_position = all_name.find('-')
            bpm = all_name[0:end_position]
            response[int(bpm)] = i
        
        return response

    def bpm_rus_song(self) -> dict:
        """Формирует словарь с bpm российских песен"""
        rus_song_list = self.rus_song()
        all_song = self.all_songs_dict()
        response = {}
        for i in rus_song_list:
            all_name = all_song[i]
            end_position = all_name.find('-')
            bpm = all_name[0:end_position]
            response[int(bpm)] = i 
        return response

    def bpm_dict(self):
        """"Фомирует словарь id:bpm """
        all_song = self.all_songs_dict()

        response = {}

        for i in all_song.keys():
            if all_song[i] != None:
                response[i] = all_song[i]['bpm']
            else:
                pass

        print(response)
        pass





    # Опсионально словарь по тональностям
    def ton_eng_song(self):
        """Формирует словарь тональностей зарубежных песен"""
        pass

    def ton_rus_song(self):
        """Формирует словарь тональностей российских песен"""
        pass

class Conditions(Songs):
    def __init__(self, song_folder):
        """"Проверяет условия для формирования ПЛ"""
        super().__init__(song_folder)
        pass

    # Базовые вычисления bpm
    def scope_bpm(self, bpm:int) -> dict:
        """Вычисляет bpm от предыдущей песни"""
        response = {}
        # добавить в словарь исходный би пи ЭМ
        # Добавить в словарь +/- бипиэм
        # Добавить умноженный диапазон БИ ПИ ЭМ!
        # Добавить разделенный диапазон БИ ПИ ЭМ

        # Вернуть словарь!
        
        pass
        
    def bpm_examination(self, lang_song: dict, target_bpm: int) -> list:
        """Возвращает список ID песен удовлетворяющих BPM"""
        
        pass




    def magic_rotator(self, lang, target_bpm) -> int:
        """Находит только лучшие песни"""
        
        # Полный список песен
        all_songs = self.all_songs_dict()

        # список id целевых песен песен
        lang_song = None #Целевой словарь

        # Диапазон поиска
        bpm_range = []

        if lang == 'ru':
            lang_song = self.lang_songs('ru')
        elif lang == 'eng':
            lang_song = self.lang_song('eng')
        else:
            print ('!!!!!!!!Что-то пошло не так в методе MAGIC_ROTATOR, блоке определения языковой подборки!!!!!!!!!') 

        
        # Собираем список песен с целевым BPM
        target_bpm_song = []
        for i in lang_song:
            bpm_song = all_songs[i]['bpm']
            if bpm_song == target_bpm:
                target_bpm_song.append(i)
            else:
                pass
        
        #Сепаратор 1
        if len(target_bpm_song) > 0:
            return target_bpm_song[randint(0,len(target_bpm_song)-1)]
        elif len(target_bpm_song) == 0:
            # Расширяем диапазон +/-2
            if target_bpm > 0:
                bpm_range.clear()
                bpm_range.append(target_bpm + 2)
                bpm_range.append(target_bpm - 2)
                print(bpm_range)
            else:
                print('BPM Не может быть равен 0! Измените начальный BPM')
                return None
            
            

        else:
            print ('В методе MAGIC_ROTATOR произошла ошибка! Блок изменения диапазона BPM')
        
        #
        # 
        # return target_bpm_song
    


        
        #return lang_song



            
            
            
            # Сепаратор 1 - собираем id песен которые удовлетворяют целевому бипиэм
            # Если песн нет расширяем диапазон +/-2
            # Сепараор 2 - собираем id песен которые удволетворяют джиапазону
            # если песн нет меняем диапазон - целевой *2 +/-2
            # Сепаратор 3
            # Если песн нет меняем диапазон от целевого //2 +/-2
            # Если песн нет возвращзаем строку - "Песен с заданными параметрами нет"

        pass


    def song_1(self) -> int:
        """Правила подбора первой песни"""
        #найти песню с нужным bpm и страной
        lang = 'ru'
        bpm = first_bpm

        song = self.magic_rotator(lang, bpm)

        return song

        



        

    def song_2(self) -> int:
        pass

    def song_3(self) -> int:
        pass

    def song_4(self) -> int:
        pass

    def song_5(self) -> int:
        pass

    def song_6(self) -> int:
        pass

    def song_7(self) -> int:
        pass

    def song_8(self) -> int:
        pass

    def song_9(self) -> int:
        pass

    def song_10(self) -> int:
        pass

    def song_11(self) -> int:
        pass

    def song_12(self) -> int:
        pass
    

class Playlist(Conditions):
    def __init__(self):
        """Подбирает песни и формирует текстовый файл"""
        super().__init__(song_folder)
        pass

    def get_playlist(self, file_name):
        """Формирует плейлист обращаясь к классу условия"""
        pass




# Экземпляры
folder = Folder(song_folder)
song = Songs(song_folder)
songs = Conditions(song_folder)

# Вызовы
#print (song.rus_song())
#print (song.eng_song())
#print(song.bpm_eng_song())
#print(song.bpm_rus_song())
#print(song.bpm_eng_song().keys())
#print(song.all_songs_dict())
#song.bpm_dict()
#print (song.rus_song())
print (songs.song_1())


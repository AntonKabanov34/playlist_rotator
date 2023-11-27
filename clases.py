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

    def copy_file(self):
        """Копирует фалы в папку"""

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
        if artist_name in ['gorkypark', 'zivert']:
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
        self.song_id = []
        pass

    # Cкрипты поиска
    def bpm_target_serch(self, lang_song:dict, target_bpm) -> list:
        """Возвращает список ID песен с целевым BPM"""
        # Полный список песен
        all_songs = self.all_songs_dict()
        response = []
        for i in lang_song:
            bpm_song = all_songs[i]['bpm']
            if bpm_song == target_bpm:
                response.append(i)
            else:
                pass
        
        return response

    def bpm_range_serch(self, lang_song:dict, bpm_range:list) -> list:
        """"Производит поиск ID композиций которые попадают в диапазон bpm_range"""
        all_songs = self.all_songs_dict()
        response = []

        for i in lang_song:
            bpm_song = all_songs[i]['bpm']
            if bpm_range[0] <= bpm_song <= bpm_range[-1]:
                response.append(i)
            else:
                pass
        return response

    def bpm_nearest_song(self, lang_song:dict, target_bpm:int) -> int:
        """Ищет ближайшую песню c близким к целевому BPM"""
        pass

    # Вычисления BPM
    def bpm_range_1(self, target_bpm:int) -> list:
        """Первый диапазон BPM +/-2 от входящего"""
        response = []
        if target_bpm <= 0:
            print ('BPM не может быть меньше или равен 0')
            target_bpm = 1
            return [1, target_bpm, 1]
        elif target_bpm > 0:
            a = target_bpm + 2
            b = target_bpm - 2
            response.append(1) if b < 0 else b
            response.append(target_bpm)
            response.append(a)
        return response

    def bpm_range_2(self, target_bpm:int) -> list:
        """"Целевой диапазон *2 +/- 2"""
        new_target_bpm = target_bpm *2
        response = []
        if target_bpm <= 0:
            print ('BPM не может быть меньше или равен 0')
            target_bpm = 1
        else:
            pass

        if new_target_bpm > 0:
            a = new_target_bpm + 2
            b = new_target_bpm - 2
            response.append(1) if b < 0 else b
            response.append(target_bpm)
            response.append(a)
        return response

        


        pass
    
    def bpm_range_3(self, target_bpm:int) -> list:
        """"Целевой диапазон //2 +/- 2"""
        
        response = []
        
        if target_bpm <= 0:
            print ('BPM не может быть меньше или равен 0')
            target_bpm = 1
        else:
            pass

        new_target_bpm = target_bpm // 2

        if new_target_bpm  <= 1:
            new_target_bpm = 1
        else:
            pass

        if new_target_bpm > 0:
            a = new_target_bpm + 2
            b = new_target_bpm - 2
            response.append(b) if b > 0 else 1
            response.append(new_target_bpm)
            response.append(a)
        return response
        
    def random_bpm(self, target_bpm) -> int:
        """"Рандомизирует целевой BPM для поиска"""
        action = [1,2,3,4]
        r = randint(0, len(action) - 1)

        if action[r] == 1:
            target_bpm = target_bpm + 5
            return target_bpm
        elif action[r] == 2:
            target_bpm = target_bpm - 5
            return target_bpm
        elif action[r] == 3:
            target_bpm = target_bpm * 2
            return target_bpm
        elif action[r] == 4:
            target_bpm = target_bpm // 2
            return target_bpm
        pass
    
    # Алгоритм ротатора
    def magic_rotator(self, lang, target_bpm) -> int:
        """Находит только лучшие песни"""
        
        # список id целевых песен песен
        lang_song = None #Целевой словарь

        # Формируем целевой словарь
        if lang == 'ru':
            lang_song = self.lang_songs('ru')
        elif lang == 'eng':
            lang_song = self.lang_songs('eng')
        else:
            print ('!!!!!!!!Что-то пошло не так в методе MAGIC_ROTATOR, блоке определения языковой подборки!!!!!!!!!') 

        # Собираем список песен с целевым BPM
        target_bpm_song = self.bpm_target_serch(lang_song, target_bpm)
        
        
        #Сепаратор 1 (если есть песни с целевым bpm)
        if len(target_bpm_song) > 0:
            return target_bpm_song[randint(0,len(target_bpm_song)-1)]
        
        # Сепаратор 2 (если нет песен с целевым bpm)
        elif len(target_bpm_song) == 0:
            bpm_range = self.bpm_range_1(target_bpm)
            target_bpm_song = self.bpm_range_serch(lang_song, bpm_range)
            if len(target_bpm_song) > 0:
                return target_bpm_song[randint(0,len(target_bpm_song)-1)]
            
            # Сепаратор 3 (если нет песен с целевым +/- 2 bpm)
            else:
                bpm_range = self.bpm_range_2(target_bpm)
                target_bpm_song = self.bpm_range_serch(lang_song, bpm_range)
                if len(target_bpm_song) > 0:
                    return target_bpm_song[randint(0,len(target_bpm_song)-1)]
                
                # Сепаратор 4 (если нет песен с целевым *2 +/- 2) 
                else:
                    bpm_range = self.bpm_range_3(target_bpm)
                    target_bpm_song = self.bpm_range_serch(lang_song, bpm_range)
                    if len(target_bpm_song) > 0:
                        return target_bpm_song[randint(0,len(target_bpm_song)-1)]
                    else:
                        # КОСТЫЛЬ! Дописать алгоритм поиска ближайшей по BPM песни
                        return None
        else:
            print ('В методе MAGIC_ROTATOR произошла ошибка! Блок изменения диапазона BPM')
        pass
     
    def search_songs(self,lang, bpm) -> int:
        """Добавляет песни в плейлист"""
        flag = 10
        song = self.magic_rotator(lang, bpm)
        if song not in self.song_id:
            return song
        else:
            while song in self.song_id:
                print(f'Мы в вечном цикле. Флаг {flag}')
                song = self.magic_rotator(lang, bpm)
                flag -= 1
                if flag <= 0:
                    print('Выходим из цикла по флагу')
                    break
        
        return None

    def serch_end_bpm(self):
        """Ищет ближайший BPM"""
        for i in reversed(self.song_id):
            if isinstance(i, int):
                return self.all_songs_dict()[i]['bpm']
            else:
                print('Поиск последнего BPM прошел неудачно. Вернул случайное значение 90-120')
                return randint(90,130)


    # Правила плейлиста
    def song_1(self) -> int:
        """Правила подбора первой песни"""
        lang = 'ru'
        bpm = first_bpm
        song = self.magic_rotator(lang, bpm)
        self.song_id.append(song)
        print(f'Первая песня добавлена {song}')
        print(self.song_id)
        pass
    
    def song_2(self) -> int:
        lang = 'ru'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Вторая песня добавлена {song}')
        else:
           print ('Песня не найдена')
           bpm = self.serch_end_bpm()
           song = self.search_songs(lang, bpm)
           self.song_id.append(song)
           print(f'Вторая песня добавлена {song} использвоанием поиска BPM')

    def song_3(self) -> int:
        lang = 'eng'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Третья песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Третья песня добавлена {song} с использвоанием поиска BPM')

    def song_4(self) -> int:
        lang = 'ru'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Четвертая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Четвертая песня добавлена {song} с использвоанием поиска BPM')
 
    def song_5(self) -> int:
        lang = 'ru'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Пятая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Пятая песня добавлена {song} с использвоанием поиска BPM')

    def song_6(self) -> int:
        lang = 'eng'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Шестая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Шестая песня добавлена {song} с использвоанием поиска BPM')

    def song_7(self) -> int:
        lang = 'ru'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Седьмая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Седьмая песня добавлена {song} с использвоанием поиска BPM')

    def song_8(self) -> int:
        lang = 'ru'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Восьмая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Восьмая песня добавлена {song} с использвоанием поиска BPM')

    def song_9(self) -> int:
        lang = 'eng'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Девятая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Девятая песня добавлена {song} с использвоанием поиска BPM')
 
    def song_10(self) -> int:
        lang = 'ru'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Десятая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Десятая песня добавлена {song} с использвоанием поиска BPM')

    def song_11(self) -> int:
        lang = 'ru'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Одинадцатая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'Одинадцатая песня добавлена {song} с использвоанием поиска BPM')

    def song_12(self) -> int:
        lang = 'eng'
        if isinstance(self.song_id[-1], int):
            bpm = self.random_bpm(self.all_songs_dict()[self.song_id[-1]]['bpm'])
            song = self.search_songs(lang, bpm)
            self.song_id.append(song)
            print(f'Двенадцатая песня добавлена {song}')
        else:
         print ('Песня не найдена')
         bpm = self.serch_end_bpm()
         song = self.search_songs(lang, bpm)
         self.song_id.append(song)
         print(f'ДВенадцатая песня добавлена {song} с использвоанием поиска BPM')

   
   # Сборка плейлиста
    def run(self):
        """Собирает ПЛЕЙЛИСТ"""
        #self.song_id.clear()
        self.song_1()
        self.song_2()
        self.song_3()
        self.song_4()
        self.song_5()
        self.song_6()
        self.song_7()
        self.song_8()
        self.song_9()
        self.song_10()
        self.song_11()
        self.song_12()
        print(self.song_id)

    def txt_file(self):
        """Преобразовывает ID в название песен"""
        all_songs = self.all_songs_dict()
        response = []
        for index, item in enumerate(self.song_id, start=1):
            if item != None:
                print(f"{index} - {all_songs[item]['all_name']}")
            else:
                print(f"{index} - Песня не найдена")


# Экземпляры
folder = Folder(song_folder)
song = Songs(song_folder)
songs = Conditions(song_folder)


# Вызовы
songs.run()
songs.txt_file()




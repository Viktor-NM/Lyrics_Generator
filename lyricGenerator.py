import requests
from bs4 import BeautifulSoup
import json
from os import system
from time import sleep

class Generator:
    def __init__(self):
        self.lyrics = []
        self.song_list = {}

        with open('lyrics.json') as lyrics_json:
            if lyrics_json:
                self.data = json.load(lyrics_json)

                for t in self.data:
                    self.song_list[t] = self.data[t]

    #Busqueda desde genius si existe letra
    def __s_genius(self):
        url = f'https://genius.com/{self.artist.replace(" ", "-")}-{self.song.replace(" ", "-")}-lyrics'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        resultset = soup.find_all('div', attrs={'class': "Lyrics__Container-sc-1ynbvzw-2 jgQsqn"})

        return resultset

    #Busqueda desde azlyrics si existe letra
    def __s_azlyrics(self):
        url = f'https://www.azlyrics.com/lyrics/{self.artist.replace(" ", "")}/{self.song.replace(" ", "")}.html'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        resultSet = soup.find_all('div', attrs={'class': ''})

        return resultSet

    #Repetir la busqueda en ambas paginas por si no esta diponible
    def __rep_search(self):
        state = False

        while not state:
            genius = self.__s_genius()
            azlyrics = self.__s_azlyrics()

            if genius:
                state = True
                return genius

            elif azlyrics:
                state = True
                return azlyrics

    #Generar letra
    def generate(self, artist, song):

        self.artist = artist; self.song = song
        result = self.__rep_search()

        for divs in result:
            div = divs.strings
            for d in div:
                self.lyrics.append(str(d).strip('\n'))

        for word in range(len(self.lyrics)-1,-1,-1):
            if self.lyrics[word] == '':
                self.lyrics.pop(word)

        self.__save_song()

        return self.lyrics

    #Guarda el historial de busquedas en un diccionario
    def __save_song(self):
        self.song_list[f'{self.artist.title()} - {self.song.title()}'] = {'artist': self.artist, 'song': self.song, 'lyrics': self.lyrics}

    #Genera un archivo json con las canciones buscadas
    def generate_json(self):
        with open('lyrics.json', 'w') as lyrics_json:
            json.dump(self.song_list, lyrics_json)

    #Muestra las canciones buscadas
    def show_history(self):
        title = list(self.data.keys())
        if title:
            for t in title:
                print(f'{title.index(t) + 1}.- {t}')
        else:
            print('No hay ninguna cancion en tu historial')

    #Comprueba si la letra de la cancion ya existe
    def compare_to(self, artist, song):
        key_song_list = list(self.song_list.keys())

        return True if f'{artist.title()} - {song.title()}' in key_song_list else False

    #Regresa la letra de la cancion ya existente
    def lyrics_of(self, title):
        return self.song_list[title]['lyrics']

lyrics = Generator()
r = 'y'

def menu():
    system('cls')
    lyrics.show_history()
    artist = input('\nIngresa el nombre de un artista/banda: ')
    song = input('Ingresa el nombre de una cancion: ')

    return artist, song

while r =='y':
    artist, song = menu()
    system('cls')

    if lyrics.compare_to(artist, song):
        l = lyrics.lyrics_of(f'{artist.title()} - {song.title()}')

    else:
        l = lyrics.generate(artist, song)
        lyrics.generate_json()

    print(f'\n{"-"*8} {song.capitalize()} by {artist.title()} {"-"*8}')
    for p in l:
        print(p)

    r = input('\nDesea buscar otra letra? [Y/n]: ').lower()

    if r != 'y':
        system('cls')
        print('Saliendo...')
        sleep(0.3)







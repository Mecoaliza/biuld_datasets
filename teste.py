import urllib, urllib.error
from functions import save_in_database
from urllib import parse
import json
import requests
import sqlite3

def print_json(json_data):
    list_keys=['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 
               'Actors', 'Plot', 'Language', 'Country', 'Awards',
               'Metascore', 'imdbRating', 'imdbVotes', 'imdbID', 'BoxOffice']
    print("-"*50)
    for i in list_keys:
        if i in list(json_data.keys()):
            print(f"{i}: {json_data[i]}")
    print("-"*50)



def search_movie(title):
    if len(title) < 1 or title=='quit': 
        print("Não encontrado...")
        return 

    try:
        title_url = parse.urlencode({'t': title})  #http://www.omdbapi.com/?t=Barbie&y=2023 &{'y': year}
        year_url = parse.urlencode({'y': year})
        api_key = '9019e34'
        url = f'http://www.omdbapi.com/?{title_url}&{year_url}&apikey={api_key}'
        print(f'Procurando o filme "{title}"... ')
        uh = urllib.request.urlopen(url)
        data = uh.read()
        json_data=json.loads(data)
        
        if json_data['Response']=='True':
            print_json(json_data)
            save_database =input('Salvar o filme no banco de dados? Digite "sim" ou "não": ').lower()
            if save_database =='sim':
                save_in_database(json_data)
        else:
            print("Erro encontrado: ",json_data['Erro'])
    
    except urllib.error.URLError as e:
        print(f"ERROR: {e.reason}")


def save_in_database(movie_data):
    conn = sqlite3.connect('movie.sqlite')
    cur=conn.cursor()

    cur.execute ('''CREATE TABLE IF NOT EXISTS filmes (
        title TEXT,
        year INTEGER,
        rated TEXT,
        released TEXT,
        runtime TEXT,
        genre TEXT,
        director TEXT,
        writer TEXT,
        actors TEXT,
        plot TEXT,
        language TEXT,
        country TEXT,
        awards TEXT,
        metascore INTEGER,
        imdbRating REAL,
        imdbVotes TEXT,
        imdbID TEXT,
        boxOffice TEXT
    )
''')

    conn.execute('INSERT INTO filmes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
             (movie_data['Title'], movie_data['Year'], movie_data['Rated'], movie_data['Released'], movie_data['Runtime'],
              movie_data['Genre'], movie_data['Director'], movie_data['Writer'], movie_data['Actors'], movie_data['Plot'],
              movie_data['Language'], movie_data['Country'], movie_data['Awards'], movie_data['Metascore'],
              movie_data['imdbRating'], movie_data['imdbVotes'], movie_data['imdbID'], movie_data['BoxOffice']))
    conn.commit()
    conn.close()


title = input('\nDigite o nome do filme: ')
year = input('\nDigite o ano: ')
if len(title) < 1 or title=='quit': 
    print("Não encontrado...")
else:
    movie_data = search_movie(title)
    if movie_data is not None:
        save_in_database(movie_data)
import sqlite3
import pandas as pd


def save_in_database(json_data):
    # filename = input("Digite o nome do filme: ")
    # filename = filename+'.sqlite'

    conn = sqlite3.connect('movies.db')
    cur=conn.cursor()


    cur.execute ('''CREATE TABLE IF NOT EXISTS filmes (
        title TEXT,
        year INTEGER,
        rated TEXT,
        released TEXT,
        runtime INTEGER,
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
        imdbID TEXT
    )
''')
    
    data = search_movie()

    # cur.execute('SELECT Title FROM MovieInfo WHERE Title = ? ', (title,))
    conn.execute('INSERT INTO filmes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
             (data['title'], data['year'], data['rated'], data['released'], data['runtime'],
              data['genre'], data['director'], data['writer'], data['actors'], data['plot'],
              data['language'], data['country'], data['awards'], data['metascore'],
              data['imdbRating'], data['imdbVotes'], data['imdbID']))
    conn.commit()
    conn.close()
    



def print_database(database):
    conn = sqlite3.connect(str(database))
    cur=conn.cursor()

    for row in cur.execute('SELECT * FROM MovieInfo'):
        print(row)
    conn.close()



def save_in_excel(filename, database):

    if filename.split('.')[-1]!='xls' and filename.split('.')[-1]!='xlsx':
        print ("O arquivo não está com a extensão correta. Tente novamente!")
        return 
    

    conn = sqlite3.connect(str(database))

    df = pd.read_sql_query('SELECT * FROM MovieInfo', conn)
    conn.close()

    df.to_excel(filename,sheet_name='Movie_Info')







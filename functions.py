import sqlite3
import pandas as pd


def save_in_database(json_data):
    filename = input("Digite o nome do filme: ")
    filename = filename+'.sqlite'

    conn = sqlite3.connect(str(filename))
    cur=conn.cursor()

    title = json_data['Title']
    if json_data['Year']!='N/A':
        year = int(json_data['Year'])
    if json_data['Runtime']!='N/A':
        runtime = int(json_data['Runtime'].split()[0])
    if json_data['Country']!='N/A':
        country = json_data['Country']
    if json_data['Metascore']!='N/A':
        metascore = float(json_data['Metascore'])
    else:
        metascore=-1
    if json_data['imdbRating']!='N/A':
        imdb_rating = float(json_data['imdbRating'])
    else:
        imdb_rating=-1


    cur.execute('''CREATE TABLE IF NOT EXISTS MovieInfo 
    (Title TEXT, Year INTEGER, Runtime INTEGER, Country TEXT, Metascore REAL, IMDBRating REAL)''')
    
    cur.execute('SELECT Title FROM MovieInfo WHERE Title = ? ', (title,))
    row = cur.fetchone()



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







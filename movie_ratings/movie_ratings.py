from bs4 import BeautifulSoup
import pandas as pd
import requests
import sqlite3
from log_manager import logger
from time import time

def imdb_crawl():
    start_time = time()
    headers = {
        'authority': 'www.imdb.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
     }
    title_list = list()
    year_list = list()
    rating_list = list()
    start_list = ['1','51','101','151']
    logger.info('Requesting IMDB...')
    for start in start_list:
        params = (
            ('title_type', 'feature'),
            ('year', '2021-01-01,2021-12-31'),
            ('start', f'{start}'),
            ('ref_', 'adv_prv'),
        )
        response = requests.get('https://www.imdb.com/search/title/', headers=headers, params=params)
        logger.info(f'Response status from IMDB :{response.status_code}')
        if response.status_code != 200:
            print(response)
            return response,[], True
        text = response.content
        soup = BeautifulSoup(text,'lxml')
        for d in soup.find_all('div',class_ ="lister-list"):
            for div in d.find_all('div',class_='lister-item mode-advanced'):
                tt = div.find('div',class_ = 'lister-item-image float-left')
                tt1 = tt.find('img',class_ = 'loadlate')
                tt_title = tt1['alt']                           #title
                tt_number = tt1['data-tconst']                  #unique number for every movie
                for div1 in div.find_all('div',class_ = 'lister-item-content'):
                    try:
                        title = div1.find('a', href=f"/title/{tt_number}/?ref_=adv_li_tt").text
                        year = div1.find('span', class_ ="lister-item-year text-muted unbold").text.lstrip('I) (').rstrip(')')
                        rating = div1.find('div',class_ ="inline-block ratings-imdb-rating")['data-value']
                        title_list.append(title)
                        year_list.append(year)
                        rating_list.append(rating)
                    except Exception as e:
                        logger.exception('Error occurred :{e}')
                        pass
    dic_imdb = {
        'Rating': rating_list,
        'Title': title_list,
        'Year':year_list
    }
    df_imdb = pd.DataFrame(dic_imdb)
    logger.info('Request Completed From IMDB...')
    logger.info(f'Total values from IMDB:{len(df_imdb)}')
    end_time = time()
    logger.info(f'Execution Time for IMDB: {end_time - start_time}')
    return df_imdb, title_list , False

def rotten_crawl(title_list):
    start_time = time()
    headers = {
        'authority': 'www.rottentomatoes.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    }

    params = (('year', '2021'),)
    logger.info('Requesting Rotten Tomatoes...')
    response = requests.get('https://www.rottentomatoes.com/top/bestofrt/', headers=headers, params=params)
    logger.info(f'Response status from Rotten tomatoes:{response.status_code}')
    if response.status_code != 200:
        return response, True
    text_rotten = response.content
    try:
        df = pd.read_html(text_rotten)[2]
    except ValueError:
        logger.exception('HTML table not found.')
        return [] , False
    df.drop(['No. of Reviews','Rank'], axis = 1,inplace = True)
    df = df.merge(df.Title.apply(lambda t: pd.Series({'Title_new':t.split(' (')[0],
                                                 'Year':t.split(' (')[-1].strip(')')})), 
             left_index=True, right_index=True)
    df.drop(['Title'], axis = 1,inplace = True)
    df.rename(columns = {'RatingTomatometer':'Rating', 'Title_new':'Title'}, inplace = True)
    df['mask'] = df.Title.apply(lambda t: pd.Series(t in title_list))
    index_names = df[ df['mask'] == True ].index
    df.drop(index_names,inplace = True)
    df.drop(columns = 'mask',inplace = True)
    logger.info('Request Completed From Rotten Tomatoes...')
    logger.info(f'Total values from Rotten Tomatoes:{len(df)}')
    end_time = time()
    logger.info(f'Execution Time for Rotten Tomatoes: {end_time - start_time}')
    return df, False

def insert_data(results):
    logger.info(f'Total values to insert in DB:{len(results)}')
    logger.info('Connecting to DB... "movie_ratings.db"')
    con = sqlite3.connect("movie_ratings.db") # db name
    cur = con.cursor()
    logger.info('Check if movie_rating table exists in the DB...')
    table_exists_check = """SELECT name FROM sqlite_master WHERE type='table' AND name='movie_rating'; """
    listOfTables = cur.execute(table_exists_check).fetchall()
    if listOfTables == []:
        logger.info('Table "movie_rating" not found!')
    else:
        logger.warning('Table "movie_rating" found!')
        logger.info('Dropping existing table "movie_rating"...')
        cur.execute(''' DROP table movie_rating''')
        logger.info('Dropped table "movie_rating"')
    sql_create = '''CREATE TABLE movie_rating
                (id INTEGER PRIMARY KEY, 
                rating TEXT NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL);'''
    logger.info(f'SQL for creating table "movie_rating":{sql_create}')
    cur.execute(sql_create)
    logger.info(f'Table created!!!')
    logger.info(f'Inserting data into table "movie_rating"...')
    for i,r,t,y in results.itertuples():
        sql_insert = f'''INSERT INTO movie_rating (rating, title, year)
                    VALUES ('{r}',"{t}",'{y}')'''
        # print(sql_insert)
        # logger.info({sql_insert})
        cur.execute(sql_insert)
    con.commit()
    logger.info('Data inserted successfully!!!')
    logger.info('Disconnecting DB...')
    con.close()
    logger.info('Disconnected...')
    logger.info('Request Completed Data Scrapped Successfully!!!')
    html = results.to_html(index = False)
    logger.info('Writing Table to HTML file..')
    with open ("result_table.html", "w") as text_file: 
        text_file.write(html)
    logger.info('HTML file created!!!')

program_start_time = time()
logger.info('Scraping Movies....')
df_imdb,title_list, fails_imdb = imdb_crawl()
if fails_imdb:
    logger.error('Request Failed From IMDB...')
else:
    df , fails_rotten = rotten_crawl(title_list)
    if fails_rotten:
        logger.error('Request Failed From Rotten Tomatoes...')
    else:
        logger.info('Creating resultant Dataframe...')
        results = pd.concat([df_imdb,df])
        logger.info('Calling insert data function')
        insert_data(results)
program_end_time = time()
logger.info(f'Total Execution Time: {program_end_time-program_start_time}')



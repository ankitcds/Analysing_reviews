from home.log_manager import logger
import sqlite3
import pandas as pd
def fetch_review(color,style_name):
    logger.info('Connecting to DB')
    con = sqlite3.connect("home\iphone-review.db") # db name
    logger.info('Creating a cursor')
    cur = con.cursor()
    color = color.title()
    style_name = style_name.upper()
    if color.lower() in 'red':   #checking color red because it is there in DB as "(PRODUCT)RED"
        color = '(PRODUCT)RED'
    logger.info('Selecting data from DB')
    
    sql = f''' SELECT * FROM review_data
               WHERE color = '{color}'
               and style_name = '{style_name}' '''
               
    logger.info(f'SQL Query:{sql}')
    df = pd.read_sql_query(sql,con)
    review_details = df.to_dict(orient= 'records')
    cur.close()
    logger.info('Disconnecting to DB')
    return review_details
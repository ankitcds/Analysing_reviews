import csv, sqlite3

con = sqlite3.connect("iphone-review.db") # db name
cur = con.cursor()

cur.execute('''CREATE TABLE review_data 
            (color, review, review_of_text, 
            review_title,style_name,
            verified_purchase);''') # use your column names here

with open('iphone_review\\review_data.csv','r',encoding='utf-8') as fin:   #opening csv to insert data from it to DB
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['color'], i['review'], i['review_of_text'],
              i['review_title'],i['style_name'],
              i['verified_purchase']) for i in dr]

cur.executemany('''INSERT INTO review_data 
                (color, review, review_of_text,
                review_title,style_name, 
                verified_purchase)
                VALUES (?,?,?,?,?,?);''', to_db)
con.commit()
con.close()
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("iphone_review_data1.csv") #(,encoding = '')
 
comment_words = ''
stopwords = set(STOPWORDS)
print(df.head())

# iterate through the csv file
for val in df.review:    #df.column_name
    # typecaste each val to string
    #val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converting each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 1200, height = 1200,
                background_color ='red',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()
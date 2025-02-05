# NLTK already has a built-in, pretrained sentiment analyzer called VADER (Valence Aware Dictionary and sEntiment Reasoner).
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
data_df = pd.read_csv('review_data.csv')
print(data_df.shape)
print(data_df.head())
data_df['Negative'] = ''
data_df['Neutral'] = ''
data_df['Positive'] = ''
data_df['Compound'] = ''

sia = SentimentIntensityAnalyzer()
sia.polarity_scores("Wow, NLTK is really powerful!")
for i in range(len(data_df)):
    a = sia.polarity_scores(data_df['review'][i])
    data_df['Negative'][i] = a['neg']
    data_df['Neutral'][i] = a['neu']
    data_df['Positive'][i] = a['pos']
    data_df['Compound'][i] = a['compound']
print(data_df.head())
data_df['Sentiment'] = ''
for i in range(len(data_df)):
    if (data_df['Compound'][i] > -0.25) & (data_df['Compound'][i] < 0.25):
        data_df['Sentiment'][i] = 'Neutral'
    if data_df['Compound'][i] <= -0.25:
        data_df['Sentiment'][i] = 'Negative'
    if data_df['Compound'][i] >= 0.25:
        data_df['Sentiment'][i] = 'Positive'
# NLTK already has a built-in, pretrained sentiment analyzer called VADER (Valence Aware Dictionary and sEntiment Reasoner).
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
from home.log_manager import logger

def analyse_sentiment(data_df):
    logger.info(f'Review Dataframe:{data_df}')
    logger.info('Creating columns in dataframe : Negative, Neutral, Positive, Compound')
    data_df['Negative'] = ''
    data_df['Neutral'] = ''
    data_df['Positive'] = ''
    data_df['Compound'] = ''

    sia = SentimentIntensityAnalyzer()
    sia.polarity_scores("Wow, NLTK is really powerful!")

    i = 0
    a = sia.polarity_scores(data_df['review'][i])
    logger.info('Assigining Values to those columns after calculation')
    data_df['Negative'][i] = a['neg']
    data_df['Neutral'][i] = a['neu']
    data_df['Positive'][i] = a['pos']
    data_df['Compound'][i] = a['compound']
    
    data_df['Sentiment'] = ''
    if (data_df['Compound'][i] > -0.25) & (data_df['Compound'][i] < 0.25):
        data_df['Sentiment'][i] = 'Neutral'
    if data_df['Compound'][i] <= -0.25:
        data_df['Sentiment'][i] = 'Negative'
    if data_df['Compound'][i] >= 0.25:
        data_df['Sentiment'][i] = 'Positive'
    logger.info('Sentiment Analysed...')
    sentiment_dic = data_df.to_dict(orient= 'records')
    return sentiment_dic
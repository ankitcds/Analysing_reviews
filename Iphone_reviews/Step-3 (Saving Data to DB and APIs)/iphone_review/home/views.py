from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from home.authenticator import check_if_missing
from home.fetching_reviews import fetch_review
from home.sentiment_analysis import analyse_sentiment
from home.log_manager import logger
import json
import pandas as pd

@csrf_exempt
@api_view(['GET', 'POST'])
def get_reviews(request):
    if request.method == 'POST':
        out = {
            "status": 405,
            "message": "Request method 'POST' not supported",
            "data": None
        }
        logger.debug('Request method "POST" not supported')
        return JsonResponse(out)
    logger.info('Request Started')
    color = request.GET.get('color','')
    style_name = request.GET.get('storage_size','')
    logger.info(f'color:{color},style_name:{style_name}')
    logger.info('Checking if any parameter is missing')
    found, out = check_if_missing(color = color, style_name = style_name) #checking if any parameter is missing 
    logger.info(f'found:{found},out:{out}')
    if found:
        return JsonResponse(out)
    
    logger.info('fetching reviews from DB')
    review_details = fetch_review(color,style_name)  #fetching reviews based on given parameters from DB 
    logger.info('Reviews fetched')
    out = {
        'status':'200',
        'message':'OK',
        'reviews': review_details
    }
    
    logger.info(f"Request Completed with Status:{out.get('status')} and Message:{out.get('message')}")
    return JsonResponse(out)

@csrf_exempt
@api_view(['GET', 'POST'])
def sentiment_analysis(request):
    out = ''
    if request.method == 'POST':
        out = {
            "status": 405,
            "message": "Request method 'POST' not supported",
            "data": None
        }
        logger.debug('Request method "POST" not supported')
        return JsonResponse(out)
    logger.info('Request Started')
    body_unicode = request.body.decode('utf-8')
    review_body = json.loads(body_unicode)
    color = review_body.get('color', '')
    review = review_body.get('review', '')
    review_of_text = review_body.get('review_of_text', '')
    review_title = review_body.get('review_title', '')
    style_name = review_body.get('style_name', '')
    verified_purchase = review_body.get('verified_purchase', '')
    logger.info('Checking if any parameter is missing')
    found , out = check_if_missing(color = color,
                                   review = review,
                                   review_body = review_body,
                                   review_of_text= review_of_text,
                                   review_title= review_title,
                                   style_name= style_name,
                                   verified_purchase= verified_purchase)  # check if request body is missing
    logger.info(f'found:{found},out:{out}')
    if found:
        return JsonResponse(out)
    
    data_df = pd.DataFrame()
    data_df = data_df.append(review_body, ignore_index=True)
    logger.info('Analysing Sentiments of the review...')
    sentiment_dic = analyse_sentiment(data_df)   #calling sentiment analysis function
    logger.info('Analysis Completed')
    out = {
        'status':200,
        'message':'OK',
        'sentiment result': sentiment_dic
        }
    logger.info(f"Request Completed with Status:{out.get('status')} and Message:{out.get('message')}")
    return JsonResponse(out)



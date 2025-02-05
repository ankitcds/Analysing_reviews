from home.log_manager import logger

def check_if_missing(**params):
    missing_params = list()
    if params.get('color', "-") == "":
        missing_params.append({'message': "Missing request parameter color"})
        
    if params.get('style_name', "-") == "":
        missing_params.append({'message': "Missing request parameter storage size/style name"})
        
    if params.get('review_of_text', "-") == "":
        missing_params.append({'message': "Missing request parameter review_of_text"})
    
    if params.get('review', "-") == "":
        missing_params.append({'message': "Missing request parameter review"})
    
    if params.get('review_title', "-") == "":
        missing_params.append({'message': "Missing request parameter review_title"})
    
    if params.get('verified_purchase', "-") == "":
        missing_params.append({'message': "Missing request parameter verified_purchase"})
        
    if missing_params:
        out = {
            "status": 400,
            "message": ";".join([mp.get('message', '') for mp in missing_params]),
            "data": None
        }
        logger.error(f'Missing Parameters')
        return True, out
    else:
        return False, {}
import requests
import json

def emotion_detector(text_to_analyze):
    """
    Sends text to the Watson NLP Emotion Prediction API and returns emotion scores.
    Handles blank text and API errors gracefully.
    
    Args:
        text_to_analyze (str): The text to analyze.
    
    Returns:
        dict: A dictionary containing emotion scores and the dominant emotion.
              All values are None if an error occurs.
    """
    # Handle blank input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    try:
        response = requests.post(url, headers=headers, json=input_json)
        
        # If the API returns a 400 status code (bad request)
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        # Parse the JSON response
        response_dict = json.loads(response.text)
        emotions = response_dict['emotionPredictions'][0]['emotion']
        
        # Extract individual emotion scores
        anger_score = emotions.get('anger', 0.0)
        disgust_score = emotions.get('disgust', 0.0)
        fear_score = emotions.get('fear', 0.0)
        joy_score = emotions.get('joy', 0.0)
        sadness_score = emotions.get('sadness', 0.0)
        
        # Build the scores dictionary
        scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        # Find the dominant emotion (highest score)
        if all(score == 0.0 for score in scores.values()):
            dominant_emotion = None
        else:
            dominant_emotion = max(scores, key=scores.get)
        
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
        
    except (KeyError, json.JSONDecodeError, requests.exceptions.RequestException) as e:
        # Catch any other errors (network issues, malformed JSON, etc.)
        print(f"Error in emotion_detector: {e}")
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
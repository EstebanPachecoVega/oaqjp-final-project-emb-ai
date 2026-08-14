import requests
import json

def emotion_detector(text_to_analyze):
    """
    Envía el texto a la API de Watson NLP para predecir emociones.
    Retorna un diccionario con las puntuaciones de ira, desagrado, miedo, alegría, tristeza
    y la emoción dominante.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    response = requests.post(url, headers=headers, json=input_json)
    
    # Convertir la respuesta de texto a diccionario
    try:
        response_dict = json.loads(response.text)
        # Extraer las emociones del primer elemento de emotionPredictions
        emotions = response_dict['emotionPredictions'][0]['emotion']
        anger_score = emotions.get('anger', 0.0)
        disgust_score = emotions.get('disgust', 0.0)
        fear_score = emotions.get('fear', 0.0)
        joy_score = emotions.get('joy', 0.0)
        sadness_score = emotions.get('sadness', 0.0)
        
        # Encontrar la emoción dominante (máxima puntuación)
        scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        # Si todas las puntuaciones son 0, la emoción dominante es None
        if all(score == 0.0 for score in scores.values()):
            dominant_emotion = None
        else:
            dominant_emotion = max(scores, key=scores.get)
        
        # Retornar el diccionario con el formato solicitado
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
    except (KeyError, json.JSONDecodeError) as e:
        # Si ocurre un error (respuesta no esperada), devolvemos un diccionario con valores por defecto
        return {
            'anger': 0.0,
            'disgust': 0.0,
            'fear': 0.0,
            'joy': 0.0,
            'sadness': 0.0,
            'dominant_emotion': None
        }
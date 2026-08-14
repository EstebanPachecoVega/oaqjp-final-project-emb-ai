"""
Emotion Detection Web Application using Flask
"""
from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """Renderiza la página principal (index.html)"""
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_endpoint():
    """
    Endpoint que recibe texto a analizar y devuelve la respuesta formateada.
    Parámetro: textToAnalyze (GET)
    """
    text_to_analyze = request.args.get('textToAnalyze', '')

    if not text_to_analyze.strip():
        return "Texto no proporcionado. Por favor, ingresa un texto para analizar.", 400

    result = emotion_detector(text_to_analyze)

    # Verificar si la respuesta es válida (dominant_emotion no None)
    if result['dominant_emotion'] is None:
        return "Texto inválido. Por favor, ingresa un texto válido para analizar.", 400

    # Formatear la salida según lo solicitado
    response = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
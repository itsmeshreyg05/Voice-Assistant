# vapi_app.py
import vapi_python as vapi_sdk
from detectors import detect_language
from flask import Flask, request, jsonify
from deep_translator import MyMemoryTranslator


vapi_sdk.api_key = "9f6d5698-e715-48e3-a3a7-11ea39bc294b"

app = Flask(__name__)

# Translate any text to English
def translate_to_english(text, src_lang):
    try:
        return MyMemoryTranslator(source=src_lang, target='en').translate(text)
    except Exception:
        return "(Translation unavailable)"

def start_session(vapi=None):
    if vapi is None:
        vapi = vapi_sdk
    text = vapi.transcribe_initial()
    lang = detect_language(text) or 'en'
    
    if not lang:
        vapi.send_tts("Sorry, what language would you like me to use?")
        text2 = vapi.transcribe_response()
        lang = detect_language(text2) or 'en'

    vapi.set_locale(lang)
    vapi.send_tts({
        'en': "Hi! How can I help you today?",
        'es': "¡Hola! ¿En qué puedo ayudarte?",
        'de': "Hallo! Wie kann ich dir helfen?",
        'hi': "नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ?"
    }.get(lang, "Hello! How can I help?"))

    vapi.on_user_utterance(lambda text: handle_utterance(text, vapi))

def handle_utterance(text, vapi=None):
    if vapi is None:
        vapi = vapi_sdk
    lc = text.lower()
    lang_switch = {
        'english': 'en', 'inglés': 'en', 'spanish': 'es',
        'español': 'es', 'deutsch': 'de', 'alemán': 'de',
        'hindi': 'hi', 'हिंदी': 'hi'
    }
    for k, code in lang_switch.items():
        if k in lc:
            vapi.set_locale(code)
            vapi.send_tts({
                'en': "Switched to English.",
                'es': "Cambiado al español.",
                'de': "Wir sprechen jetzt Deutsch.",
                'hi': "अब हम हिंदी में बात करेंगे।"
            }[code])
            return
    # Detect language and translate
    detected_lang = detect_language(text) or 'en'
    if detected_lang != 'en':
        translation = translate_to_english(text, detected_lang)
        response = f"{text} ({translation})"
    else:
        response = text
    vapi.send_tts(response)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('event')
    text = data.get('text', '')

    if event == 'call.started':
        start_session()
    elif event == 'user.said':
        handle_utterance(text)
    # Add more event handling as needed

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=5000)

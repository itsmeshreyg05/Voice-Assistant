# test_vapi_flow.py
from detectors import detect_language
from deep_translator import MyMemoryTranslator
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Mock Vapi interactions for testing
class MockVapi:
    def __init__(self):
        self.locale = None
        self.last_tts = None

    def transcribe_initial(self):
        return self._text_in

    def transcribe_response(self):
        return self._text_in

    def set_locale(self, lang):
        self.locale = lang

    def send_tts(self, text):
        self.last_tts = text

    def on_user_utterance(self, cb):
        self._callback = cb

def translate_to_english(text, src_lang):
    try:
        return MyMemoryTranslator(source=src_lang, target='en').translate(text)
    except Exception:
        return "(Translation unavailable)"

mock = MockVapi()

# Test sentences
for text in ["¿Cómo estás?", "Wie geht's?", "नमस्ते", "Bonjour"]:
    mock._text_in = text
    lang = detect_language(text) or "en"
    assert lang in ("es","de","hi","en","mr","fr"), f"Detected lang '{lang}' not supported, got: {lang} for input: {text}"
    mock.set_locale("en"); mock.last_tts = None

    # Run your session starter
    from vapi_lang import start_session
    start_session(vapi=mock)

    # Translate to English for test output
    if lang != 'en':
        translation = translate_to_english(text, lang)
        print(f"Input: {text[:10]}... Detected: {mock.locale} — Greeting: {mock.last_tts} — English: {translation}")
    else:
        print(f"Input: {text[:10]}... Detected: {mock.locale} — Greeting: {mock.last_tts}")

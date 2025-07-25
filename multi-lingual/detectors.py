# detectors.py
from fast_langdetect import detect as fl_detect
from lingua import LanguageDetectorBuilder

lingua_detector = (
    LanguageDetectorBuilder.from_all_languages()
    .with_low_accuracy_mode()
    .build()
)

def detect_language(text: str):
    # Try fast detection
    try:
        r = fl_detect(text)
        code = r["lang"]  # ISO 639‑1 e.g. 'es', 'de', 'hi'
        score = r["score"]
        if score >= 0.6:
            return code
    except:
        pass

    # Fallback with lingua
    lang = lingua_detector.detect_language_of(text)
    if lang:
        return lang.iso_code_639_1.lower()
    return None

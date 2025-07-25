# enhanced_chatbot.py
import os
import sys
import json
from langdetect import detect, DetectorFactory
from deep_translator import MyMemoryTranslator, LingueeTranslator, LibreTranslator
import pyttsx3
import random
import threading
import time

# For stable language detection
DetectorFactory.seed = 0

# Configure UTF-8 encoding for output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Language names mapped to ISO codes
LANGUAGE_CODES = {
    # Main languages
    'english': 'en', 'español': 'es', 'spanish': 'es', 'deutsch': 'de', 'german': 'de', 
    'hindi': 'hi', 'हिंदी': 'hi', 'français': 'fr', 'french': 'fr',
    # Additional European languages
    'russian': 'ru', 'русский': 'ru', 'italian': 'it', 'italiano': 'it',
    'portuguese': 'pt', 'português': 'pt', 'dutch': 'nl', 'nederlands': 'nl', 
    'greek': 'el', 'ελληνικά': 'el', 'polish': 'pl', 'polski': 'pl',
    'turkish': 'tr', 'türkçe': 'tr', 'czech': 'cs', 'čeština': 'cs', 
    'slovak': 'sk', 'slovenčina': 'sk', 'swedish': 'sv', 'svenska': 'sv',
    'norwegian': 'no', 'norsk': 'no', 'danish': 'da', 'dansk': 'da',
    'finnish': 'fi', 'suomi': 'fi', 'hungarian': 'hu', 'magyar': 'hu',
    'romanian': 'ro', 'română': 'ro', 'bulgarian': 'bg', 'български': 'bg',
    'croatian': 'hr', 'hrvatski': 'hr', 'albanian': 'sq', 'shqip': 'sq',
    'ukrainian': 'uk', 'українська': 'uk', 'serbian': 'sr', 'српски': 'sr',
    'slovenian': 'sl', 'slovenščina': 'sl', 'estonian': 'et', 'eesti': 'et',
    'latvian': 'lv', 'latviešu': 'lv', 'lithuanian': 'lt', 'lietuvių': 'lt',
    # Asian languages
    'chinese': 'zh', '中文': 'zh', 'japanese': 'ja', '日本語': 'ja', 
    'korean': 'ko', '한국어': 'ko', 'vietnamese': 'vi', 'tiếng việt': 'vi',
    'thai': 'th', 'ไทย': 'th', 'indonesian': 'id', 'bahasa indonesia': 'id',
    'malay': 'ms', 'bahasa melayu': 'ms', 'tagalog': 'tl', 'filipino': 'tl',
    'bengali': 'bn', 'বাংলা': 'bn', 'urdu': 'ur', 'اردو': 'ur',
    'tamil': 'ta', 'தமிழ்': 'ta', 'telugu': 'te', 'తెలుగు': 'te',
    # Middle Eastern languages
    'arabic': 'ar', 'العربية': 'ar', 'hebrew': 'he', 'עברית': 'he',
    'farsi': 'fa', 'فارسی': 'fa', 'persian': 'fa', 'turkish': 'tr',
    # African languages
    'swahili': 'sw', 'kiswahili': 'sw', 'afrikaans': 'af', 'zulu': 'zu', 'isizulu': 'zu',
    'amharic': 'am', 'አማርኛ': 'am', 'yoruba': 'yo', 'igbo': 'ig',
    # Other languages
    'esperanto': 'eo', 'latin': 'la', 'maori': 'mi', 'irish': 'ga', 'gaelic': 'gd',
    'icelandic': 'is', 'íslenska': 'is', 'maltese': 'mt', 'malti': 'mt'
}

# Language names for display
LANGUAGE_NAMES = {
    # Main languages
    'en': 'English', 'es': 'Spanish', 'de': 'German', 'hi': 'Hindi', 'fr': 'French',
    # European languages
    'ru': 'Russian', 'it': 'Italian', 'pt': 'Portuguese', 'nl': 'Dutch', 'el': 'Greek',
    'pl': 'Polish', 'tr': 'Turkish', 'cs': 'Czech', 'sk': 'Slovak', 'sv': 'Swedish',
    'no': 'Norwegian', 'da': 'Danish', 'fi': 'Finnish', 'hu': 'Hungarian', 'ro': 'Romanian',
    'bg': 'Bulgarian', 'hr': 'Croatian', 'sq': 'Albanian', 'uk': 'Ukrainian', 'sr': 'Serbian',
    'sl': 'Slovenian', 'et': 'Estonian', 'lv': 'Latvian', 'lt': 'Lithuanian',
    # Asian languages
    'zh': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'vi': 'Vietnamese', 'th': 'Thai',
    'id': 'Indonesian', 'ms': 'Malay', 'tl': 'Tagalog', 'bn': 'Bengali', 'ur': 'Urdu',
    'ta': 'Tamil', 'te': 'Telugu',
    # Middle Eastern languages
    'ar': 'Arabic', 'he': 'Hebrew', 'fa': 'Farsi',
    # African languages
    'sw': 'Swahili', 'af': 'Afrikaans', 'zu': 'Zulu', 'am': 'Amharic', 'yo': 'Yoruba', 'ig': 'Igbo',
    # Other languages
    'eo': 'Esperanto', 'la': 'Latin', 'mi': 'Maori', 'ga': 'Irish', 'gd': 'Gaelic',
    'is': 'Icelandic', 'mt': 'Maltese'
}

class MultiTranslator:
    """Uses multiple translation services for better reliability and fallback options"""
    
    def __init__(self):
        self.libre_base_url = "https://libretranslate.de/"  # Free instance of LibreTranslate
        self.libre_api_key = os.environ.get("LIBRE_API_KEY")
        self.translators = [
            ('MyMemory', MyMemoryTranslator),  # Free with usage limits
            ('Libre', LibreTranslator),        # Free open source translation (needs API key)
            ('Linguee', LingueeTranslator)     # Only for certain language pairs
        ]
        
    def translate(self, text, source_lang, target_lang='en'):
        """Tries multiple translation services until one works"""
        if not text or source_lang == target_lang:
            return text
            
        errors = []
        
        for name, translator_class in self.translators:
            try:
                # Skip Libre if no API key
                if name == 'Libre' and not self.libre_api_key:
                    continue
                
                # Handle specific translator limitations
                if name == 'Linguee' and (source_lang not in ['en', 'de', 'fr', 'es', 'pt'] or 
                                        target_lang not in ['en', 'de', 'fr', 'es', 'pt']):
                    continue
                
                # Initialize the translator with appropriate parameters
                if name == 'Libre':
                    translator = translator_class(source=source_lang, target=target_lang, base_url=self.libre_base_url, api_key=self.libre_api_key)
                else:
                    translator = translator_class(source=source_lang, target=target_lang)
                
                # Check if language is supported by this translator
                supported = []
                try:
                    supported = translator.get_supported_languages(as_dict=True)
                except Exception:
                    pass  # Not all translators implement this
                if supported and (source_lang not in supported.values() or target_lang not in supported.values()):
                    continue
                
                result = translator.translate(text)
                if result:
                    print(f"Translation successful using {name}")
                    return result
            except Exception as e:
                errors.append(f"{name}: {str(e)}")
                continue
                
        print(f"Warning: All translation attempts failed: {errors}")
        return f"(Translation unavailable for this language pair. Try a more common language or check your API key.)"

class MultilanguageBot:
    def __init__(self):
        self.translator = MultiTranslator()
        self.current_lang = 'en'  # Default language
        self.voice_enabled = False
        self.responses = self._load_responses()
        self.user_history = []
        
    def _load_responses(self):
        """Load chatbot responses from file or use default"""
        try:
            # Try to load from file
            if os.path.exists('responses.json'):
                with open('responses.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Could not load responses file: {e}")
            
        # Default responses
        return {
            "greeting": {
                "en": ["Hello!", "Hi there!", "Greetings!", "Welcome!"],
                "es": ["¡Hola!", "¡Saludos!", "¡Bienvenido!"],
                "fr": ["Bonjour!", "Salut!", "Bienvenue!"],
                "de": ["Hallo!", "Guten Tag!", "Willkommen!"],
                "hi": ["नमस्ते!", "हैलो!", "स्वागत है!"],
                "zh": ["你好!", "您好!", "欢迎!"],
                "ja": ["こんにちは!", "やあ!", "ようこそ!"],
                "ru": ["Привет!", "Здравствуйте!", "Добро пожаловать!"]
            },
            "help": {
                "en": ["I can chat in over 50 languages using free translation services!",
                      "• Type in any language and I'll understand.",
                      "• Say 'switch to [language]' to change languages.",
                      "• Say 'languages' to see all supported languages.",
                      "• Say 'voice on/off' to toggle voice feedback.",
                      "• Say 'exit' or 'quit' to end the conversation."],
                "es": ["¡Puedo chatear en más de 50 idiomas utilizando servicios de traducción gratuitos!",
                      "• Escribe en cualquier idioma y te entenderé.",
                      "• Di 'cambiar a [idioma]' para cambiar de idioma.",
                      "• Di 'languages' para ver todos los idiomas disponibles.",
                      "• Di 'voice on/off' para activar/desactivar la voz.",
                      "• Di 'exit' o 'quit' para terminar la conversación."]
            },
            "farewell": {
                "en": ["Goodbye!", "See you later!", "Bye!", "Take care!"],
                "es": ["¡Adiós!", "¡Hasta luego!", "¡Cuídate!"],
                "fr": ["Au revoir!", "À bientôt!", "Prenez soin de vous!"],
                "de": ["Auf Wiedersehen!", "Bis später!", "Tschüss!"],
                "hi": ["अलविदा!", "फिर मिलेंगे!", "अपना ख्याल रखना!"]
            },
            "name": {
                "en": ["I'm MultiLingualBot, your polyglot assistant!"],
                "es": ["Soy MultiLingualBot, ¡tu asistente políglota!"],
                "de": ["Ich bin MultiLingualBot, dein polyglotter Assistent!"],
                "hi": ["मैं मल्टीलिंगुअलबॉट हूं, आपका बहुभाषी सहायक!"]
            },
            "fallback": {
                "en": ["I see!", "Interesting!", "Tell me more.", "Go on.", "I understand."],
                "es": ["¡Ya veo!", "¡Interesante!", "Cuéntame más.", "Continúa.", "Entiendo."],
                "fr": ["Je vois!", "Intéressant!", "Dis m'en plus.", "Continue.", "Je comprends."],
                "de": ["Ich verstehe!", "Interessant!", "Erzähl mir mehr.", "Weiter.", "Ich verstehe."],
                "hi": ["मैं समझता हूँ!", "दिलचस्प!", "मुझे अधिक बताएं।", "जारी रखें।", "मैं समझता हूँ।"]
            }
        }
    
    def _get_response(self, category, lang):
        """Get a random response from a category in the specified language or fall back to English"""
        if category in self.responses and lang in self.responses[category]:
            return random.choice(self.responses[category][lang])
        elif category in self.responses and 'en' in self.responses[category]:
            # Fallback to English if the language isn't available
            english_response = random.choice(self.responses[category]['en'])
            # Try to translate to target language
            try:
                return self.translator.translate(english_response, 'en', lang)
            except:
                return english_response
        return "I'm not sure what to say."
    
    def detect_language(self, text):
        """Detect language of input text"""
        try:
            return detect(text)
        except:
            return None
    
    def speak_text(self, text):
        """Speak the provided text if voice is enabled"""
        if not self.voice_enabled:
            return
            
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Voice error: {e}")
    
    def process_input(self, user_input):
        """Process user input and generate appropriate response"""
        if not user_input.strip():
            return "I didn't catch that. Can you please say something?"
            
        # Store user input in history
        self.user_history.append(user_input)
        
        # Check for special commands
        lc = user_input.lower()
        
        # Check for exit command
        if lc in ['exit', 'quit', 'bye', 'goodbye']:
            return "exit"
            
        # Check for help command
        if lc in ['help', 'commands', 'options']:
            return self._get_response("help", self.current_lang)
            
        # Check for languages list command
        if lc in ['languages', 'list languages', 'show languages', 'language list']:
            return self._format_language_list()
            
        # Check for voice toggle command
        if 'voice on' in lc:
            self.voice_enabled = True
            return "Voice mode activated. I'll speak my responses."
        if 'voice off' in lc:
            self.voice_enabled = False
            return "Voice mode deactivated."
            
        # Check for language switch commands
        for keyword, lang_code in LANGUAGE_CODES.items():
            if keyword in lc or f"switch to {keyword}" in lc or f"change to {keyword}" in lc:
                self.current_lang = lang_code
                response = f"Switching to {LANGUAGE_NAMES.get(lang_code, keyword)}."
                translated = self.translator.translate(response, 'en', lang_code)
                return f"{response}\n{translated}"
        
        # Detect language and set current language if confident
        detected_lang = self.detect_language(user_input)
        if detected_lang and detected_lang != self.current_lang:
            print(f"Detected language: {LANGUAGE_NAMES.get(detected_lang, detected_lang)}")
            self.current_lang = detected_lang
        
        # Translate to English if not already English
        english_translation = None
        if self.current_lang != 'en':
            english_translation = self.translator.translate(user_input, self.current_lang, 'en')
        
        # Generate response
        response = self.generate_response(user_input, english_translation)
        
        return response
    
    def generate_response(self, user_input, english_translation=None):
        """Generate chatbot response based on input"""
        lc = user_input.lower()
        
        # Format response with translation if available
        response_parts = []
        
        # Add English translation if not in English
        if english_translation and self.current_lang != 'en':
            response_parts.append(f"You said (in English): {english_translation}")
        
        # Check for specific intents
        if any(greeting in lc for greeting in ['hello', 'hi ', 'hey', 'greetings', 'hola', 'bonjour', 'namaste']):
            bot_response = self._get_response("greeting", self.current_lang)
        elif any(name in lc for name in ['your name', 'who are you', 'what are you']):
            bot_response = self._get_response("name", self.current_lang)
        elif any(bye in lc for bye in ['bye', 'goodbye', 'exit', 'quit']):
            bot_response = self._get_response("farewell", self.current_lang)
        else:
            bot_response = self._get_response("fallback", self.current_lang)
        
        response_parts.append(f"Bot ({LANGUAGE_NAMES.get(self.current_lang, self.current_lang)}): {bot_response}")
        
        # If response is not in English, add English translation
        if self.current_lang != 'en':
            try:
                eng_translation = self.translator.translate(bot_response, self.current_lang, 'en')
                response_parts.append(f"(In English: {eng_translation})")
            except Exception as e:
                response_parts.append(f"(Translation error: {str(e)})")
        
        # Speak the response in the target language
        threading.Thread(target=self.speak_text, args=(bot_response,)).start()
        
        return "\n".join(response_parts)
    
    def _format_language_list(self):
        """Format and return a list of available languages"""
        languages = {}
        for name, code in sorted(LANGUAGE_NAMES.items(), key=lambda x: x[1]):
            first_letter = code[0].upper()
            if first_letter not in languages:
                languages[first_letter] = []
            languages[first_letter].append(f"{LANGUAGE_NAMES[name]} ({name})")
        
        parts = ["Available Languages:"]
        for letter in sorted(languages.keys()):
            parts.append(f"\n{letter}: {', '.join(sorted(languages[letter]))}")
        
        response = "\n".join(parts)
        
        # If not in English, also provide a translation of the heading
        if self.current_lang != 'en':
            try:
                heading = "Available Languages:"
                translated_heading = self.translator.translate(heading, 'en', self.current_lang)
                response = response.replace(heading, f"{translated_heading} ({heading})")
            except:
                pass
                
        return response

def print_colorized(text, color_code):
    """Print text with ANSI color codes"""
    print(f"\033[{color_code}m{text}\033[0m")

def main():
    print_colorized("="*60, '36')
    print_colorized("     🌎 ADVANCED MULTILINGUAL CHATBOT 🌎", '32;1')
    print_colorized("="*60, '36')
    print_colorized("• Type in ANY of 50+ languages and I'll understand", '33')
    print_colorized("• Using FREE open-source translation services", '33') 
    print_colorized("• Say 'switch to Spanish' (or any language) to change my language", '33')
    print_colorized("• Say 'voice on' to enable speech (if available)", '33')
    print_colorized("• Type 'help' for commands or 'exit' to quit", '33')
    print_colorized("="*60, '36')
    
    bot = MultilanguageBot()
    
    while True:
        try:
            user_input = input("\nYou: ")
            
            # Show "typing" animation
            print("Bot is typing", end="")
            for _ in range(3):
                time.sleep(0.3)
                print(".", end="", flush=True)
            print()
            
            response = bot.process_input(user_input)
            
            if response == "exit":
                print_colorized("\nBot: Goodbye! Have a great day!", '32')
                break
                
            print_colorized(response, '32')
            
        except KeyboardInterrupt:
            print_colorized("\nExiting chatbot. Goodbye!", '31')
            break
        except Exception as e:
            print_colorized(f"\nAn error occurred: {str(e)}", '31')
            print("Let's continue our conversation.")

if __name__ == "__main__":
    main()

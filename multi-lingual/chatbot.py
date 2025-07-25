# chatbot.py
from detectors import detect_language
from deep_translator import MyMemoryTranslator
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def translate_to_english(text, src_lang):
    try:
        return MyMemoryTranslator(source=src_lang, target='en').translate(text)
    except Exception:
        return "(Translation unavailable)"

def generate_response(text, detected_lang):
    """Generate a chatbot response based on the input text."""
    # This is a simple echo response - you can make this more sophisticated
    # by integrating with an actual chatbot/LLM API
    if "hello" in text.lower() or "hi" in text.lower():
        return {
            'en': "Hello! How can I help you today?",
            'es': "¡Hola! ¿En qué puedo ayudarte?",
            'de': "Hallo! Wie kann ich dir helfen?",
            'hi': "नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ?"
        }.get(detected_lang, "Hello! How can I help?")
    elif "name" in text.lower():
        return {
            'en': "I'm MultiLingualBot, your polyglot assistant!",
            'es': "Soy MultiLingualBot, ¡tu asistente políglota!",
            'de': "Ich bin MultiLingualBot, dein polyglotter Assistent!",
            'hi': "मैं मल्टीलिंगुअलबॉट हूं, आपका बहुभाषी सहायक!"
        }.get(detected_lang, "I'm MultiLingualBot, your polyglot assistant!")
    elif "bye" in text.lower() or "goodbye" in text.lower():
        return {
            'en': "Goodbye! Have a great day!",
            'es': "¡Adiós! ¡Que tengas un buen día!",
            'de': "Auf Wiedersehen! Einen schönen Tag noch!",
            'hi': "अलविदा! आपका दिन शुभ हो!"
        }.get(detected_lang, "Goodbye! Have a great day!")
    else:
        return {
            'en': "I see! Tell me more.",
            'es': "¡Ya veo! Cuéntame más.",
            'de': "Ich verstehe! Erzähl mir mehr.",
            'hi': "मैं समझता हूं! मुझे और बताओ।"
        }.get(detected_lang, "I see! Tell me more.")

def main():
    print("===== Multilingual Chatbot =====")
    print("Type in ANY language and I will respond!")
    print("(Type 'exit' to quit)")
    print("================================")
    
    current_lang = 'en'  # default language
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nChatbot: Goodbye! Thanks for chatting!")
                break
                
            # Detect language
            detected_lang = detect_language(user_input) or current_lang
            
            # Check for language switch commands
            lc = user_input.lower()
            lang_switch = {
                'english': 'en', 'inglés': 'en', 'spanish': 'es',
                'español': 'es', 'deutsch': 'de', 'alemán': 'de',
                'hindi': 'hi', 'हिंदी': 'hi', 'french': 'fr',
                'français': 'fr', 'russian': 'ru', 'русский': 'ru',
                'chinese': 'zh', '中文': 'zh', 'japanese': 'ja',
                '日本語': 'ja', 'arabic': 'ar', 'العربية': 'ar',
                'portuguese': 'pt', 'português': 'pt', 'italian': 'it',
                'italiano': 'it', 'korean': 'ko', '한국어': 'ko',
                'turkish': 'tr', 'türkçe': 'tr'
            }
            
            for k, code in lang_switch.items():
                if k in lc:
                    detected_lang = code
                    current_lang = code
                    print(f"\nChatbot: Switching to {k.title()} mode.")
                    break
            
            # Translate to English if not already English
            if detected_lang != 'en':
                translation = translate_to_english(user_input, detected_lang)
                print(f"Translation: {translation}")
            
            # Generate response
            response = generate_response(user_input, detected_lang)
            
            # Show response
            print(f"Chatbot: {response}")
            
        except Exception as e:
            print(f"Sorry, I encountered an error: {str(e)}")

if __name__ == "__main__":
    main()

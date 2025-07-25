# Multilingual Chatbot

A free, open-source multilingual chatbot that can understand and respond in 50+ languages using only free translation services.

## Features

- **Multiple Language Support**: Communicate in 50+ languages
- **Free and Open Source**: Uses only free translation APIs (MyMemory, LibreTranslate, and Linguee)
- **Language Detection**: Automatically detects the language you're typing in
- **Language Switching**: Change the bot's language anytime with a simple command
- **Voice Output**: Optional text-to-speech functionality
- **Terminal-Based**: Runs locally in your terminal with a colorful interface

## Required Packages

```bash
pip install deep-translator langdetect pyttsx3
```

## Running the Chatbot

You can run either the simple or enhanced version of the chatbot:

### Simple Version

```bash
python chatbot.py
```

### Enhanced Version (Recommended)

```bash
python enhanced_chatbot.py
```

## Usage Instructions

- **Type in any language**: The chatbot will automatically detect and respond in the same language
- **Commands**:
  - `help` - Show available commands
  - `languages` - Show a list of all supported languages
  - `switch to [language]` - Change the bot's language (e.g., "switch to Spanish")
  - `voice on` or `voice off` - Enable or disable text-to-speech
  - `exit` or `quit` - End the conversation

## Translation Services Used

The chatbot implements a fallback mechanism that attempts to use several free translation services:

1. **MyMemoryTranslator** - Free with usage limits (up to 5000 chars/day)
2. **LibreTranslate** - Free and open-source machine translation API
3. **LingueeTranslator** - Dictionary-based translator for specific language pairs

## Notes

- The chatbot works best with shorter phrases and common languages
- LibreTranslate may sometimes be slow or unavailable depending on the free server load
- Some rare languages may not be supported by all translation services

## Example Conversation

```
Bot: Hello! How can I help you today?

You: Bonjour, comment ça va?
Translation: Hello, how are you?
Bot (French): Je vais bien, merci! Comment puis-je vous aider aujourd'hui?
(In English: I'm fine, thanks! How can I help you today?)

You: switch to Japanese
Bot: Switching to Japanese.
日本語に切り替えます。

You: What time is it?
Bot (Japanese): 何時ですか？
(In English: What time is it?)
```

## Troubleshooting

If you encounter translation errors:

1. Try shorter phrases
2. Check your internet connection
3. Wait and try again (rate limits may apply)
4. Try a more common language

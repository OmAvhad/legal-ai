from googletrans import Translator
from time import sleep

# Define a dictionary for language titles
language_titles = {
    'hi': 'Hindi',
    'mr': 'Marathi',
    'sd': 'Sindhi',
}

# Initialize the translator
translator = Translator()

def translate_text(text, languages):
    """Translate the given text into the selected languages."""
    translations = {}
    for lang in languages:
        try:
            translated = translator.translate(text, dest=lang)
            translations[lang] = translated.text
        except Exception as e:
            translations[lang] = f"Error: {str(e)}"
        # Add delay to prevent Google blocking requests
        sleep(1)
    return translations

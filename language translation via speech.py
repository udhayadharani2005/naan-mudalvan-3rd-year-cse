import speech_recognition as sr
from googletrans import Translator

class SpeechTranslator:
    def _init_(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.translator = Translator()
        
        # Language mapping with full names
        self.languages = {
            'english': 'en',
            'spanish': 'es',
            'french': 'fr',
            'german': 'de',
            'hindi': 'hi',
            'tamil': 'ta',
            'japanese': 'ja',
            'russian': 'ru',
            'chinese': 'zh-CN'
        }
        
        self.source_lang = 'en'
        self.target_lang = 'ta'  # Default to Tamil
    
    def get_language_code(self, language_name):
        """Convert full language name to code"""
        return self.languages.get(language_name.lower(), 'en')
    
    def set_languages(self):
        """Set source and target languages using full names"""
        print("\nAvailable languages:")
        for lang in self.languages:
            print(f"- {lang.capitalize()}")
        
        while True:
            source = input("\nEnter source language (e.g. 'English'): ").strip().lower()
            if source in self.languages:
                self.source_lang = self.languages[source]
                break
            print("Invalid language. Please try again.")
        
        while True:
            target = input("Enter target language (e.g. 'Tamil'): ").strip().lower()
            if target in self.languages:
                self.target_lang = self.languages[target]
                break
            print("Invalid language. Please try again.")
    
    def listen(self):
        """Capture speech and convert to text"""
        with self.microphone as source:
            print(f"\nSpeak in {self.source_lang} (say 'exit' to quit)...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language=self.source_lang)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError:
                print("Could not request results; check internet")
            except sr.WaitTimeoutError:
                print("Listening timed out")
            return None
    
    def translate_text(self, text):
        """Translate text to target language"""
        if not text:
            return None
            
        try:
            translation = self.translator.translate(text, src=self.source_lang, dest=self.target_lang)
            print(f"\nTranslation: {translation.text}")
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    def run(self):
        print("=== Speech Translation System ===")
        print("Speak in one language, get translation in another\n")
        self.set_languages()
        
        while True:
            text = self.listen()
            if not text:
                continue
                
            if text.lower() in ['exit', 'quit', 'stop']:
                print("Goodbye!")
                break
                
            self.translate_text(text)

if _name_ == "_main_":
    try:
        translator = SpeechTranslator()
        translator.run()
    except KeyboardInterrupt:
        print("\nTranslation stopped")
    except Exception as e:
        print(f"Error: {e}")

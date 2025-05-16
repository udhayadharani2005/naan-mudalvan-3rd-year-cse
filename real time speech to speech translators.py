import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import time
import queue
import subprocess
from threading import Event

class SentenceTranslator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.translator = Translator()
        self.stop_event = Event()
        
        # Enhanced language support
        self.languages = {
            'english': 'en',
            'spanish': 'es',
            'french': 'fr',
            'german': 'de',
            'hindi': 'hi',
            'tamil': 'ta',
            'japanese': 'ja',
            'chinese': 'zh-cn',
            'korean': 'ko',
            'russian': 'ru'
        }
        
        # Audio configuration
        self.pause_threshold = 1.2  # Seconds of silence to consider sentence complete
        self.energy_threshold = 300  # Microphone sensitivity
        self.dynamic_energy_threshold = True

    def configure_microphone(self):
        """Set up microphone with optimal settings"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        self.recognizer.pause_threshold = self.pause_threshold
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold

    def select_languages(self):
        """Interactive language selection"""
        print("\nAvailable languages:")
        for i, lang in enumerate(self.languages.keys(), 1):
            print(f"{i}. {lang.capitalize()}")
        
        while True:
            try:
                src_num = int(input("\nSelect YOUR language number: ")) - 1
                self.source_lang = list(self.languages.values())[src_num]
                break
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")
        
        while True:
            try:
                tgt_num = int(input("Select TARGET language number: ")) - 1
                self.target_lang = list(self.languages.values())[tgt_num]
                break
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")

    def speak_translation(self, text):
        """Convert translated text to natural speech"""
        tts = gTTS(text=text, lang=self.target_lang, slow=False)
        tts.save("translation.mp3")
        
        # Hidden audio playback
        subprocess.run(
            ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', 'translation.mp3'],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        os.remove("translation.mp3")

    def process_sentence(self, audio):
        """Convert audio to text and translate complete sentences"""
        try:
            text = self.recognizer.recognize_google(audio, language=self.source_lang)
            print(f"\n[{self.source_lang.upper()}]: {text}")
            
            if 'exit' in text.lower():
                self.stop_event.set()
                return
            
            translation = self.translator.translate(text, src=self.source_lang, dest=self.target_lang)
            print(f"[{self.target_lang.upper()}]: {translation.text}")
            
            self.speak_translation(translation.text)
            
        except sr.UnknownValueError:
            print("(Listening...)")
        except sr.RequestError:
            print("(Network error - check internet connection)")
        except Exception as e:
            print(f"(Error: {str(e)})")

    def run(self):
        """Continuous sentence-by-sentence translation"""
        self.configure_microphone()
        self.select_languages()
        
        print("\nSpeak naturally (say 'exit' to quit)...\n")
        
        with self.microphone as source:
            while not self.stop_event.is_set():
                try:
                    audio = self.recognizer.listen(
                        source,
                        phrase_time_limit=10,
                        timeout=None
                    )
                    self.process_sentence(audio)
                except KeyboardInterrupt:
                    self.stop_event.set()
        
        print("\nTranslation session ended")

if __name__ == "__main__":
    # Required: pip install SpeechRecognition googletrans gTTS ffmpeg-python
    
    translator = SentenceTranslator()
    translator.run()

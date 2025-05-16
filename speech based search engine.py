import speech_recognition as sr
from googlesearch import search
import webbrowser
import time

class SpeechSearchEngine:
    def _init_(self):
        self.recognizer = sr.Recognizer()
        self.setup_microphone()
        
    def setup_microphone(self):
        """Handle microphone setup with better error handling"""
        print("Initializing microphone...")
        try:
            self.microphone = sr.Microphone()
            # Test microphone access
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone ready!")
        except Exception as e:
            print(f"Microphone error: {e}")
            print("Try these solutions:")
            print("1. Make sure your microphone is connected")
            print("2. Check microphone permissions in Windows Settings")
            print("3. Try a different microphone")
            exit(1)
    
    def listen(self):
        """Improved voice listening with better feedback"""
        with self.microphone as source:
            print("\nSpeak now (say 'exit' to quit)...")
            try:
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                print("Processing your voice...")
                query = self.recognizer.recognize_google(audio).lower().strip()
                print(f"You said: {query}")
                return query
            except sr.WaitTimeoutError:
                print("I didn't hear anything. Try speaking louder.")
                return None
            except sr.UnknownValueError:
                print("I couldn't understand that. Please try again.")
                return None
            except sr.RequestError:
                print("Internet connection required for speech recognition.")
                return None
            except Exception as e:
                print(f"Unexpected error: {e}")
                return None
    
    def open_website(self, url):
        """Open URL in default browser"""
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        print(f"Opening: {url}")
        webbrowser.open(url)
    
    def is_website(self, query):
        """Improved website detection"""
        common_domains = ('.com', '.org', '.net', '.in', '.co')
        return any(domain in query for domain in common_domains)
    
    def run(self):
        print("=== Voice Website Opener ===")
        print("Say a website name (like 'google.com') or search query")
        
        while True:
            query = self.listen()
            if not query:
                continue
                
            if query in ['exit', 'quit', 'close']:
                print("Closing program...")
                break
                
            if self.is_website(query):
                self.open_website(query)
            else:
                print(f"Searching for: {query}")
                try:
                    first_result = next(search(query, num_results=1))
                    self.open_website(first_result)
                except Exception as e:
                    print(f"Search failed: {e}")

if _name_ == "_main_":
    try:
        engine = SpeechSearchEngine()
        engine.run()
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")

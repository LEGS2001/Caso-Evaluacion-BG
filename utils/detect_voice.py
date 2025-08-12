import speech_recognition as sr
import pyttsx3

def detect_voice():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone(device_index=1) as mic:
                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                
                text = r.recognize_google(audio, language="es-EC")
                text = text.lower()
                
                print(f"Texto: {text}")
                return text
        
        except sr.UnknownValueError:
            print("No se entendió el audio, intenta de nuevo.")

            r = sr.Recognizer()
            continue
        
def generate_audio(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)  
    
    engine.setProperty('rate', 300)

    engine.say(texto)
    engine.runAndWait()
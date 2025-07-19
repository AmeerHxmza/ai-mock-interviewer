

import pyttsx3
import os
import tempfile

def speak(text, filename="question.wav"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    filepath = os.path.join(tempfile.gettempdir(), filename)
    engine.save_to_file(text, filepath)
    engine.runAndWait()
    return filepath

# from elevenlabs import set_api_key, generate
# from elevenlabs import generate, save

# set_api_key(os.getenv("ELEVEN_API_KEY"))

# def speak(text, filename="question.wav"):
#     audio = generate(text=text, voice="Aria")
#     save(audio, filename)
#     return filename


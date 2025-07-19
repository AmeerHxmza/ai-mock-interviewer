

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

# import os
# import tempfile
# from elevenlabs import generate, save, set_api_key
# from utils.config import ELEVEN_API_KEY




# print("✅ ElevenLabs works correctly!")

# set_api_key(ELEVEN_API_KEY)

# def speak(text, filename="question.wav", voice="Aria"):  # You can change the voice name if needed
#     audio = generate(
#         text=text,
#         voice=voice,
#         model="eleven_monolingual_v1"  # or "eleven_multilingual_v2"
#     )
    
#     filepath = os.path.join(tempfile.gettempdir(), filename)
#     save(audio, filepath)
#     return filepath

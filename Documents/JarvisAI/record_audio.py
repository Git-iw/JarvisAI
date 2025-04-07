# import sounddevice as sd
# import numpy as np
# import scipy.io.wavfile as wav
#
# def record_audio(duration=5, filename="voice_input.wav"):
#     fs = 44100
#     print("Listening....")
#     audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
#     sd.wait()
#     wav.write(filename, fs, audio)
#     print("Audio Recording Done")
#     return filename
# import sounddevice as sd
# import numpy as np
# import whisper
# import tempfile
# import scipy.io.wavfile as wav
#
# # Load the Whisper model
# model = whisper.load_model("base")  # You can also use "small" or "medium" for better accuracy
#
# def record_audio(duration=5):
#     fs = 44100  # Sample rate
#     print("🎙️ Listening...")
#     audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
#     sd.wait()
#     print("✅ Recording Done")
#
#     # Save temporarily for Whisper
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
#         wav.write(temp_file.name, fs, audio)
#         return temp_file.name
#
# def transcribe_audio(file_path):
#     print("🧠 Transcribing...")
#     result = model.transcribe(file_path)
#     print("📝 Text:", result["text"])
#     return result["text"]
import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile as wav
import speech_recognition as sr
import os

# Load the best Whisper model
model = whisper.load_model("large")  # large-v3 is the most accurate for multilingual

def record_audio(duration=5):
    fs = 44100  # Sample rate
    print("🎙️ Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("✅ Recording Done")

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wav.write(temp_file.name, fs, audio)
        return temp_file.name

def transcribe_audio(file_path):
    print("🧠 Transcribing with Whisper...")
    try:
        result = model.transcribe(file_path, language="te")  # Force Telugu
        text = result["text"].strip()
        if text:
            print("📝 Whisper Transcription:", text)
            return text
    except Exception as e:
        print("⚠️ Whisper failed:", e)






import queue
import sounddevice as sd
import json
from record_audio import record_audio
from transcribe import transcribe_audio
from gemini_bot import gemini_prompt
from spotify import play_song
from spotify import extract_song_query
from vosk import Model, KaldiRecognizer
import os
import pyttsx3
import webbrowser

engine = pyttsx3.init()

if not os.path.exists("vosk-model"):
    print("Please download a Vosk model and place it in a folder named 'model'")
    exit(1)

model = Model("vosk-model")
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

WAKE_WORD = "jarvis"

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

def detect_wake_word():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🟢 Say the wake word to activate...")
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()
                if WAKE_WORD in text:
                    print("✨ Wake word detected!")
                    return

def main():
    detect_wake_word()  # Only happens once at startup
    print("✨ Wake word detected! Jarvis is now active.")

    while True:
        print("🎙️ JARVIS AI Listening...")
        audio_file = record_audio()
        if audio_file is None:
            detect_wake_word()
            continue

        text_prompt = transcribe_audio(audio_file)
        # if not text_prompt.strip():
        #     print("⚠️ Silence detected. Please speak again.")
        #     continue  # Skip this cycle if the input is empty

        print(f"User: {text_prompt}")

        if "quit".lower() in text_prompt.lower():
            print("Goodbye Sir")
            engine.say("Goodbye Sir")
            engine.runAndWait()
            break

        if "open youtube".lower() in text_prompt.lower():
            webbrowser.open("https://youtube.com")
            continue

        if "play the song".lower() in text_prompt.lower():
            song = text_prompt.replace("play the song", "").strip()
            query = extract_song_query(song)
            play_song(query)
            detect_wake_word()


        response = gemini_prompt(text_prompt)

        if not response.strip():
            print("⚠️ Gemini returned an empty response.")
            continue

        print(f"Jarvis: {response}")
        engine.say(response)
        engine.runAndWait()


if __name__ == "__main__":
    main()
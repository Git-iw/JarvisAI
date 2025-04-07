from record_audio import record_audio
from transcribe import transcribe_audio
from gemini_bot import gemini_prompt
import pyttsx3
import webbrowser

engine = pyttsx3.init()

def main():
    while True:
        print("JARVIS AI")
        audio_file = record_audio()
        text_prompt = transcribe_audio(audio_file)
        print(f"User: {text_prompt}")

        if "quit".lower() in text_prompt.lower():
            print("Goodbye Sir")
            engine.say("Goodbye Sir")
            engine.runAndWait()
            break
        if "open youtube".lower() in text_prompt.lower():
            webbrowser.open("https://youtube.com")

        response = gemini_prompt(text_prompt)
        print(f"Jarvis: {response}")
        engine.say(response)
        engine.runAndWait()


if __name__ == "__main__":
    main()
import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile as wav


# Load the best Whisper model
model = whisper.load_model("large")  # large-v3 is the most accurate for multilingual

def record_audio(duration=5, threshold=15):
    fs = 44100  # Sample rate
    print("🎙️ Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # Calculate RMS energy to check if there's actual speech
    rms = np.sqrt(np.mean(audio ** 2))
    print(f"RMS: {rms}")
    if rms < threshold:  # You can tweak this threshold
        print("🤫 Detected silence or low noise. Please speak louder.")
        return None

    print("✅ Recording Done")

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wav.write(temp_file.name, fs, audio)
        return temp_file.name


def transcribe_audio(file_path):
    print("🧠 Transcribing with Whisper...")
    try:
        result = model.transcribe(file_path, language="en")  # Force Telugu
        text = result["text"].strip()
        if text:
            print("📝 Whisper Transcription:", text)
            return text
    except Exception as e:
        print("⚠️ Whisper failed:", e)





import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play

API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

client = ElevenLabs(
    api_key= API_KEY
)

def speak(prompt):
    audio = client.generate(
        text=prompt,
        voice="bHMGij7OhWM9CNyCNeSn",
        model="eleven_turbo_v2"
    )
    play(audio)

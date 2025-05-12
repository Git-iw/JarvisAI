import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env

genai.configure(api_key=os.getenv("AIzaSyBXU3td0VltM_9ykGQrqjHpbCvdnbP17kw"))

model = genai.GenerativeModel("gemini-2.0-flash")  # Or "gemini-1.5-pro" for more accuracy

def clean_response_text(text):
    # Remove markdown formatting characters
    chars_to_remove = ['*', '_', '`', '~', '#']
    for char in chars_to_remove:
        text = text.replace(char, '')
    return text

def gemini_prompt(prompt):
    try:
        response = model.generate_content(prompt)
        clean_text = clean_response_text(response.text)
        return clean_text
    except Exception as e:
        return f"Error: {e}"

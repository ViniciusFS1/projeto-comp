# projeto-comp


python -m pip install -q -U google-genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.




from google import genai
from google.genai import types
import pandas as pd

def processer(path):
    client = genai.Client()
    df = pd.read_csv(path)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",

    for title in df:
        config=types.GenerateContentConfig(
            system_instruction="You are a cat. Your name is Neko."),
        contents="Hello there"
        

print(response.text)

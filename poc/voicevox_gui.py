import asyncio
import base64
import requests
import streamlit as st
from voicevox import Client


# Function to generate audio using Voicevox
async def generate_audio(text: str, speaker: int = 4):
    async with Client(base_url="http://localhost:50021") as client:
        audio_query = await client.create_audio_query(text, speaker=speaker)
        with open("voice.wav", "wb") as f:
            f.write(await audio_query.synthesis(speaker=speaker))


# Function to autoplay audio in Streamlit
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
                md,
                unsafe_allow_html=True,
        )


# Function to translate text using Google Translate API
def translate(text: str, source_lang: str = "auto",
        target_lang: str = "en") -> str:
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={text}"
    response = requests.get(url)
    response.raise_for_status()
    json_response = response.json()
    translated_text = ''.join([item[0] for item in json_response[0]])
    return translated_text


st.set_page_config(page_title="VOICEVOX", layout="centered")

st.title("VOICEVOX")

text_input = st.text_area("Enter text:")

if st.button("Submit"):
    if text_input:
        try:
            translated_text = translate(text_input)
            st.write(f"**Translation:** {translated_text}")
            asyncio.run(generate_audio(text_input))
            autoplay_audio("voice.wav")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text.")

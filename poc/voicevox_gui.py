import asyncio
import base64
import json
import requests
import streamlit as st
from voicevox import Client
import nest_asyncio

from mecab_demo_2 import get_html

# Apply the nest_asyncio patch
nest_asyncio.apply()

st.set_page_config(page_title="VOICEVOX", layout="centered")

st.title("VOICEVOX")

# Load JSON data from file
with open('voices.json', 'r') as file:
    names = json.load(file)

# Create a list of formatted name strings for the select box
options = [f"{item['japanese']} - {item['english']}" for item in names]

# Create a select box widget
selected_name = st.selectbox('Choose a speaker:', options)
selected_index = options.index(selected_name)
selected_uuid = names[selected_index]['uuid']


@st.cache_data
def fetch_speaker_info_sync(uuid):
    async def fetch_speaker_info(uuid):
        async with Client(base_url="http://localhost:50021") as client:
            voice_info = await client.fetch_speaker_info(uuid)
            return voice_info.portrait

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_speaker_info(uuid))


# Function to generate audio using Voicevox
async def generate_audio(text: str, speaker: int):
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


text_input = st.text_area("Enter text:")

if st.button("Submit"):
    if text_input:
        try:
            furigana_text = get_html(text_input)
            st.write(f"**Furigana:** {furigana_text}", unsafe_allow_html=True)
            translated_text = translate(text_input)
            st.write(f"**Translation:** {translated_text}")
            asyncio.run(generate_audio(text_input, speaker=selected_index))
            autoplay_audio("voice.wav")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text.")

# Fetch and display the avatar image
try:
    loop = asyncio.get_event_loop()
    avatar_base64 = fetch_speaker_info_sync(selected_uuid)
    avatar_image = base64.b64decode(avatar_base64)
    st.image(avatar_image, caption=selected_name)
except Exception as e:
    st.error(f"Failed to fetch speaker avatar: {e}")

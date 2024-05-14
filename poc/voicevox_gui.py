import asyncio
import base64
import hmac
import json
import requests
import streamlit as st
from streamlit_cookies_controller import CookieController
from voicevox import Client
import nest_asyncio

from mecab_demo_2 import get_html

nest_asyncio.apply()

st.set_page_config(page_title="Reader", layout="centered")

controller = CookieController()

st.title("Reader")


# Function to check the password
def check_password():
    """Returns `True` if the user has the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"],
                               st.secrets["password"]):
            st.session_state["password_correct"] = True
            controller.set('auth_cookie',
                           st.secrets["password"])  # Set the cookie
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Check if the auth cookie exists and is correct
    stored_password = controller.get('auth_cookie')
    if stored_password and hmac.compare_digest(st.secrets["password"],
                                               stored_password):
        st.session_state["password_correct"] = True

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # If no valid cookie, show input for password.
    if stored_password is None or not hmac.compare_digest(
            st.secrets["password"], stored_password):
        st.text_input("Password", type="password", on_change=password_entered,
                      key="password")
        if "password_correct" in st.session_state and not st.session_state[
            "password_correct"]:
            st.error("😕 Password incorrect")
        return False
    return True


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Load JSON data from file
with open('voices.json', 'r') as file:
    names = json.load(file)

# Create a list of formatted name strings for the select box
options = [f"{item['japanese']} - {item['english']}" for item in names]

# Check if the voice index cookie exists and is valid
stored_voice_index = controller.get('voice_index')
if stored_voice_index is None or int(stored_voice_index) >= len(options) or int(
        stored_voice_index) < 0:
    selected_index = 0
    controller.set('voice_index', '0')
else:
    selected_index = int(stored_voice_index)

selected_name = options[selected_index]

# Create a select box widget
selected_name = st.selectbox('Choose a speaker:', options, index=selected_index)
new_selected_index = options.index(selected_name)

# Update the cookie if the selection changes
if new_selected_index != selected_index:
    controller.set('voice_index', str(new_selected_index))

selected_uuid = names[new_selected_index]['uuid']


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

            # Run the async function to generate audio and wait for it to complete
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                    generate_audio(text_input, speaker=selected_index))

            # Play the audio after it's generated
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

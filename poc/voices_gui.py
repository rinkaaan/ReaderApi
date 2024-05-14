import streamlit as st
import asyncio
import nest_asyncio
from voicevox import Client
import json
import base64

# Apply the nest_asyncio patch
nest_asyncio.apply()


@st.cache_data
def fetch_speaker_info_sync(uuid):
    async def fetch_speaker_info(uuid):
        async with Client(base_url="http://localhost:50021") as client:
            voice_info = await client.fetch_speaker_info(uuid)
            return voice_info.portrait

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_speaker_info(uuid))


def main():
    st.title("Voicevox Streamlit App")

    # Load JSON data from file
    with open('voices.json', 'r') as file:
        voices = json.load(file)

    # Create a list of formatted name strings for the select box
    options = [f"{item['japanese']} - {item['english']}" for item in voices]

    # Create a select box widget
    selected_name = st.selectbox('Choose a name:', options)
    selected_index = options.index(selected_name)

    # Display the selected name
    st.write('You selected:', selected_name)

    # Fetch speaker info using the cached synchronous function
    uuid = voices[selected_index]['uuid']
    image_base64 = fetch_speaker_info_sync(uuid)

    # Decode base64 encoded image and display it
    image_data = base64.b64decode(image_base64)
    st.image(image_data, caption=selected_name)


if __name__ == "__main__":
    main()

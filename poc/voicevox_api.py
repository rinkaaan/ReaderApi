import asyncio

from voicevox import Client


async def main():
    async with Client(base_url="http://localhost:50021") as client:
        # audio_query = await client.create_audio_query(
        #     "更に言えば、システムで自動で出来ることが増えていっていませんか？", speaker=4
        # )
        # with open("voice.wav", "wb") as f:
        #     f.write(await audio_query.synthesis(speaker=4))

        voices = await client.fetch_speakers()
        for voice in voices:
            print(voice.name, voice.uuid)

        # base64 encoded image
        # voice_info = await client.fetch_speaker_info(voices[0].uuid)
        # print(voice_info.portrait)


if __name__ == "__main__":
    ## already in asyncio (in a Jupyter notebook, for example)
    # await main()
    ## otherwise
    asyncio.run(main())

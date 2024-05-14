import asyncio

from voicevox import Client


async def main():
    async with Client(base_url="http://localhost:50021") as client:
        audio_query = await client.create_audio_query(
            "更に言えば、システムで自動で出来ることが増えていっていませんか？そんなに公務員って必要ですか？そこの為に働かされて徴収されているとしか感じないです 全てAIで出来るとも思いませんが、必要最小限にしませんか？", speaker=4
        )
        with open("voice.wav", "wb") as f:
            f.write(await audio_query.synthesis(speaker=4))


if __name__ == "__main__":
    ## already in asyncio (in a Jupyter notebook, for example)
    # await main()
    ## otherwise
    asyncio.run(main())

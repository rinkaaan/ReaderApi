import os

from dotenv import load_dotenv

from api.resources.media_utils import download_metadata

cookies_path = "/Users/nguylinc/Downloads/cookies.txt"
load_dotenv()


def test_twitter_multiple_videos():
    media_url = os.getenv("TWITTER_MULTIPLE_VIDEOS")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_twitter_single_video():
    media_url = os.getenv("TWITTER_SINGLE_VIDEO")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_youtube_video():
    media_url = os.getenv("YOUTUBE_VIDEO")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_youtube_video_in_playlist():
    media_url = os.getenv("YOUTUBE_VIDEO_IN_PLAYLIST")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_insta_video():
    media_url = os.getenv("INSTA_VIDEO")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_twitter_multiple_photos():
    media_url = os.getenv("TWITTER_MULTIPLE_PHOTOS")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_twitter_single_photo():
    media_url = os.getenv("TWITTER_SINGLE_PHOTO")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_insta_photo():
    media_url = os.getenv("INSTA_PHOTO")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_insta_photos():
    media_url = os.getenv("INSTA_PHOTOS")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)


def test_instagram_photo_and_video():
    media_url = os.getenv("INSTAGRAM_PHOTO_AND_VIDEO")
    metadata = download_metadata(cookies_path, media_url)
    print(metadata)

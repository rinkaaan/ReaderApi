from models.base import ReaderModel, AlbumModel
from sql_scripts.clients import session


def get_file_path(url):
    if "nguylinc-photos-test" in url:
        return url.split("nguylinc-photos-test/")[1]
    return url


class Test:
    def test_add_ksuid(self):
        # medias = session.query(ReaderModel).all()
        #
        # for media in medias:
        #     media: ReaderModel = session.query(ReaderModel).filter(ReaderModel.id == media.id).first()
        #     media.thumbnail_path = get_file_path(media.thumbnail_path)
        #
        # session.commit()

        albums = session.query(AlbumModel).all()

        for album in albums:
            album: AlbumModel = session.query(AlbumModel).filter(AlbumModel.id == album.id).first()
            new_path = get_file_path(album.thumbnail_path)
            album.thumbnail_path = new_path

        session.commit()

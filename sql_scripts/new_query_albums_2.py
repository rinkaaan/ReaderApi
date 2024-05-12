import logging

from sqlalchemy import desc

from models.base import ReaderModel, AlbumModel
from sql_scripts.clients import session


class Test:
    def test(self):
        logging.disable(logging.WARNING)
        q = session.query(AlbumModel)
        q = q.order_by(desc(AlbumModel.id))
        # q = q.limit(10)
        albums = q.all()

        for album in albums:
            sorted_medias = sorted(album.media, key=lambda media: media.created_at, reverse=True)
            if sorted_medias:
                newest_media: ReaderModel = sorted_medias[0]
                print(newest_media.thumbnail_path)
                album.thumbnail_src_url = sorted_medias[0].thumbnail_src_url
            else:
                print(f"No media in {album.name}")
                session.delete(album)

        session.commit()


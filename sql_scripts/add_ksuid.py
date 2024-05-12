from ksuid import Ksuid

from api.app import session
from models.base import ReaderModel


class Test:
    def test_add_ksuid(self):
        medias = session.query(ReaderModel).all()

        for media in medias:
            media.created_at_ksuid = str(Ksuid(media.created_at))
            # media = session.query(ReaderModel).filter(ReaderModel.id == media.id).first()
            # media.created_at_ksuid = Ksuid(media.created_at)

        session.commit()

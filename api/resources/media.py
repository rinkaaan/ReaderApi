import threading

from apiflask import APIBlueprint, Schema, HTTPError
from apiflask.fields import String, List, Integer, Boolean, Nested
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from api.resources.media_utils import download_metadata, upload_thumbnail, create_albums_if_not_exists, download_medias_helper
from api.resources.utils import date_to_ksuid
from api.schemas.main import ReaderSchema
from models.base import ReaderModel, AlbumModel

media_bp = APIBlueprint("Reader", __name__, url_prefix="/media")


class AddReaderIn(Schema):
    media_url = String()


@media_bp.post("/")
@media_bp.input(AddReaderIn, arg_name="params")
@media_bp.output({})
def add_media(params):
    from api.app import session, COOKIES_PATH

    medias = download_metadata(COOKIES_PATH, params["media_url"])
    for raw_media in medias:
        upload_thumbnail(raw_media)
        albums = create_albums_if_not_exists(raw_media)

        media = ReaderModel(
            id=raw_media.id,
            thumbnail_path=raw_media.thumbnail_dst_path,
            duration=raw_media.duration,
            webpage_url=raw_media.webpage_url,
            albums=albums
        )
        session.add(media)

    try:
        session.commit()
    except IntegrityError as e:
        print(e)
        session.rollback()
        raise HTTPError(400, "Reader already exists")

    return {}


class DownloadReadersIn(Schema):
    media_ids = List(String())


@media_bp.post("/download")
@media_bp.input(DownloadReadersIn, arg_name="params")
@media_bp.output({})
def download_medias(params):
    from api.app import COOKIES_PATH

    download_medias_helper(params["media_ids"], COOKIES_PATH)
    return {}


# class AddReaderToAlbumsIn(Schema):
#     media_id = String()
#     album_ids = List(String())


# @media_bp.post("/add-to-albums")
# @media_bp.input(AddReaderToAlbumsIn, arg_name="params")
# @media_bp.output({})
# def add_media_to_albums(params):
#     from api.app import session
#
#     # get media
#     q = session.query(ReaderModel).filter(ReaderModel.id == str(params["media_id"]))
#     media = q.first()
#
#     if not media:
#         raise HTTPError(404, "Reader not found")
#
#     q = session.query(AlbumModel).filter(AlbumModel.id.in_(params["album_ids"]))
#     for album in q.all():
#         if album not in media.albums:
#             media.albums.append(album)
#
#     session.commit()
#     return {}


class UpdateReaderAlbumsIn(Schema):
    media_id = String()
    album_ids = List(String())


@media_bp.post("/update-albums")
@media_bp.input(UpdateReaderAlbumsIn, arg_name="params")
@media_bp.output({})
def update_media_albums(params):
    from api.app import session

    media = session.query(ReaderModel).filter(ReaderModel.id == str(params["media_id"])).first()
    if not media:
        raise HTTPError(404, "Reader not found")

    media.albums.clear()
    q = session.query(AlbumModel).filter(AlbumModel.id.in_(params["album_ids"]))
    for album in q.all():
        media.albums.append(album)

    session.commit()
    return {}


class RemoveReaderFromAlbumIn(Schema):
    media_id = String()
    album_id = String()


@media_bp.post("/remove-from-album")
@media_bp.input(RemoveReaderFromAlbumIn, arg_name="params")
@media_bp.output({})
def remove_media_from_album(params):
    from api.app import session
    media = session.query(ReaderModel).filter(ReaderModel.id == str(params["media_id"])).first()
    if not media:
        raise HTTPError(404, "Reader not found")

    album = session.query(AlbumModel).filter(AlbumModel.id == str(params["album_id"])).first()
    if not album:
        raise HTTPError(404, "Album not found")

    media.albums.remove(album)
    session.commit()
    return {}


class GetReaderIn(Schema):
    media_id = String()


@media_bp.get("/")
@media_bp.input(GetReaderIn, arg_name="params", location="query")
@media_bp.output(ReaderSchema)
def get_media(params):
    from api.app import session
    media = session.query(ReaderModel).filter(ReaderModel.id == str(params["media_id"])).first()
    if not media:
        raise HTTPError(404, "Reader not found")
    media_dict = media.to_dict()
    media_dict["albums"] = [album.to_dict() for album in media.albums]
    return media_dict


class QueryReaderIn(Schema):
    # last_id and before_date are mutually exclusive
    last_id = String(load_default=None)
    before_date = String(load_default=None)
    limit = Integer(load_default=30)
    descending = Boolean(load_default=True)
    # search = String(load_default=None)
    album_id = String(load_default=None)


class QueryReaderOut(Schema):
    media = List(Nested(ReaderSchema))
    no_more_media = Boolean()


@media_bp.get("/query")
@media_bp.input(QueryReaderIn, arg_name="params", location="query")
@media_bp.output(QueryReaderOut)
def query_media(params):
    from api.app import session
    q = session.query(ReaderModel)

    if params["album_id"]:
        q = q.filter(ReaderModel.albums.any(id=str(params["album_id"])))

    if params["last_id"]:
        if params["descending"]:
            q = q.filter(ReaderModel.created_at_ksuid < params["last_id"])
        else:
            q = q.filter(ReaderModel.created_at_ksuid > params["last_id"])
    elif params["before_date"]:
        before_date_ksuid = date_to_ksuid(params["before_date"])
        q = q.filter(ReaderModel.created_at_ksuid < before_date_ksuid)
        q = q.order_by(desc(ReaderModel.created_at_ksuid))

    # if params["search"]:
    #     q = q.filter(ReaderModel.title.contains(params["search"]))

    if params["descending"]:
        q = q.order_by(desc(ReaderModel.created_at_ksuid))
    q = q.limit(params["limit"])

    # if params["album_id"]:
    #     media_list = [media.to_dict() for media in q.all()]
    # # if album was not specified, populate albums field of each media
    # else:
    #     media_list = []
    #     for media in q.all():
    #         media_dict = media.to_dict()
    #         media_dict["albums"] = [album.to_dict() for album in media.albums]
    #         media_list.append(media_dict)
    media_list = []
    for media in q.all():
        media_dict = media.to_dict()
        media_dict["albums"] = [album.to_dict() for album in media.albums]
        media_list.append(media_dict)

    return {
        "media": media_list,
        "no_more_media": len(media_list) < params["limit"]
    }


class DeleteReaderIn(Schema):
    media_ids = List(String())


@media_bp.delete("/")
@media_bp.input(DeleteReaderIn, arg_name="params")
@media_bp.output({})
def delete_media(params):
    from api.app import session, bucket

    paths_to_delete = []

    for media_id in params["media_ids"]:
        media: ReaderModel = session.query(ReaderModel).filter(ReaderModel.id == str(media_id)).first()
        paths_to_delete.append(media.thumbnail_path)
        if not media:
            continue
        session.delete(media)
    session.commit()

    # TODO: delete albums that media belongs to if they have no media left

    # Delete files from bucket in separate thread to avoid blocking request
    def delete_paths(paths):
        for path in paths:
            file = bucket.get_file_info_by_name(path)
            file.delete()

    threading.Thread(target=delete_paths, args=(paths_to_delete,)).start()

    return {}

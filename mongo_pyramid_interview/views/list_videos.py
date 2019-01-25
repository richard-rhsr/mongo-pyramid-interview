from pyramid.view import view_config
import pyramid.httpexceptions as exc
import bson
from pymongo.collection import ReturnDocument

import logging
log = logging.getLogger(__name__)

collection_name = 'videos'

@view_config(route_name='videos', renderer='../templates/list_videos.jinja2')
def list_videos(request):
    videos = request.db[collection_name].find()
    return {
        'videos': videos,
        'form_action': request.route_url('save_video'),
        'themes_link': request.route_url('themes'),
        'error_message': (request.session.pop_flash('error_message') or [''])[0],
        'name_field': (request.session.pop_flash('name_field') or [''])[0],
        'theme_field': (request.session.pop_flash('theme_field') or [''])[0],
    }

@view_config(route_name='save_video')
def save_video(request):
    name = (request.POST['name'] or '').strip()
    theme = (request.POST['theme'] or '').strip()
    if not name:
        request.session.flash('Video must have a Name', 'error_message')
        request.session.flash(theme, 'theme_field')
        raise exc.HTTPFound(request.route_url("videos"))
    elif not theme:
        request.session.flash('Video must have a Theme', 'error_message')
        request.session.flash(name, 'name_field')
        raise exc.HTTPFound(request.route_url("videos"))
    else:
        videos_collection = request.db[collection_name]
        videos_collection.update_one(
            {'name': name},
            {
                '$set': {'theme': theme},
                '$setOnInsert': {'likes': bson.int64.Int64(0), 'dislikes': bson.int64.Int64(0)},
            },
            upsert=True
        )
        raise exc.HTTPFound(request.route_url("videos"))

@view_config(route_name='like_video', renderer='json')
def like_video(request):
    videos_collection = request.db[collection_name]
    video_info = request.json_body
    name = video_info['name']
    updated_info = videos_collection.find_one_and_update(
        {'name': name},
        {'$inc': {'likes': bson.int64.Int64(1)} },
        return_document=ReturnDocument.AFTER
    )
    result = {
        'name': updated_info['name'],
        'theme': updated_info['theme'],
        'likes': updated_info['likes'] + 0,
        'dislikes': updated_info['dislikes'] + 0,
    }
    return result

@view_config(route_name='dislike_video', renderer='json')
def dislike_video(request):
    videos_collection = request.db[collection_name]
    video_info = request.json_body
    name = video_info['name']
    updated_info = videos_collection.find_one_and_update(
        {'name': name},
        {'$inc': {'dislikes': bson.int64.Int64(1)} },
        return_document=ReturnDocument.AFTER
    )
    result = {
        'name': updated_info['name'],
        'theme': updated_info['theme'],
        'likes': updated_info['likes'] + 0,
        'dislikes': updated_info['dislikes'] + 0,
    }
    return result

@view_config(route_name='themes', renderer='../templates/list_themes.jinja2')
def list_themes(request):
    pipeline = [
        {'$group': {'_id': '$theme', 'sum_likes': {'$sum': '$likes'}, 'sum_dislikes': {'$sum': '$dislikes'}}},
        {'$project': {'score': {'$subtract': ['$sum_likes', {'$divide': ['$sum_dislikes', 2]}]}}},
        {'$sort': {'score': -1}}
    ]
    themes = request.db[collection_name].aggregate(pipeline)
    return {
        'themes': themes,
        'videos_link': request.route_url('videos')
    }
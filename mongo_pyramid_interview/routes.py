def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('videos', '/', request_method='GET')
    config.add_route('themes', '/themes', request_method='GET')
    config.add_route('save_video', '/new_video', request_method='POST')
    config.add_route('like_video', '/like_video', request_method='POST')
    config.add_route('dislike_video', '/dislike_video', request_method='POST')

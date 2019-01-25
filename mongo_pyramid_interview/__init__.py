from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from urllib.parse import urlparse
from pymongo import MongoClient
# from gridfs import GridFS



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = MongoClient(
        host=db_url.hostname,
        port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
           db.authenticate(db_url.username, db_url.password)
        return db

    # def add_fs(request):
    #     return GridFS(request.db)

    config.add_request_method(add_db, 'db', reify=True)
    # config.add_request_method(add_fs, 'fs', reify=True)

    session_factory = SignedCookieSessionFactory(settings['session_secret'])
    config.set_session_factory(session_factory)

    config.include('pyramid_jinja2')
    config.include('.routes')
    
    config.scan()
    return config.make_wsgi_app()

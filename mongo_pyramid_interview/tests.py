import unittest

from pyramid import testing

from collections.abc import Iterable

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    # def test_videos_listing(self):
    #     from .views.list_videos import list_videos
    #     request = testing.DummyRequest()
    #     info = list_videos(request)
    #     # self.assertEqual(info['project'], 'mongo_pyramid_interview')
    #     self.assertIsInstance(info['videos'], Iterable)

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from mongo_pyramid_interview import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    # def test_list_videos(self):
    #     res = self.testapp.get('/', status=200)
    #     self.assertTrue(b'Videos Listing' in res.body)

    # def test_list_themes(self):
    #     res = self.testapp.get('/themes', status=200)
    #     self.assertTrue(b'Video Themes' in res.body)

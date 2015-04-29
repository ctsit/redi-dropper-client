'''
Goal: test functions in utils.py
'''

import os
# from werkzeug.datastructures import Headers
from redidropper import utils


def test_create_salt(app):
    '''
    Verify the remote address reading
    https://realpython.com/blog/python/python-web-applications-with-flask-part-iii/
    '''
    # add testing request context
    # http://flask.pocoo.org/docs/0.10/api/#flask.ctx.RequestContext
    wsgi_env = {
        'REMOTE_ADDR': os.environ.get('REMOTE_ADDR', '1.2.3.4'),
        'HTTP_USER_AGENT': os.environ.get('HTTP_USER_AGENT', 'cURL')}

    # headers = Headers([('Referer', '/example/url')])
    # with app.test_request_context(environ_base=wsgi_env, headers=headers):

    with app.test_request_context(environ_base=wsgi_env):
        actual_ip = utils._get_remote_addr()
        actual_agent = utils._get_user_agent()
        actual_hash = utils._create_salt()

        assert '1.2.3.4' == actual_ip
        assert 'cURL' == actual_agent
        assert 16 == len(actual_hash)


def test_generate_sha512_hmac():
    expected = '8vhMgmofeNDCISwvPc9yB7XQiNSPZHwDVz6kuYuA7aPA43j8RQVy+xwI2+87u3Pkpvq/qiuRuDreUoSxblqGzA=='
    actual = utils._generate_sha512_hmac('pepper', 'salt', 'password')
    assert actual == expected


def test_generate_auth(app):
    wsgi_env = {
        'REMOTE_ADDR': os.environ.get('REMOTE_ADDR', '1.2.3.4'),
        'HTTP_USER_AGENT': os.environ.get('HTTP_USER_AGENT', 'cURL')}

    with app.test_request_context(environ_base=wsgi_env):
        salt, actual_pass = utils.generate_auth('pepper', 'password')
        assert actual_pass is not None
        assert 88 == len(actual_pass)


def test_clean_int():
    """
    Verify common cases
    """
    cases = [
        {"x": None,     "exp": None},
        {"x": "",       "exp": None},
        {"x": "  ",     "exp": None},
        {"x": "  0x0",  "exp": None},
        {"x": "-1",     "exp": None},
        {"x": "-0.3",   "exp": None},
        {"x": "0.0",    "exp": None},
        {"x": "0",      "exp": 0},
        {"x": "0.3",    "exp": None},
        {"x": "01",     "exp": 1},
        {"x": "2",      "exp": 2},
        {"x": 3,        "exp": 3},
        {"x": 1.2,      "exp": None},
        {"x": 123,      "exp": 123},
    ]

    for case in cases:
        actual = utils.clean_int(case['x'])
        expected = case['exp']
        assert actual == expected


def test_allowed_file():
    cases = [
        {"x": None,     "exp": False},
        {"x": "",       "exp": False},
        {"x": "  ",     "exp": False},
        {"x": "  0x0",  "exp": False},
        {"x": "x.rar",  "exp": False},
        {"x": "tgz",    "exp": False},

        {"x": "a .txt", "exp": True},
        {"x": "b.pdf",  "exp": True},
        {"x": "c.png",  "exp": True},
        {"x": "d.jpg",  "exp": True},
        {"x": "e.jpeg", "exp": True},
        {"x": "f.gif",  "exp": True},
        {"x": "g.tiff", "exp": True},
        {"x": "h.zip",  "exp": True},
        {"x": "i.tar",  "exp": True},
        {"x": "j.tgz",  "exp": True},
        {"x": "k.bz2",  "exp": True},
        ]

    for case in cases:
        actual = utils.allowed_file(case['x'])
        expected = case['exp']
        assert actual == expected


def test_pack():

    assert '{"message":"msg","status":"info"}' == utils.pack_info("msg") \
        .replace(' ', '').replace('\n', '')
    assert '{"message":"msg","status":"error"}' == utils.pack_error("msg") \
        .replace(' ', '').replace('\n', '')

from redidropper import utils
#import unittest
#class TestUtils(unittest.TestCase):

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
    #assert '{"info": "<\' weird || danger;\\\\==="}' \ == utils.pack("info", "<' weird || danger;\===")
    assert '{"status": "info", "message": "msg"}' == utils.pack_info("msg")
    assert '{"status": "error", "message": "msg"}' == utils.pack_error("msg")

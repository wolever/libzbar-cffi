import libzbar as zbar

def test_version():
    assert zbar.zbar_version() == (0, 10)

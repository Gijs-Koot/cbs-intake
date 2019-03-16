import cbs_intake.cat
import os
import tempfile


def test_caching():

    fd = tempfile.gettempdir()
    fn = os.path.join(fd, cbs_intake.cat.CACHE_FILE)

    text = cbs_intake.cat.download_data()
    with open(fn) as f:
        same = f.read()

    assert len(same) == len(text), "contents of cache file and \
    returned data should be the same"


    entries = cbs_intake.cat.list_entries(text)

    assert len(entries) > 100, "should be at least 100 entries long"

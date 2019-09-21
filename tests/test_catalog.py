import cbs_intake.cat
import os
import tempfile
import pytest
from intake import open_catalog


@pytest.fixture
def sample_catalog():
    return open_catalog("./tests/cbs_catalog_sample.yml")


def test_reading_catalog():

    fd = tempfile.gettempdir()
    fn = os.path.join(fd, cbs_intake.cat.CACHE_FILE)

    breakpoint

    text = cbs_intake.cat.download_data()
    with open(fn) as f:
        same = f.read()

    assert len(same) == len(text), "contents of cache file and \
    returned data should be the same"

    entries = cbs_intake.cat.list_entries(text)

    assert len(entries) > 4000, "should be at least 100 entries long"


def test_read_sample(sample_catalog):

    pass
        

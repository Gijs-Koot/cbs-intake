import intake
import logging


def test_discovery():

    # hijack registry for live inserting class in registry
    cat = intake.open_catalog("./tests/cbs_catalog_sample.yml")

    # load one of the datasets
    src = cat['82439NED'].get()

    assert src.discover()["npartitions"] == 1

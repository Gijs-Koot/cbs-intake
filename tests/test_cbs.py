import intake
from cbs_intake.ds import CBSODataSource


def test_discovery():

    # hijack registry for live inserting class in registry
    intake.registry['cbs-odata'] = CBSODataSource
    cat = intake.open_catalog("./catalog/cbs.yml")

    # load one of the datasets
    src = cat['82055NED'].get()

    print(src.discover())

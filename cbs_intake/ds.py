import pandas as pd
from intake import DataSource, Schema


class CBSODataSource(DataSource):

    name = 'cbs-odata'

    def __init__(self, url, metadata=None):

        super(CBSODataSource, self).__init__(metadata)
        self.url = url

    def _get_schema(self):

        dtypes = [int]
        return Schema(datashape=None,
                      dtype=None,
                      shape=(None, len(dtypes)),
                      npartitions=1,
                      extra_metadata={})

    def _get_partition(self, i):

        return pd.DataFrame({
            "a": [1, 2]
        })

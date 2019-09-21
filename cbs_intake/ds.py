import pandas as pd
from intake import DataSource, Schema
import requests


class CBSODataSource(DataSource):

    name = 'cbs-odata'

    def __init__(self, url, metadata=None):

        self.base_url = url
        super(CBSODataSource, self).__init__(metadata)

    def _get_schema(self):

        dtypes = [int]
        return Schema(datashape=None,
                      dtype=None,
                      shape=(None, len(dtypes)),
                      npartitions=1,
                      extra_metadata={})

    def _get_partition(self, i):

        url = self.base_url + "/TypedDataSet"
        raw = requests.get(url).json()
        return pd.DataFrame(
            raw["value"]
        )

    def _close(self):
        pass

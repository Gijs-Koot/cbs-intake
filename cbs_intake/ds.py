import pandas as pd
from intake import DataSource, Schema
import requests


class CBSODataSource(DataSource):

    container = 'dataframe'
    name = 'cbs-odata'
    version = '0.0.1'
    partition_access = False

    def __init__(self, url, metadata=None):

        self.base_url = url
        self.dataprop_url = url + "/DataProperties"
        self.data_url = url + "/TypedDataSet"
        self.info_url = url + "/TableInfos"
        
        super(CBSODataSource, self).__init__(metadata)

    def _get_schema(self):

        # at this url, the columns are described 
        self.dataprops = requests.get(self.dataprop_url).json()["value"]
        
        # dimensions are special columns for which we need additional data
        self.dimensions = [dp for dp in self.dataprops if dp["Type"] == "Dimension"]

        # this gets additional info for dimensions, ie. what the keys actually mean
        for dim in self.dimensions:
            url = self.base_url + "/" + dim["Key"]
            dim["ddata"] = requests.get(url).json()["value"]

        self.n_columns = max(d['Position'] for d in self.dataprops if d['Position'])
        self.columns = [d['Key'] for d in self.dataprops if d['Position']]
        
        # TODO: dtypes need replacing
        self.dtypes = [
            d.get('Datatype', "categorical" if d["Type"] == "Dimension" else None) 
            for d in self.dataprops if d['Position']
        ]

        return Schema(datashape=None,
                      dtype=dict(zip(self.columns, self.dtypes)),
                      shape=(None, self.n_columns),
                      npartitions=1,
                      extra_metadata={})

    def _get_partition(self, i):

        url = self.base_url + "/TypedDataSet"
        raw = requests.get(url).json()
        
        df = pd.DataFrame(
            raw["value"]
        )

        # replace dimensions with actual values

        for dim in self.dimensions:
            df[dim["Key"]] = df[dim["Key"]].replace({
                    d['Key']: d['Title'] for d in dim["ddata"]
            }).astype("category")

        return df

    def _close(self):
        pass

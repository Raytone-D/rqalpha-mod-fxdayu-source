from rqalpha.data.base_data_source import BaseDataSource
from rqalpha_mod_mongo_datasource.share.astock_minute_reader import AStockBcolzMinuteBarReader

from rqalpha_mod_mongo_datasource.module.cache import CacheMixin
from rqalpha_mod_mongo_datasource.module.odd import OddFrequencyDataSource


class BundleDataSource(OddFrequencyDataSource, BaseDataSource):
    def __init__(self, path, bundle_path):
        super(BundleDataSource, self).__init__(path)
        self._bundle_reader = AStockBcolzMinuteBarReader(bundle_path)

    def raw_history_bars(self, instrument, frequency, start_dt=None, end_dt=None, length=None):
        sid = instrument.order_book_id
        data = self._bundle_reader.raw_history_bars(sid, start_dt, end_dt, length)
        return data

    def available_data_range(self, frequency):
        return self._bundle_reader.available_data_range()

    def is_base_frequency(self, instrument, freq):
        return freq in ["1m"]


class BundleCacheDataSource(BundleDataSource, CacheMixin):
    def __init__(self, path, bundle_path):
        super(BundleCacheDataSource, self).__init__(self, path, bundle_path)
        CacheMixin.__init__(self)

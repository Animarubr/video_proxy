import logging
from dataclasses import asdict

from ..schemas import Headers

logging.basicConfig(level=logging.INFO)


class GetHeader():
    """
        This class is responsable to get the request headers
    """
   
    def __init__(self, data:dict):
        self.header = Headers(
            content_type=data.get("content-type"),
            content_length=data.get("content-length"),
            cache_control=data.get("cache-control"),
            content_disposition= data.get("content-disposition"),
            accept_ranges=data.get("accept-ranges"),
            content_range=data.get("content-range"),
            connection="keep-alive"
        )

    def _dict(self):
        return asdict(self.header)

    def _dict_formated(self):
        return {k.replace("_", "-").title(): str(v) for k, v in asdict(self.header).items()}
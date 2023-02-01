import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from requests import Request
# import http.client
import logging

# http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.INFO)
start_time = time.time()
# You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

class Session:
    
    def __init__(self):
        self.http = requests.Session()
        self.retry = Retry(connect=5, backoff_factor=0.5)
        self.adapter = HTTPAdapter(max_retries=self.retry)
        self.http.mount("http://", self.adapter)
        self.http.mount("https://", self.adapter)
        self.headers = {}
    
    def make_request(self, method:str, url:str, headers:dict, verify:bool=True, stream:bool=False) -> Request:
        r = self.http.request(method=method, url=url, headers=headers, verify=verify, stream=stream)
        logging.info(f"--- Maked Request in: {time.time() - start_time} seconds ---")
        return r
        # try:
           
        # except Exception as e:
        #     logging.warning(f"Algo esta errado: {e}")
        #     raise HTTPException(status_code=500, detail=str(e))
        
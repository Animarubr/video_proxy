from httpx import Request

import httpx
import logging

logging.basicConfig(level=logging.INFO)

class SessionX:
    
    def __init__(self):
        self.headers = {}
        self.httpx = httpx.AsyncClient()
    
    async def get_headers_x(self, url:str) -> Request:
        async with self.httpx as client:
            r = await client.head(url=url, headers=self.headers)
        return r
    
    async def get_stream_x(self, url:str):
        client = httpx.AsyncClient()
        async with client.stream("GET", url=url, headers=self.headers) as response:
            async for chunk in response.aiter_bytes():
                yield chunk


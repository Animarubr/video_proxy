import logging
import random
from starlette.responses import StreamingResponse
from fastapi import HTTPException

from ..service.jwtdecode import Jwt
from ..service.sessionx import SessionX
from ..service.handle_headers import GetHeader
from ..models.buffers import Buffer

logging.basicConfig(level=logging.INFO)

class Proxy(SessionX):
    
    def __init__(self, token:str, range_header):
        super().__init__()
        self.data = self.solve_data(token)
        self.range = range_header
        self.referer = self.get_referer()
        self.chunk_size = 4096 * 1024 # 3145728 -> 3.1 mega 6291456  8192
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        ]
        self.buffer = Buffer()

    def solve_data(self, token):
        data = self.dec_token(token) 
        return data
    
    def dec_token(self, token):
        jwt = Jwt()
        return jwt.decode(token)
    
    def get_referer(self):
        ref = self.data.get("ref")
        if ref:
            logging.info(f"Referer-Anime: {ref}")
            return ref
        
        raise HTTPException(status_code=400, detail="Referer is empty!") 
    
    async def stream(self):
        from_bytes, until_bytes = self.range.replace("bytes=", "").split("-")
        target = self.data.get("url") if type(self.data.get("url")) != tuple else self.data.get("url")[0]
        user_agent = random.choice(self.user_agents) if type(self.data.get("url")) != tuple else self.data.get("url")[1]
        
        if not until_bytes:
            until_bytes = int(from_bytes) + self.chunk_size  # Default self.chunk_size is 3MB
        
        self.headers["referer"] = self.referer            
        self.headers["range"] = f"bytes={from_bytes}-{until_bytes}"
        self.headers["User-Agent"] = user_agent
        
        req = await self.get_headers_x(url=target)
        stream_bytes = self.get_stream_x(target)
        resp_headers = GetHeader(req.headers)._dict()
        
        resp_headers["range"] = self.headers.get("range")
        resp_headers["cache_control"] = resp_headers.get("cache_control").replace("private", "public")
        resp_headers["access-control-allow-headers"] = "Range"
        
        del resp_headers['content_disposition']
        
        if int(from_bytes) != 0:
            if until_bytes > int(from_bytes):
                resp_headers["range"] = f"bytes={self.chunk_size}-{from_bytes}"
        
        final_headers = {i.replace("_", "-").title():resp_headers[i] for i in resp_headers.keys() if resp_headers[i] is not None}

        response = StreamingResponse(
            stream_bytes,
            206,
            media_type=final_headers.get("Content-Type"),
            headers=final_headers
        )
        
        return response
    
                
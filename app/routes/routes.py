from fastapi import APIRouter, Header
from ..models.stream import Proxy

routes = APIRouter()

@routes.get("/proxy")
async def main(token: str, Range: str = Header(None)):
    range_header = Range
    
    if range_header is None:
        range_header = "bytes=0-"
        
    proxy = Proxy(token, range_header)
    return await proxy.stream()

# @routes.get("/teste/hentais")
# async def teste_hentais():
#     a = AssistirHentais("https://www.assistirhentai.com/episodio/isekai-kita-node-sukebe-skill-de-zenryoku-ouka-shiyou-to-omou-episodio-01/")
#     return a.get_video_link_from_iframe()
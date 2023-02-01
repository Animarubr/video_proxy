from dataclasses import dataclass

@dataclass
class Headers:
   content_type:str
   content_length:str
   cache_control:str
   content_disposition:str
   accept_ranges:str
   content_range:str
   connection:str

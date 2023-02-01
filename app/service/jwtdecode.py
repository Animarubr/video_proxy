from jose import jwt, JWTError

class Jwt:
    def __init__(self):
        self._JWT_SECRET = "animesvision"
       
    def encript(self, string):
        token = jwt.encode(string, self._JWT_SECRET)
        return token

    def decode(self, token):
        try:
            data = jwt.decode(
                token,
                key=self._JWT_SECRET,
                algorithms=[
                    "HS256",
                ],
            )
            return data
        except (ValueError, UnicodeDecodeError, JWTError) as exc:
            return ({'detail': str(exc), 'status':400})

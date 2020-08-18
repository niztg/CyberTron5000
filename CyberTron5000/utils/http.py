from aiohttp import ClientSession


class APIError(Exception):
    def __init__(self, message="An issue has occured with the API!"):
        self.message = message

    def __str__(self):
        return self.message


class CyberHTTP:
    def __init__(self):
        self.session = None

    async def set_session(self):
        self.session = ClientSession()

    async def get(self, url, **kwargs):
        if not self.session:
            await self.set_session()
        try:
            async with self.session.get(url, **kwargs) as r:
                if r.status != 200 or r.status == 404: # i know this is obselete
                    raise APIError()
                data = await r.json()
        except Exception as error:
            raise error
        return data

    async def close(self):
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

from core.logger import log, trace, json
import inspect
import httpx
import os

httpxcept = (httpx._exceptions.WriteError,
             httpx._exceptions.ConnectTimeout,
             httpx._exceptions.ReadTimeout,
             httpx._exceptions.ConnectError,
             ConnectionResetError,
             Exception)


class Client:
    def __init__(self, url, **kwargs):
        self.limit = int(kwargs.get('limit', 3))
        self.url = url

    def process(self, exc):
        log.debug(exc)

    def post(self, **kwargs):
        for x in range(1, self.limit + 1):
            try:
                with httpx.Client() as client:
                    client.post(url=self.url, **kwargs)
                return

            except httpxcept as exc:
                self.process(exc)

    def get(self, **kwargs):
        for x in range(1, self.limit + 1):
            try:
                with httpx.Client() as client:
                    r = client.get(url=self.url, **kwargs)
                return r

            except httpxcept as exc:
                self.process(exc)

        return None

    async def async_post(self, **kwargs):
        for x in range(1, self.limit + 1):
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(url=self.url, **kwargs)
                return

            except httpxcept as exc:
                self.process(exc)

    async def async_get(self, **kwargs):
        for x in range(1, self.limit + 1):
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(url=self.url, **kwargs)
                return r

            except httpxcept as exc:
                self.process(exc)

        return None


class API(Client):
    def __init__(self, loc='', **kwargs):
        pre = f"http://{json.orm['api']['host']}:{json.orm['api']['port']}/{loc}"
        super().__init__(pre, **kwargs)


api = API


Request = Client

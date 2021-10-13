from typing import Callable
from core.logger import log, trace, json
import functools
import inspect
import httpx
import os

httpxcept = (httpx._exceptions.WriteError,
             httpx._exceptions.ConnectTimeout,
             httpx._exceptions.ReadTimeout,
             httpx._exceptions.ConnectError,
             ConnectionResetError,
             Exception)


def retry(method: Callable):  # this implements the retry functionality in a better way
    @functools.wraps(method)
    def _retry(self, *args, **kwargs):
        for x in range(1, self.limit + 1):
            try:
                return method(self, *args, **kwargs)
            except httpxcept as exc:
                self.process(exc)
        return self
    return _retry


class Client:
    def __init__(self, url: str, **kwargs):
        self.limit = int(kwargs.get('limit', 3))
        self.url = url

    def json(self):  # returns None if it fails to return anything in the retry
        return None  # this prevents a potentially fatal error from occuring

    def process(self, exc: Exception):
        log.warn(exc)

    @retry
    def post(self, **kwargs) -> httpx.Response:
        with httpx.Client() as client:
            client.post(url=self.url, **kwargs)
        return

    @retry
    def get(self, **kwargs) -> httpx.Response:
        with httpx.Client() as client:
            r = client.get(url=self.url, **kwargs)
        return r

    @retry
    async def async_post(self, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            await client.post(url=self.url, **kwargs)
        return

    @retry
    async def async_get(self, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            r = await client.get(url=self.url, **kwargs)
        return r


class API(Client):
    def __init__(self, loc: str = '', **kwargs):
        pre = f"http://{json.orm['api']['host']}:{json.orm['api']['port']}/{loc + '/' if loc[-1] != '/' else loc}"
        super().__init__(pre, **kwargs)  # the last ternery in the above tries to mitigate 308 redirects


api = API


Request = Client

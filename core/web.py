from core.logger import log, trace, json
import httpx
import os

httpxcept = (httpx._exceptions.WriteError,
             httpx._exceptions.ConnectTimeout,
             httpx._exceptions.ReadTimeout,
             httpx._exceptions.ConnectError,
             Exception)


class Client:
    def __init__(self, url, **kwargs):
        self.limit = int(kwargs.get('limit', 3))
        self.url = url

    def process(self, exc):
        log.debug(exc)

    def post(self, _json: dict):
        for x in range(1, self.limit + 1):
            try:
                with httpx.Client() as client:
                    client.post(url=self.url, json=_json)
                return
            except httpxcept as exc:
                self.process(exc)
            # except httpx._exceptions.WriteError:
            #     log.error(f'[POST] {self.url} Write Error (Attempt #{x})')
            # except httpx._exceptions.ConnectTimeout:
            #     log.error(f'[POST] {self.url} Connect Timeout (Attempt #{x})')
            # except httpx._exceptions.ReadTimeout:
            #     log.error(f'[POST] {self.url} Read Timeout (Attempt #{x})')
            # except Exception as exc:
            #     log.exception(exc)
        log.error(f'[POST] {self.url} failed after {self.limit} attempts')

    def get(self, header=None):
        for x in range(1, self.limit + 1):
            try:
                with httpx.Client() as client:
                    r = client.get(url=self.url, headers=header)
                return r
            except _exc as exc:
                log.error('Web exception occured')
            # except httpx._exceptions.ConnectTimeout:
            #     log.error(f'[GET] {self.url} Connect Timeout (Attempt #{x})')
            # except httpx._exceptions.ReadTimeout:
            #     log.error(f'[GET] {self.url} Read Timeout (Attempt #{x})')
            # except Exception as exc:
            #     log.exception(exc)
        log.error(f'[GET] {self.url} failed after {self.limit} attempts')
        return None

    async def async_post(self, _json: dict):
        for x in range(1, self.limit + 1):
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(url=self.url, json=_json)
                return
            except httpx._exceptions.WriteError as exc:
                log.error(f'[POST] {self.url} Write Error (Attempt #{x})')
                # log.exception(exc)
            except httpx._exceptions.ConnectTimeout:
                log.error(f'[POST] {self.url} Connect Timeout (Attempt #{x})')
            except httpx._exceptions.ReadTimeout:
                log.error(f'[POST] {self.url} Read Timeout (Attempt #{x})')
            except Exception as exc:
                log.exception(exc)
        log.error(f'[POST] {self.url} failed after {self.limit} attempts')

    async def async_get(self):
        for x in range(1, self.limit + 1):
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(url=self.url)
                return r
            except httpx._exceptions.ConnectTimeout:
                log.error(f'[GET] {self.url} Connect Timeout (Attempt #{x})')
            except httpx._exceptions.ReadTimeout:
                log.error(f'[GET] {self.url} Read Timeout (Attempt #{x})')
            except Exception as exc:
                log.exception(exc)
        log.error(f'[GET] {self.url} failed after {self.limit} attempts')
        return None


class API(Client):
    def __init__(self, loc='', **kwargs):
        _pre = f"http://{json.orm['api']['host']}:{json.orm['api']['port']}/{loc}"
        super().__init__(_pre, **kwargs)


api = API


Request = Client

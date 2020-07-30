from core.logger import log
import httpx
import os


class Client:
    def __init__(self, url):
        self.url = url

    def post(self, json):
        try:
            with httpx.Client() as client:
                client.post(url=self.url, json=dict(json))
        except httpx._exceptions.WriteError:
            log.debug(f'{self.url} Write Error')
        except httpx._exceptions.ConnectTimeout:
            log.debug(f'{self.url} Connect Timeout')
        except httpx._exceptions.ReadTimeout:
            log.debug(f'{self.url} Read Timeout')
        except Exception as exc:
            log.exception(exc)

    def get(self):
        try:
            with httpx.Client() as client:
                r = client.get(url=self.url)
            return r
        except httpx._exceptions.ConnectTimeout:
            log.debug(f'{self.url} Connect Timeout')
        except httpx._exceptions.ReadTimeout:
            log.debug(f'{self.url} Read Timeout')
        except Exception as exc:
            log.exception(exc)
        return None

    async def async_post(self, json):
        try:
            async with httpx.AsyncClient() as client:
                await client.post(url=self.url, json=dict(json))
        except httpx._exceptions.WriteError:
            log.debug(f'{self.url} Write Error')
        except httpx._exceptions.ConnectTimeout:
            log.debug(f'{self.url} Connect Timeout')
        except httpx._exceptions.ReadTimeout:
            log.debug(f'{self.url} Read Timeout')
        except Exception as exc:
            log.exception(exc)

    async def async_get(self):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url=self.url)
            return r
        except httpx._exceptions.ConnectTimeout:
            log.debug(f'{self.url} Connect Timeout')
        except httpx._exceptions.ReadTimeout:
            log.debug(f'{self.url} Read Timeout')
        except Exception as exc:
            log.exception(exc)
        return None


Request = Client

import json

import aiohttp
from aiohttp import ClientResponse

import dto
from data.config import API_BACKEND_URL
from data.logger_config import logger


class HttpClient:

    @classmethod
    async def make_request(cls, method: str, path: str, data=None, headers=None, **kwargs):
        headers = headers or {}
        headers["Accept"] = "application/json"

        url = f"{API_BACKEND_URL}{path}"

        if data is not None:
            data = data.to_payload()
        elif data is None and method == "POST":
            raise NotImplementedError

        body = json.dumps(data) if data else None
        headers["Content-Type"] = "application/json"

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=body, headers=headers, **kwargs) as resp:
                logger.info(f'REQUEST\nBODY: {body}\nHEADERS: {headers}\nURL: {url}')
                await resp.json()
                return resp


class HttpBase(HttpClient):
    base_url = '/base'

    @classmethod
    async def _request(cls, path: str, method: str, data: dto.BaseDto = None, headers: dict = None, **kwargs) -> ClientResponse:
        path = f'{cls.base_url}{path}'
        return await HttpClient.make_request(path=path, method=method, data=data, headers=headers, **kwargs)


    @classmethod
    async def _make_response(cls, response: ClientResponse):
        try: data = await response.json()
        except: data = {}

        logger.info(f'RESPONSE: {await response.json()}')

        return {**data, "code": response.status}







import copy
import mimetypes
import os
from typing import Any, Coroutine

import aiohttp
from typing_extensions import Optional

from data.config import API_BACKEND_URL, API_BACKEND_KEY
from data.logger_config import logger
from dto import *
import json
from dto import single_dto
import dto
from dto.api_response import ApiResponse


class FormDataAdapter:
    @staticmethod
    def adapt(data: dict) -> aiohttp.FormData:
        form = aiohttp.FormData()

        def _add_recursive(prefix, value):
            if isinstance(value, dict):
                for k, v in value.items():
                    new_key = f"{prefix}[{k}]" if prefix else k
                    _add_recursive(new_key, v)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    new_key = f"{prefix}[{i}]"
                    _add_recursive(new_key, item)
            elif isinstance(value, tuple) and len(value) == 3:
                file_obj, filename, content_type = value
                form.add_field(prefix, file_obj, filename=filename, content_type=content_type)
            else:
                form.add_field(prefix, str(value))

        for key, value in data.items():
            _add_recursive(key, value)

        return form


class HttpClient:
    API_KEY = API_BACKEND_KEY

    @classmethod
    async def make_request(
            cls,
            method: str,
            path: str,
            data: None | BaseDto = None,
            headers: None | dict = None,
            content_type: str = "json",
            **kwargs
    ):
        headers = headers or {}
        headers.update({
            "Accept": "application/json",
            "X-API-Key": API_BACKEND_KEY
        })

        url = f"{API_BACKEND_URL}{path}"

        payload = None
        if data is not None:
            if isinstance(data, BaseDto):
                payload = data.to_payload()
            else:
                raise ValueError("Data must be BaseDto instance")
        elif method.upper() in ["POST", "PUT", "PATCH"]:
            payload = {}


        if content_type == "form-data":
            data = cls._prepare_files(payload)
            body = FormDataAdapter.adapt(data)
        elif content_type == "json":
            headers["Content-Type"] = "application/json"
            body = json.dumps(payload)
        else:
            raise ValueError("Unsupported content type")

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=body, headers=headers, **kwargs) as resp:
                try:
                    response_data = await resp.json()
                except:
                    response_data = await resp.text()

                logger.info(f'REQUEST\nBODY: {body}\nHEADERS: {headers}\nURL: {url}\nRESPONSE: {response_data}')
                return {"data": response_data, "status": resp.status}


    @staticmethod
    def _prepare_files(data: dict) -> dict:
        if not data:
            return {}

        result = copy.deepcopy(data)

        def _process(obj):
            if isinstance(obj, dict):
                return {k: _process(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_process(item) for item in obj]
            elif isinstance(obj, str) and os.path.isfile(obj):
                filename = os.path.basename(obj)
                content_type = mimetypes.guess_type(obj)[0] or "application/octet-stream"
                return (open(obj, "rb"), filename, content_type)
            return obj

        return _process(result)


class HttpUser(HttpClient):
    base_url = '/user'

    @classmethod
    async def _request(
            cls,
            path: str,
            method: str,
            data: BaseDto | None = None,
            headers: dict | None = None,
            **kwargs
    ) -> dict:

        full_path = f'{cls.base_url}{path}'
        return await cls.make_request(
            method=method,
            path=full_path,
            data=data,
            headers=headers,
            **kwargs
        )

    @classmethod
    async def create(cls, data: UserDto) -> ApiResponse:
        response = await cls._request('', 'POST', data=data)

        if response.get("status") == 200:
            return ApiResponse(
                data=UserDto.model_validate(response["data"]),
                status=response.get("status"),
            )
        else:
            return ApiResponse(
                status=response.get("status"),
                message=response.get("message", None)
            )

    @classmethod
    async def get(cls, chat_id: int):
        response = await cls._request(f'/{chat_id}', 'GET')
        print(response)

        if response.get("status") == 200:
            return ApiResponse(
                data=UserDto.model_validate(response["data"]),
                status=response.get("status"),
            )
        else:
            return ApiResponse(
                status=response.get("status"),
                message=response.get("detail", None)
            )





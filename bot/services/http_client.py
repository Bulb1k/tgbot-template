from typing import Any, Optional, Dict, Type, TypeVar, List

import httpx
from pydantic import BaseModel, TypeAdapter

from data.config import API_BACKEND_URL, API_BACKEND_KEY
from data.logger_config import logger
from schemas import *

T = TypeVar('T')


class HttpClient:

    def __init__(self, base_url: str = API_BACKEND_URL, api_key: str = API_BACKEND_KEY, timeout: float = 30.0):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout

    def _prepare_data(self, data: Any) -> Optional[Dict]:
        if data is None:
            return None
        if isinstance(data, BaseModel):
            return data.model_dump(exclude_none=True)
        return data

    async def request(
            self,
            method: str,
            path: str,
            data: Any = None,
            files: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            **kwargs
    ) -> ApiResponse[Any]:
        url = f"{self.base_url}{path}"
        prepared_data = self._prepare_data(data)

        default_headers = {
            "X-API-Key": self.api_key
        }

        if headers:
            default_headers.update(headers)

        logger.info(f"REQUEST | {method} {url} | Data: {prepared_data}")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    json=prepared_data,
                    headers=default_headers,
                    **kwargs
                )

            try:
                response_data = response.json()
            except Exception:
                response_data = None

            logger.info(f"RESPONSE | {response.status_code} | Data: {response_data}")

            return ApiResponse(
                data=response_data,
                status_code=response.status_code,
                success=response.is_success
            )

        except httpx.TimeoutException:
            logger.error(f"Timeout for {method} {url}")
            return ApiResponse(data=None, status_code=408, success=False)
        except Exception as e:
            logger.error(f"Error for {method} {url}: {e}")
            return ApiResponse(data=None, status_code=500, success=False)


class HttpBase:
    base_path: str = ""
    client = HttpClient()

    @classmethod
    async def _request(cls, method: str, path: str = "", data: Any = None, files: Optional[Dict] = None,
                       **kwargs) -> ApiResponse:
        full_path = f"{cls.base_path}{path}"
        return await cls.client.request(method, full_path, data=data, files=files, **kwargs)

    @classmethod
    def _make_response(cls, response: ApiResponse, schema: Type[T]) -> ApiResponse[T]:
        if response.success:
            try:
                validated_data = schema.model_validate(response.data)
                return ApiResponse(
                    data=validated_data,
                    status_code=response.status_code,
                    success=response.success
                )
            except Exception as e:
                logger.error(f"Validation error: {e}")
        return ApiResponse(
            data=None,
            status_code=response.status_code,
            success=False
        )

    @classmethod
    def _make_list_response(cls, response: ApiResponse, schema: Type[T]) -> ApiResponse[List[T]]:
        if response.success:
            try:
                validated_data = TypeAdapter(List[schema]).validate_python(response.data)
                return ApiResponse(
                    data=validated_data,
                    status_code=response.status_code,
                    success=response.success
                )
            except Exception as e:
                logger.error(f"Validation error: {e}")
        return ApiResponse(
            data=None,
            status_code=response.status_code,
            success=False
        )

    @classmethod
    async def get(cls, path: str = "", **kwargs) -> ApiResponse:
        return await cls._request("GET", path, **kwargs)

    @classmethod
    async def post(cls, path: str = "", data: Any = None, files: Optional[Dict] = None, **kwargs) -> ApiResponse:
        return await cls._request("POST", path, data=data, files=files, **kwargs)

    @classmethod
    async def put(cls, path: str = "", data: Any = None, **kwargs) -> ApiResponse:
        return await cls._request("PUT", path, data=data, **kwargs)

    @classmethod
    async def delete(cls, path: str = "", **kwargs) -> ApiResponse:
        return await cls._request("DELETE", path, **kwargs)

    @classmethod
    async def patch(cls, path: str = "", data: Any = None, **kwargs) -> ApiResponse:
        return await cls._request("PATCH", path, data=data, **kwargs)

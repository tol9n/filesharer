import os
from io import BytesIO
import httpx
from aiobotocore.session import get_session
from dotenv import load_dotenv

load_dotenv()


class Manager:
    def __init__(self, bucket):
        self.bucket = bucket
        self.session = get_session()

    async def _get_client(self):
        client = self.session.create_client(
            's3',
            region_name='ru-central1',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id=os.getenv('aws_access_key_id'),
            aws_secret_access_key=os.getenv('aws_secret_access_key')
        )
        return client

    async def get_object_list(self) -> dict[str, str | list]:
        async with await self._get_client() as client:
            response = await client.list_objects_v2(Bucket=self.bucket, Prefix='')
            return response

    async def get_object_by_name(self, file_name: str) -> BytesIO | str:
        async with await self._get_client() as client:
            try:
                response = await client.get_object(
                    Bucket=self.bucket,
                    Key=file_name
                )
                body = await response['Body'].read()
                return BytesIO(body)
            except:
                return 'error while download'

    async def put_object(self, file_name: str, file_path: str) -> str:
        async with await self._get_client() as client:
            with open(file_name, 'rb') as f:
                try:
                    await client.put_object(
                        Bucket=self.bucket,
                        Key=file_path,
                        Body=f,
                    )
                    return 'success'
                except:
                    return 'error while upload'

    async def delete_object(self, file_path: str) -> str:
        async  with await self._get_client() as client:
            try:
                await client.delete_object(Bucket=self.bucket, Key=file_path)
                return 'success'
            except:
                return 'error while delete'

    # async def delete_folder(self, folder_path: str) -> list[str | dict[str, str]]:
    #     async with await self._get_client() as client:
    #         object_list = await self.get_object_list()
    #         return object_list

    async def put_object_bytes(self, file_url: str, file_name: str) -> str:
        async with await self._get_client() as client:
            req = httpx.get("http://l-florist.ru/themes/FKFnbMINp4U.jpg").content
            try:
                await client.put_object(
                    Bucket=self.bucket,
                    Key=file_name,
                    Body=req,
                )
                return 'success'
            except:
                return 'error while upload'

#TODO: допилить удаление папок (перебор по префиксу и удаление всех подходящих)
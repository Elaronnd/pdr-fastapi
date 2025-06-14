from contextlib import asynccontextmanager
from io import BytesIO

from PIL.Image import Image
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from app.config.config import ACCESS_KEY_R2, SECRET_KEY_R2, ENDPOINT_URL_R2, BUCKET_NAME_R2


class R2Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "region_name": "auto"
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def is_file_exists(self, filename: str, folder: str) -> bool:
        async with self.get_client() as client:
            try:
                await client.head_object(
                    Bucket=self.bucket_name,
                    Key=f"{folder}/{filename}"
                )
                return True
            except ClientError as error:
                if error.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                    return False
                raise error

    async def upload_file(
            self,
            img: Image,
            filename: str,
            folder: str
    ):
        if await self.is_file_exists(filename=filename, folder=folder) is True:
            raise FileExistsError("filename already in S3 database")

        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=95)
        buffer.seek(0)

        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=f"{folder}/{filename}",
                Body=buffer
            )

    async def delete_file(self, filename: str, folder: str):
        async with self.get_client() as client:
            try:
                await client.delete_object(
                    Bucket=self.bucket_name,
                    Key=f"{folder}/{filename}"
                )
            except ClientError as error:
                if error.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                    return
                raise error

    async def generate_image_url(
            self,
            filename: str,
            folder: str
    ) -> str:
        async with self.get_client() as client:
            url = await client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': f"{folder}/{filename}"},
                ExpiresIn=3600
            )
            return url


r2_client = R2Client(
    access_key=ACCESS_KEY_R2,
    secret_key=SECRET_KEY_R2,
    endpoint_url=ENDPOINT_URL_R2,
    bucket_name=BUCKET_NAME_R2
)

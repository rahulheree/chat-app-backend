# from minio import Minio
# from minio.error import S3Error
# from .settings import settings
# import io


# class MinioClient:
#     def __init__(self):
#         self.client = Minio(
#             settings.MINIO_ENDPOINT,
#             access_key=settings.MINIO_ACCESS_KEY,
#             secret_key=settings.MINIO_SECRET_KEY,
#             secure=False  # Set to True in production with HTTPS
#         )
#         self.bucket_name = settings.MINIO_BUCKET

#     def initialize_bucket(self):
#         """
#         Creates the bucket if it doesn't already exist.
#         """
#         try:
#             found = self.client.bucket_exists(self.bucket_name)
#             if not found:
#                 self.client.make_bucket(self.bucket_name)
#                 print(f"Bucket '{self.bucket_name}' created.")
#             else:
#                 print(f"Bucket '{self.bucket_name}' already exists.")
#         except S3Error as exc:
#             print("Error initializing MinIO bucket:", exc)
#             raise

#     def upload_file(self, file_name: str, file_data: bytes) -> str:
#         """
#         Uploads a file to the MinIO bucket.

#         :param file_name: The name of the file to be saved.
#         :param file_data: The file content in bytes.
#         :return: The URL of the uploaded file.
#         """
#         try:
#             file_stream = io.BytesIO(file_data)
#             self.client.put_object(
#                 self.bucket_name,
#                 file_name,
#                 file_stream,
#                 length=len(file_data),
#             )
#             file_url = f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{file_name}"
#             return file_url
#         except S3Error as exc:
#             print("Error uploading file to MinIO:", exc)
#             raise


# minio_client = MinioClient()
from minio import Minio
from minio.error import S3Error
from datetime import timedelta
from .settings import settings
import io


class MinioClient:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False  # Set True if HTTPS
        )
        self.bucket_name = settings.MINIO_BUCKET

    def initialize_bucket(self):
        """
        Creates the bucket if it doesn't already exist.
        """
        try:
            found = self.client.bucket_exists(self.bucket_name)
            if not found:
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created.")
            else:
                print(f"Bucket '{self.bucket_name}' already exists.")
        except S3Error as exc:
            print("Error initializing MinIO bucket:", exc)
            raise

    def upload_file(self, file_name: str, file_data: bytes) -> dict:
        """
        Uploads a file to MinIO and returns file_name + presigned URL.
        """
        try:
            file_stream = io.BytesIO(file_data)
            self.client.put_object(
                self.bucket_name,
                file_name,
                file_stream,
                length=len(file_data),
            )
            # Generate presigned URL (valid 1 hour)
            file_url = self.client.presigned_get_object(
                self.bucket_name,
                file_name,
                expires=timedelta(hours=1)
            )
            return {"file_name": file_name, "file_url": file_url}
        except S3Error as exc:
            print("Error uploading file to MinIO:", exc)
            raise

    def generate_presigned_url(self, file_name: str, expiry_hours: int = 1) -> str:
        """
        Generate a new presigned URL for an existing file.
        """
        try:
            return self.client.presigned_get_object(
                self.bucket_name,
                file_name,
                expires=timedelta(hours=expiry_hours)
            )
        except S3Error as exc:
            print("Error generating presigned URL:", exc)
            raise


minio_client = MinioClient()


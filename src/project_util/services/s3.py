import boto3
from dotenv import load_dotenv


class S3Client:
    def __init__(
        self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
    ):
        """
        Store your access keys in the env variables:

        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY

        When using temporary credentials:
        - AWS_SESSION_TOKEN

        Otherwise pass them into the arguments.
        :param aws_access_key_id:
        :param aws_secret_access_key:
        :param aws_session_token:
        """
        load_dotenv()
        self._boto3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )

    def save(self, data: bytes, bucket_name: str, path: str):
        self._boto3.put_object(Body=data, Bucket=bucket_name, Key=path)

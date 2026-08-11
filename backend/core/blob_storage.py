import os
import uuid
from dotenv import load_dotenv

load_dotenv()

from azure.storage.blob import BlobServiceClient


connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER")

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

container_client = blob_service_client.get_container_client(
    container_name
)


def upload_pdf(file):
    extension = file.filename.split(".")[-1]

    blob_name = f"{uuid.uuid4()}.{extension}"

    blob_client = container_client.get_blob_client(blob_name)

    blob_client.upload_blob(
        file.file,
        overwrite=True
    )

    return blob_client.url


def upload_text(text: str):

    blob_name = f"{uuid.uuid4()}.txt"

    blob_client = container_client.get_blob_client(blob_name)

    blob_client.upload_blob(
        text.encode("utf-8"),
        overwrite=True
    )

    return blob_client.url


def upload_url(url: str):

    blob_name = f"{uuid.uuid4()}.txt"

    blob_client = container_client.get_blob_client(blob_name)

    blob_client.upload_blob(
        url.encode("utf-8"),
        overwrite=True
    )

    return blob_client.url


def delete_blob(blob_url: str):

    blob_name = blob_url.split("/")[-1]

    blob_client = container_client.get_blob_client(
        blob_name
    )

    blob_client.delete_blob()
  

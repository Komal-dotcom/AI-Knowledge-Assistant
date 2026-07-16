import requests

from config import BACKEND_URL


def get_documents():

    response = requests.get(
        f"{BACKEND_URL}/documents"
    )

    response.raise_for_status()

    return response.json()

def upload_document(file):

    response = requests.post(
        f"{BACKEND_URL}/documents",
        files={
            "file": (
                file.name,
                file.getvalue(),
                "application/pdf",
            )
        },
    )

    response.raise_for_status()

    return response.json()
import base64
import io
import os
import pickle

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


from config import TMP_PATH

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():
    creds = None

    token_b64 = os.environ["GOOGLE_TOKEN_PICKLE"]

    path = os.path.join(TMP_PATH, "token.pickle")

    if os.path.exists(path):
        with open(path, "rb") as token:
            creds = pickle.load(token)
            return build("drive", "v3", credentials=creds)

    if token_b64 != "":
        with open(path, "wb") as f:
            f.write(base64.b64decode(token_b64))

    if os.path.exists(path):
        with open(path, "rb") as token:
            creds = pickle.load(token)
            return build("drive", "v3", credentials=creds)

    ## if pickle expire uncoment rerun reconvert the new pickle to base64 and readd it to the .env

    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)

    #     with open('token.pickle', 'wb') as token:
    #         pickle.dump(creds, token)

    if not creds or not creds.valid and not creds.refresh_token:
        raise RuntimeError(
            "Invalid credentials and no refresh token — re-authenticate manually."
        )


def list_files(service, folder_id):
    results = (
        service.files()
        .list(q=f"'{folder_id}' in parents and trashed=false", fields="files(id, name)")
        .execute()
    )
    return results.get("files", [])


def download_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)

    with io.FileIO(file_name, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()


def move_file(service, file_id, new_folder_id, new_name=None):
    file = service.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(file.get("parents"))

    body = {}
    if new_name:
        body["name"] = new_name

    service.files().update(
        fileId=file_id,
        addParents=new_folder_id,
        removeParents=previous_parents,
        body=body if body else None,
    ).execute()


def upload_log(service, folder_id, file_name, content):
    from io import BytesIO
    from googleapiclient.http import MediaIoBaseUpload

    media = MediaIoBaseUpload(BytesIO(content.encode()), mimetype="text/plain")

    service.files().create(
        body={"name": file_name, "parents": [folder_id]}, media_body=media
    ).execute()

import pandas as pd
from googleapiclient.discovery import Resource

from config import ERROR_ID, LOG_ID
from utils.driveHelper import move_file
from utils.fileManager import WriteLog


def convertCsvToPanda(path: str, file, service: Resource):
    try:
        df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8")
        return df

    except Exception as ex:
        WriteLog(service, LOG_ID, file["name"], f"CSV read failed: {ex}")
        move_file(service, file["id"], ERROR_ID)
        return None

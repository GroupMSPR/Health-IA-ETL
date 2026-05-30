import pandas as pd
from config import ERROR_ID, LOG_ID
from utils.driveHelper import move_file
from utils.fileManager import WriteLog
from googleapiclient.discovery import Resource


def convertExcelToPanda(path: str, file, service: Resource):
    try:
        df = pd.read_excel(path)
        return df

    except Exception as ex:
        WriteLog(service, LOG_ID, file["name"], f"Excel read failed: {ex}")
        move_file(service, file["id"], ERROR_ID)
        return None

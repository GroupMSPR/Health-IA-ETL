import json

import pandas
from googleapiclient.discovery import Resource

from config import ERROR_ID, LOG_ID
from utils.driveHelper import move_file
from utils.fileManager import WriteLog


def convertJsonToPanda(path: str, file, service: Resource):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            df = pandas.DataFrame(data["data"])
        elif isinstance(data, list):
            df = pandas.DataFrame(data)
        else:
            WriteLog(
                service,
                LOG_ID,
                file["name"],
                "fileType not understood. If object, it must contain a 'data' list.",
            )
            move_file(service, file["id"], ERROR_ID)
            return None

        return df

    except Exception as ex:
        WriteLog(service, LOG_ID, file["name"], str(ex))
        move_file(service, file["id"], ERROR_ID)
        return None

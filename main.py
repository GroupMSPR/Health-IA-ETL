import os

from dotenv import load_dotenv

import pandas

from googleapiclient.discovery import Resource
from handlers.csvHandler import convertCsvToPanda
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from config import ERROR_ID, LOG_ID, TMP_PATH, TO_IMPORT_ID, Base
from handlers.excelHandler import convertExcelToPanda
from utils import driveHelper
from utils.fileManager import GetFileType, WriteLog
from handlers.dbHandler import sendToTable
from handlers.jsonHandler import convertJsonToPanda


def Main():

    load_dotenv()

    try:
        db_url = os.getenv("DATABASE_URL")

        if not db_url:
            print("Erreur : DATABASE_URL est vide ou non définie.")
            return

        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        engine: Engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        session: Session = Session(engine)

    except Exception as e:
        print("DB error:", e)
        return

    service: Resource = driveHelper.get_drive_service()

    files = driveHelper.list_files(service, TO_IMPORT_ID)
    files = sorted(
        files, key=lambda x: (not x["name"][0].isdigit(), x["name"].lower())
    )  # if there is more then 9 table we'll have to redo it to sort based on value

    for file in files:
        file_id = file["id"]
        file_name = file["name"]

        driveHelper.download_file(service, file_id, os.path.join(TMP_PATH, file_name))
        local_path = os.path.join(TMP_PATH, file_name)

        data: pandas.DataFrame = None
        match GetFileType(local_path):
            case "csv":
                data = convertCsvToPanda(local_path, file, service)
            case "xlsx":
                data = convertExcelToPanda(local_path, file, service)
            case "json":
                data = convertJsonToPanda(local_path, file, service)
            case _:
                driveHelper.move_file(service, file_id, ERROR_ID)
                WriteLog(service, LOG_ID, file_name, "unrecognise dataType")
                continue

        if data is not None:
            cols_with_lists = [
                col
                for col in data.columns
                if data[col].apply(lambda x: isinstance(x, list)).any()
            ]

            for col in cols_with_lists:
                data[col] = data[col].apply(
                    lambda x: str(x) if isinstance(x, list) else x
                )

            data = data.drop_duplicates()
            sendToTable(data, file, session, service)

    if session:
        session.close()
        print("Database connection closed.")


Main()

import datetime


def GetFileType(fileName: str):
    return fileName.split(".")[-1]


def WriteLog(service, log_folder_id, file: str, message: str):
    from utils.driveHelper import upload_log

    date = datetime.datetime.now().strftime("%Y_%d_%w_%H_%M_%S")
    filename = file.split(".")[0]
    log_name = f"{date}_{filename}.log"

    upload_log(service, log_folder_id, log_name, message)

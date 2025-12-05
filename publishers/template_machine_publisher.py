import os
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

MASTER_FOLDER = "12mvSBr6Z-tAUQgwIO2LBZegP20eGAYh9"

def get_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def ensure_folder(drive, parent_id, name):
    query = f"'{parent_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder' and title='{name}'"
    file_list = drive.ListFile({'q': query}).GetList()
    if file_list:
        return file_list[0]['id']

    folder = drive.CreateFile({
        'title': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': parent_id}]
    })
    folder.Upload()
    return folder['id']

def save_template_machine(title, json_data):
    drive = get_drive()

    today = datetime.datetime.now()
    month_name = today.strftime("%B %Y")

    month_folder = ensure_folder(drive, MASTER_FOLDER, month_name)
    stream_folder = ensure_folder(drive, month_folder, "template_machine")

    filename = f"{title}.json"
    file_path = f"/tmp/{filename}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_data)

    file = drive.CreateFile({
        'title': filename,
        'parents': [{'id': stream_folder}]
    })
    file.SetContentFile(file_path)
    file.Upload()

    return file['id']

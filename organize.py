import os
import sys
import shutil
import mimetypes
from pathlib import Path
from datetime import datetime
from send2trash import send2trash

to_scan = '/home/luan/CellLuan'
destination = '/home/luan/Organizados'
path_to_scan = Path(to_scan)
destination_path = Path(destination)

if to_scan in destination:
    sys.exit()

files = [item for item in path_to_scan.rglob("*") if item.is_file()]

for file in files: 
    mime_type, _ = mimetypes.guess_type(file)
    destination_folder_name = 'Outros'

    if type(mime_type) == str:
        destination_folder_name = mime_type.split('/')[-1]

    destination_folder_path = os.path.join(path_to_scan, destination_folder_name)
    _, file_and_ext = os.path.split(file)
    new_file_destination = os.path.join(destination_folder_path, file_and_ext)

    if os.path.exists(new_file_destination):
        if os.stat(file).st_size == os.stat(new_file_destination).st_size:
            send2trash(str(file))
        else:
            now = datetime.now()
            date_time = now.strftime('%Y%m%d') + str(now.microsecond)
            filename, ext = os.path.splitext(file_and_ext)
            shutil.move(file, os.path.join(destination_folder_path, filename + date_time + ext))
    else:
        print(f"[*] Movendo {file} para {destination_folder_name}")
        shutil.move(file, new_file_destination)


def remove_empty_directories(root):
    for dirpath, dirnames, filenames in os.walk(root):
        if not filenames and not dirnames:
            os.rmdir(dirpath)

remove_empty_directories(path_to_scan)
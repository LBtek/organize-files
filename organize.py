import os
import sys
import shutil
import mimetypes
import subprocess
from pathlib import Path
from datetime import datetime
from send2trash import send2trash

extensions = {
    "jpg": "imagens",
    "jpeg": "imagens",
    "png": "imagens",
    "ico": "imagens",
    "svg": "imagens",
    "webp": "imagens",
    "svg+xml": "imagens",
    "gif": "gifs",
    "pdf": "pdf",
    "docx": "textos",
    "document": "textos",
    "plain": "textos",
    "txt": "textos",
    "rtf": "textos",
    "epub+zip": "epub",
    "epub": "epub",
    "otf": "fontes",
    "tff": "fontes",
    "woff": "fontes",
    "woff2": "fontes",
    "mp3": "audio",
    "wav": "audio",
    "mp4": "vídeo",
    "m3u8": "vídeo",
    "webm": "vídeo",
    "mts": "vídeo",
    "xlsx": "planilhas",
    "rar": "compactados",
    "zip": "compactados",
    "gz": "compactados",
    "tar": "compactados",
    "pptx": "apresentações",
    "ppt": "apresentações",
    "presentation": "apresentações",
    "csv": "planilhas",
    "sheet": "planilhas",
    "exe": "programas",
    "msi": "programas",
    "apk": "apk",
    "torrent": "torrent",
    "x-iso9660-image": "iso",
}

to_scan = '/home/luan/CellLuan'
destination = '/home/luan/Organizados'
path_to_scan = Path(to_scan)
destination_path = Path(destination)

if to_scan in destination:
    sys.exit()

for dirpath, dirnames, filenames in os.walk(path_to_scan):
    for dirname in dirnames:
        name = str(dirname)
        if name == 'node_modules' or name == 'vendor' or name == '.gradle' or name == '.m2':
            shutil.rmtree(os.path.join(dirpath, dirname))

def cleaning(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        if not filenames and not dirnames:
            shutil.rmtree(dirpath)

cleaning(path_to_scan)

files = [item for item in path_to_scan.rglob("*") if item.is_file()]

if os.path.isdir(destination_path):
    cleaning(destination_path)
    subprocess.run(['chmod', '-R', '777', str(destination_path)])
elif files:
    subprocess.run(['chmod', '-R', '777', str(path_to_scan)])
    folder_name = destination.split('/')[-1]
    print(f"[+] Making {folder_name} folder")
    os.makedirs(destination_path)

for file in files: 
    mime_type, _ = mimetypes.guess_type(file)
    destination_folder_name = 'Outros'

    if type(mime_type) == str:
        destination_folder_name = mime_type.split('/')[-1].split('.')[-1]
    
    if not extensions.get(destination_folder_name):
        continue
    else:
        destination_folder_name = os.path.join(extensions.get(destination_folder_name), destination_folder_name)

    destination_folder_path = os.path.join(destination_path, destination_folder_name)
    base_file_path, file_and_ext = os.path.split(file)
    new_file_destination = os.path.join(destination_folder_path, file_and_ext)

    if os.path.exists(new_file_destination):
        if os.stat(file).st_size == os.stat(new_file_destination).st_size:
            os.environ.pop('GTK_USE_PORTAL', None)
            send2trash(file)
        else:
            now = datetime.now()
            date_time = now.strftime('%Y%m%d') + str(now.microsecond)
            filename, ext = os.path.splitext(file_and_ext)
            shutil.move(file, os.path.join(destination_folder_path, filename + date_time + ext))
    else:
        if not os.path.isdir(destination_folder_path):
            print(f"[+] Making {destination_folder_name} folder")
            os.makedirs(destination_folder_path)

        print(f"[*] Movendo {file} para {destination_folder_name}")
        shutil.move(file, new_file_destination)

cleaning(path_to_scan)

others_folder_path = os.path.join(destination_path, 'Outros')

for dirpath, dirnames, filenames in os.walk(path_to_scan):
    if dirnames:
        for dirname in dirnames:
            shutil.move(os.path.join(dirpath, dirname), others_folder_path)
    if filenames:
        for filename in filenames:
            shutil.move(os.path.join(dirpath, filename), others_folder_path)

    cleaning(dirpath)

cleaning(destination_path)
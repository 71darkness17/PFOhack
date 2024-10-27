from webapp import ALLOWED_EXTENSIONS

import zipfile
import os
import shutil

def clear_directory(path):
	"""
	очиска директории
	"""
	for item in os.listdir(path):
		file_path = os.path.join(path, item)
		if os.path.isfile(file_path):
			os.remove(file_path)
		elif os.path.isdir(file_path):
			shutil.rmtree(file_path, ignore_errors=True)

def unpack_zipfile(filename, extract_dir, encoding='cp437'):
    with zipfile.ZipFile(filename) as archive:
        for entry in archive.infolist():
            name = entry.filename.encode('cp437').decode(encoding)  # reencode!!!

            # don't extract absolute paths or ones with .. in them
            if name.startswith('/') or '..' in name:
                continue

            target = os.path.join(extract_dir, *name.split('/'))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if not entry.is_dir():  # file
                with archive.open(entry) as source, open(target, 'wb') as dest:
                    shutil.copyfileobj(source, dest)


def allowed_file(filename):
	"""
	Функция проверки расширения файла
	"""
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
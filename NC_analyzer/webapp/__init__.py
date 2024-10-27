from flask import Flask
import webbrowser

# Создаем экземпляр приложения
app = Flask(__name__)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'uploads/'
WORK_FOLDER = 'meta/'

# Расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'zip'}

import webapp.methods

# Конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
webbrowser.open_new('http://127.0.0.1:5000')
app.run()
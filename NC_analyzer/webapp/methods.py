from webapp import app, WORK_FOLDER, UPLOAD_FOLDER
import webapp.tools as tools

import model as md

import os

from flask import request, render_template, url_for, flash, redirect
from werkzeug.utils import secure_filename


regions = [
	{"name": "Владимирская область", "id": "33"},
	{"name": "Кировская область", "id": "43"},
	{"name": "Нижегородская область", "id": "52"},
	{"name": "Республика Марий Эл", "id": "12"},
	{"name": "Республика Мордовия", "id": "13"},
	{"name": "Республика Татарстан", "id": "16"},
	{"name": "Удмуртская Республика", "id": "18"},
	{"name": "Чувашская Республика", "id": "21"},
]

reg = "0"


@app.route('/res', methods=["GET"])
def s():
	"""
	функция для страницы с результатом
	"""

	if reg == "0":
		data = md.main()
	else:
		data = [i for i in md.main() if str(i[2]) == reg]
	print(data)
	print(reg)
	return render_template("result.html", css=url_for('static', filename='styles.css'), data=data, dlen=len(data))


@app.route('/t', methods=['GET', 'POST'])
def t():
	"""
	функция для страницы с определением региона
	"""
	global reg
	if request.method == "POST":
		selected_value = request.json.get('selectedValue')
		print(selected_value)
		reg = str(selected_value)
		print("changed is {}".format(reg))
		return redirect(url_for('s'))
	return render_template("result2.html", css=url_for('static', filename='styles2.css'), regions=regions)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
	"""
	функция для главной страницы
	"""
	if request.method == 'POST':
		# подготовка рабочей директории
		tools.clear_directory(WORK_FOLDER)
				
		if 'file' not in request.files:
			# После перенаправления на страницу загрузки
			# покажем сообщение пользователю 
			flash('Не могу прочитать файл')
			return redirect(request.url)

		file = request.files['file']
		# Если файл не выбран, то браузер может
		# отправить пустой файл без имени.
		if file.filename == '':
			flash('Нет выбранного файла')
			return redirect(request.url)

		if file and tools.allowed_file(file.filename):
			# безопасно извлекаем оригинальное имя файла
			filename = secure_filename(file.filename)
			# сохраняем файл
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], "1.zip"))
			tools.unpack_zipfile('uploads/1.zip', r'meta', encoding='cp866') # распаковка вводных данных
			# если все прошло успешно, то перенаправляем на страницу с результатом

			return redirect(url_for('t'))
			
	return render_template("index.html", css=url_for('static', filename='styles2.css'))
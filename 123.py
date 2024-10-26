import pyexcel as p
import json

# Загрузка данных из Excel
file_path = 'table1.xls'  # Укажите путь к вашему файлу
excel_data = p.get_records(file_name=file_path)

# Парсинг данных в словарь с учетом одинаковых ID
result = {}
for row in excel_data:
    print(row)
    id_value = row.pop('ID')  # Извлекаем ID как ключ
    if id_value not in result:
        result[id_value] = []
    if row not in result[id_value]:  # Проверяем на уникальность значений
        for item in row.values():
            result[id_value].append(item)


# Сохранение в JSON-файл
json_file_path = 'output.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)

print(f'Данные успешно сохранены в {json_file_path}')

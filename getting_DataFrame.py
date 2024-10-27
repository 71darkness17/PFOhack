import pandas as pd
from pypdf import PdfReader
from docx import Document
import glob
import os
from pandas.core.interchange.dataframe_protocol import DataFrame

# Читаем данные из кокнретного файла и возвращаем DataFrame объект
def read_data(file_path):
    if file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.pdf'):
        return read_pdf(file_path)
    elif file_path.endswith('.docx'):
        return read_docx(file_path)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    else:
        raise ValueError('Unsupported file format')

# Читаем данные из pdf-файла и преобразуем их в DataFrame
def read_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
    return pd.DataFrame([line.split() for line in text.splitlines()])

# Читаем данные из docx-файла и преобразуем их в DataFrame
def read_docx(file_path):
    doc = Document(file_path)
    text = '\n'.join([p.text for p in doc.paragraphs])
    return pd.DataFrame([line.split() for line in text.splitlines()])

# Объединяем данные из всех считанных файлов в один DataFrame
def load_all_data(directory):
    all_data = []
    print('Файлы в директории:')
    print(os.listdir(directory))
    for file in glob.glob(f'{directory}/*'):
        try:
            data = read_data(file)
            all_data.append(data)
            print(f'Загружен файл: {file}, размер: {data.shape}')
        except Exception as e:
            print(f'Ошибка при загрузке файла {file}: {e}')
    if not all_data:
        print('Нет данных для объединения')
    return pd.concat(all_data, ignore_index = True) if all_data else pd.DataFrame()

def convert_date(date):
    year, month = date.split('/')
    date = f'01.{month}.{year}'
    date = (pd.to_datetime('now') - pd.to_datetime(date)).days
    return date

def avrg(data):
    return sum(data) / len(data) if len(data) != 0 else 0

# Получаем всю информацию по конкретному клиенту из DataFrame
def get_client_data(data, client_id):
    client_data = data[data['client_id'] == client_id]
    if client_data.empty:
        raise ValueError(f'Клиент с ID {client_id} не найден')
    return client_data

# Вычисляем вес (вероятность прекращения пользования услугами) конкретного клиента
def get_client_weight(rf_model, feature_extractor, client_data):
    client_features = client_data.drop(columns = ['client_id', 'target', 'regions'], errors = 'ignore')
    neural_features = feature_extractor.predict(client_features)
    weight = rf_model.predict_proba(neural_features)[:, 1][0] * 100
    return weight

def sorting(clients: list, df: DataFrame):
    df.index = df['client_id']
    avg = 0
    summ = 0
    cnt = 0
    rows = [df.iloc[i] for i in range(len(df['client_id']))]
    for row in rows:
        if row['capital_size']!=0:
            summ += row['capital_size']
            cnt += 1
    avg = summ / cnt
    sorted_clients = []
    for id in df['client_id']:
        for client in clients:
            if client[0] == id:
                cur_client = client
        current = df['capital_size'].loc[id]
        capital_procent = (current - avg) / avg * 100
        common_procent = (capital_procent + cur_client[1][0]) / 2
        sorted_clients.append((id, common_procent, cur_client[1][2], cur_client[1][3]))
    sorted_clients.sort(lambda x: (x[1], x[0]))
    return sorted_clients
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from pypdf import PdfReader
# from docx import Document
import glob
import os
import numpy

def read_data(file_path):
    if file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.pdf'):
        return read_pdf(file_path)
    # elif file_path.endswith('.docx'):
    #     return read_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

def read_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return pd.DataFrame([line.split() for line in text.splitlines()])  # Уточните структуру

# def read_docx(file_path):
#     doc = Document(file_path)
#     text = "\n".join([p.text for p in doc.paragraphs])
#     return pd.DataFrame([line.split() for line in text.splitlines()])  # Уточните структуру
def marketing_list(id: int,path: str) -> (list,list):
    df = pd.read_excel(path).drop(columns=['Находится в реестре МСП', 'ОКВЭД2.Наименование', 'ОКВЭД2.Код','Город фактический',
                                       'Город юридический','Грузоотправитель','Грузополучатель',
                                       'Карточка клиента (внешний источник).Индекс платежной дисциплины Описание',
                                       'Карточка клиента (внешний источник).Индекс финансового риска Описание',
                                       'Госконтракты.Контракт','Госконтракты.Тип контракта'], errors='ignore')
    res = []
    rows = [df.iloc[i] for i in range(len(df['ID']))]
    for row in rows:
        if row.iloc[0] == id:
            for i in range(1, len(row)):
                res = row
                break
    res_col = df.columns
    ans = []
    for i in range(len(res)):
        ans.append(res.iloc[i])
    return ans, list(df.columns.values)
def transition_value(id: int,path: str) -> (list,list):
    df = pd.read_excel(path, skiprows=2).drop(columns=['Субъект федерации отп','Субъект федерации наз',
                                                       'Код груза','Гр груза по опер.номен'], errors='ignore')
    rows = [df.iloc[i] for i in range(len(df['ID']))]
    for row in rows:
        break
        # if row.iloc[0] == id:
        #     for i in range(1,len(row)):
        #         pass
    return [],[]
def requests(id: int, path: str) -> (list,list):
    df = pd.read_excel(path).drop(columns=['Дата','Тема','Номер','Тип обращения','Группа вопросов','Количество доработок'], errors='ignore')
    rows = [df.iloc[i] for i in range(len(df['ID']))]
    reports = 0
    for row in rows:
        if row.iloc[0] == id and row.iloc[1] == 'Жалобы':
            reports+=1
    l = [reports]
    return l, ['reports_amount']
def interests(id: int, path: str):
    df = pd.read_excel(path).drop(columns=['Дата','Тема','Сценарий','Подразделение','Ожидаемая выручка','Вероятность сделки, %','Дата следующей активности',
                                          'Следующая активность','Канал первичного интереса','Номер',
                                           'Ссылка (служебное поле для вывода на экран прочих реквизитов объекта)'], errors='ignore')
    res_dict = {
        'Завершен неудачно': 0,
        'Завершен успешно': 0,
        'Регистрация клиента на "РЖД Маркет"': 0,
        'Отказ в работе': 0,
        'Раз. предложения\Офор.заказа на "РЖД Маркет"': 0
    }
    rows = [df.iloc[i] for i in range(len(df['ID']))]
    for row in rows:
        if row.iloc[1] == id:
            if row.iloc[0] in res_dict.keys():
                res_dict[row.iloc[0]]+=1
    return res_dict.values(), ['fail','success','registration','denied','once_offer']
def create_dataset(paths: list) -> pd.DataFrame:
    id_table = pd.read_excel(paths[-1])
    ids = [i for i in id_table['ID']]
    predataset = list()
    columns1 = list()
    columns = list()
    j = 0
    for id in ids[847:848]:
        temp = []
        g = 8
        for i in range(len(paths)-1):
            if i<g:
                temp1, ctemp = marketing_list(id,paths[i])
                temp+=temp1
                if len(temp1)>0:
                    columns1+=ctemp
                    g = 0
            elif i == 8:
                temp1, ctemp = interests(id,paths[i])
                temp += temp1
                columns1 += ctemp
            elif i == 9:
                temp1, ctemp = requests(id,paths[i])
                temp += temp1
                columns1 += ctemp
            elif i == 10:
                temp1, ctemp = transition_value(id,paths[i])
                temp += temp1
                columns1 += ctemp
        predataset.append(temp)
        if j == 0:
            columns=columns1
            j+=1

    try:
        dataset = pd.DataFrame(data=predataset, columns=columns)
    except ValueError:
        print(len(columns), len(predataset[0]))
        dataset = []
    return dataset

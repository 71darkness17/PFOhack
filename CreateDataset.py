from concurrent.futures.thread import ThreadPoolExecutor

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from pypdf import PdfReader
# from docx import Document
import glob
import os
import numpy
import threading
from concurrent.futures import ThreadPoolExecutor
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
def change_the_data(typev: int,value):
    if type(value) == str:
        value = value.replace(' ', '')
    match value:
        case 'Микробизнес':
            return 0
        case 'Малыйбизнес':
            return 1
        case 'Среднийбизнес':
            return 2
        case 'Крупныйбизнес':
            return 3
        case None:
            return 0
        case '':
            return 0
        case _:
            if typev == 4:
                return 1
                # except TypeError:
                #     value = value.replace(' ', '#')
                #     assert 1==2, f'len: {len(value)} type: {typev} value: {value}'
            else:
                return value

def marketing_list(id: int,df: DataFrame) -> (list,list):
    # df = pd.read_excel(path).drop(columns=['Находится в реестре МСП', 'ОКВЭД2.Наименование', 'ОКВЭД2.Код','Город фактический',
    #                                    'Город юридический','Грузоотправитель','Грузополучатель',
    #                                    'Карточка клиента (внешний источник).Индекс платежной дисциплины Описание',
    #                                    'Карточка клиента (внешний источник).Индекс финансового риска Описание',
    #                                    'Госконтракты.Контракт','Госконтракты.Тип контракта'], errors='ignore').fillna(0)
    res = []
    rows = [df.iloc[i].to_list() for i in range(len(df['ID']))]
    for row in rows:
        if row[0] == id:
            for i in range(len(row)):
                row[i] = change_the_data(i,row[i])
            res = row

            #print(res)
            break
    if len(res) > 0:
        cols = ['ID', 'company_size', 'capital_size', 'emp_amount', 'is_els', 'payment_index','risk_index']
    else:
        cols = []
    return res,cols
def transition_value(id: int,df: DataFrame) -> (list,list):
    # df = pd.read_excel(path, skiprows=2).drop(columns=['Субъект федерации отп','Субъект федерации наз',
    #                                                    'Код груза','Гр груза по опер.номен'], errors='ignore')
    rows = [df.iloc[i] for i in range(len(df['ID']))]
    for row in rows:
        break
        # if row.iloc[0] == id:
        #     for i in range(1,len(row)):
        #         pass
    return [],[]
def requests(id: int, df: DataFrame) -> (list,list):
    # df = pd.read_excel(path).drop(columns=['Дата','Тема','Номер','Тип обращения','Группа вопросов','Количество доработок'], errors='ignore')
    rows = [df.iloc[i].to_list() for i in range(len(df['ID']))]
    reports = 0
    for row in rows:
        if row[0] == id and row[1] == 'Жалобы':
            reports+=1
    l = [reports]
    return l, ['reports_amount']
def interests(id: int, df: DataFrame):
    # df = pd.read_excel(path).drop(columns=['Дата','Тема','Сценарий','Подразделение','Ожидаемая выручка','Вероятность сделки, %','Дата следующей активности',
    #                                       'Следующая активность','Канал первичного интереса','Номер',
    #                                        'Ссылка (служебное поле для вывода на экран прочих реквизитов объекта)'], errors='ignore')
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
    return list(res_dict.values()), ['fail','success','registration','denied','once_offer']
def target(id: int, df: DataFrame) -> (list,list):
    #print(df)
    rows = [df.iloc[i].to_list() for i in range(len(df['ID']))]
    targ = 1
    ischoosed = False
    for row in rows:
        if row[0] == id:
            targ = row[1]
            ischoosed = True
        elif ischoosed:
            break
    if ischoosed:
        return [targ], ['target']
    else:
        return [0],['target']
# def task1(id_table: DataFrame, tables: list,paths: list, is_for_train: bool) -> (list,list):
#     predataset = list()
#     columns1 = list()
#     columns = list()
#     ids = [i for i in id_table['ID']]
#     j = True
#     end = False
#     for id in range(0, 100 , 3):
#         temp = []
#         if len(columns)>0:
#             j = False
#         end = False
#         for i in range(len(tables)):
#             if i<8 and not end:
#                 temp1, ctemp = marketing_list(ids[id],tables[i])
#
#                 if i == 0:
#                     temp+=temp1
#                     print(temp1)
#                 elif len(temp1)>0:
#                     temp = temp1
#                     print(temp1)
#                 if not 'ID' in columns1:
#                     columns1+=ctemp
#                 if len(temp)>0 and temp[1] != 0:
#                     end = True
#
#             elif i == 8:
#                 temp1, ctemp = interests(ids[id],tables[i])
#                 temp += temp1
#                 if not ctemp[0] in columns1:
#                     columns1 += ctemp
#             elif i == 9:
#                 temp1, ctemp = requests(ids[id],tables[i])
#                 temp += temp1
#                 if not ctemp[0] in columns1:
#                     columns1 += ctemp
#             # elif i == 10:
#             #     temp1, ctemp = transition_value(ids[id],tables[i])
#             #     temp += temp1
#             #     if not ctemp[0] in columns1:
#             #         columns1 += ctemp
#             elif is_for_train and i == 11:
#                 temp1, ctemp = target(ids[id], tables[i])
#                 temp += temp1
#                 if not ctemp[0] in columns1:
#                     columns1 += ctemp
#         predataset.append(temp)
#         columns=columns1
#     return predataset, columns
# def task2(id_table: DataFrame, tables: list,paths: list, is_for_train: bool) -> list:
#     predataset = list()
#     ids = [i for i in id_table['ID']]
#     j = True
#     end = False
#     for id in range(1, 100, 3):
#         temp = []
#         end = False
#         for i in range(len(tables)):
#             if i<8 and not end:
#                 temp1, ctemp = marketing_list(ids[id],tables[i])
#
#                 if i == 0:
#                     temp+=temp1
#                     print(temp1)
#                 elif len(temp1)>0:
#                     temp = temp1
#                     print(temp1)
#                 if len(temp)>0 and temp[1] != 0:
#                     end = True
#
#             elif i == 8:
#                 temp1, ctemp = interests(ids[id],tables[i])
#                 temp += temp1
#             elif i == 9:
#                 temp1, ctemp = requests(ids[id],tables[i])
#                 temp += temp1
#             # elif i == 10:
#             #     temp1, ctemp = transition_value(ids[id],tables[i])
#             #     temp += temp1
#             #     if not ctemp[0] in columns1:
#             #         columns1 += ctemp
#             elif is_for_train and i == 11:
#                 temp1, ctemp = target(ids[id], tables[i])
#                 temp += temp1
#         print('.')
#         predataset.append(temp)
#     return predataset
# def task3(id_table: DataFrame, tables: list,paths: list, is_for_train: bool) -> list:
#     predataset = list()
#     ids = [i for i in id_table['ID']]
#     j = True
#     end = False
#     for id in range(2, 100 , 3):
#         temp = []
#         end = False
#         for i in range(len(tables)):
#             if i<8 and not end:
#                 temp1, ctemp = marketing_list(ids[id],tables[i])
#
#                 if i == 0:
#                     temp+=temp1
#                     print(temp1)
#                 elif len(temp1)>0:
#                     temp = temp1
#                     print(temp1)
#                 if len(temp)>0 and temp[1] != 0:
#                     end = True
#
#             elif i == 8:
#                 temp1, ctemp = interests(ids[id],tables[i])
#                 temp += temp1
#             elif i == 9:
#                 temp1, ctemp = requests(ids[id],tables[i])
#                 temp += temp1
#             # elif i == 10:
#             #     temp1, ctemp = transition_value(ids[id],tables[i])
#             #     temp += temp1
#             #     if not ctemp[0] in columns1:
#             #         columns1 += ctemp
#             elif is_for_train and i == 11:
#                 temp1, ctemp = target(ids[id], tables[i])
#                 temp += temp1
#         predataset.append(temp)
#     return predataset
def create_dataset(paths: list, output: str, is_for_train: bool):
    id_table = pd.read_excel(paths[-1])
    tables = list()
    for i in range(8):
        tables.append(pd.read_excel(paths[i]).drop(columns=['Находится в реестре МСП', 'ОКВЭД2.Наименование', 'ОКВЭД2.Код','Город фактический',
                                       'Город юридический','Грузоотправитель','Грузополучатель',
                                       'Карточка клиента (внешний источник).Индекс платежной дисциплины Описание',
                                       'Карточка клиента (внешний источник).Индекс финансового риска Описание',
                                       'Госконтракты.Контракт','Госконтракты.Тип контракта'], errors='ignore').fillna(0))
    tables.append(pd.read_excel(paths[8]).drop(columns=['Дата','Тема','Сценарий','Подразделение','Ожидаемая выручка','Вероятность сделки, %','Дата следующей активности',
                                          'Следующая активность','Канал первичного интереса','Номер',
                                           'Ссылка (служебное поле для вывода на экран прочих реквизитов объекта)'], errors='ignore'))
    tables.append(pd.read_excel(paths[9]).drop(columns=['Дата','Тема','Номер','Тип обращения','Группа вопросов','Количество доработок'], errors='ignore'))
    tables.append(pd.read_excel(paths[10], skiprows=2).drop(columns=['Субъект федерации отп','Субъект федерации наз',
                                                       'Код груза','Гр груза по опер.номен'], errors='ignore'))
    if is_for_train:
        tables.append(pd.read_excel(paths[11]))
    #print(is_for_train,paths[11],tables[11])
    ids = [i for i in id_table['ID']]
    predataset = list()
    columns1 = list()
    columns = list()
    j = True
    end = False


    for id in range(len(ids)):
        temp = []
        if len(columns)>0:
            j = False
        end = False
        for i in range(len(tables)):
            if i<8 and not end:
                temp1, ctemp = marketing_list(ids[id],tables[i])

                if i == 0:
                    temp+=temp1
                    print(temp1)
                elif len(temp1)>0:
                    temp = temp1
                    print(temp1)
                if not 'ID' in columns1:
                    columns1+=ctemp
                if len(temp)>0 and temp[1] != 0:
                    end = True

            elif i == 8:
                temp1, ctemp = interests(ids[id],tables[i])
                temp += temp1
                if not ctemp[0] in columns1:
                    columns1 += ctemp
            elif i == 9:
                temp1, ctemp = requests(ids[id],tables[i])
                temp += temp1
                if not ctemp[0] in columns1:
                    columns1 += ctemp
            # elif i == 10:
            #     temp1, ctemp = transition_value(ids[id],tables[i])
            #     temp += temp1
            #     if not ctemp[0] in columns1:
            #         columns1 += ctemp
            elif is_for_train and i == 11:
                temp1, ctemp = target(ids[id], tables[i])
                temp += temp1
                if not ctemp[0] in columns1:
                    columns1 += ctemp
        predataset.append(temp)
        columns=columns1
    # with ThreadPoolExecutor() as executor:
    #     thread1 = executor.submit(task1,id_table,tables,paths,is_for_train)
    #     thread2 = executor.submit(task2,id_table,tables,paths,is_for_train)
    #     thread3 = executor.submit(task3,id_table,tables,paths,is_for_train)
    #     predataset, columns = thread1.result()
    #     predataset += thread2.result()
    #     predataset += thread3.result()
    for data in range(len(predataset)):
        assert len(predataset[data]) == len(columns), f'id: {data} | {len(predataset[data]),predataset[data], len(columns),columns}'
    try:
        dataset = pd.DataFrame(data=predataset, columns=columns)
    except ValueError:
        print(len(columns), len(predataset[0]))
        print(columns)
        print(predataset)
        dataset = pd.DataFrame(data=[], columns=[])
    dataset.to_csv(output)

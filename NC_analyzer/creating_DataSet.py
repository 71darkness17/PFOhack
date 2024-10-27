import multiprocessing
from multiprocessing import Pool
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from getting_DataFrame import convert_date, avrg
#
#
#           Создано в рамках Хакатона "Цифровой Прорыв: Сезон ИИ"
#                               NC Group
#
#

# Функция изменения некоторых входеных данных
def change_the_data(typev: int, value):
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
        case 'Владимирскаяобласть' :
            return '33'
        case 'Кировскаяобласть':
            return '43'
        case 'Нижегородскаяобласть':
            return '52'
        case 'РеспубликаМарийЭл':
            return '12'
        case 'РеспубликаМордовия':
            return '13'
        case 'РеспубликаТатарстан(Татарстан)':
            return '16'
        case 'УдмуртскаяРеспублика':
            return '18'
        case 'ЧувашскаяРеспублика-ЧавашРеспублики':
            return '21'
        case _:
            if typev == 4:
                return 1
            elif typev == 11:
                return ''
            else:
                return value

# Чтение таблицы маркетинговых списков
def marketing_list(id: int, df: DataFrame):
    res = []
    rows = [df.iloc[i].to_list() for i in range(len(df['ID']))]
    for row in rows:
        if row[0] == id:
            for i in range(len(row)):
                row[i] = change_the_data(i, row[i])
            res = row
            break
    if len(res) > 0:
        cols = ['ID', 'company_size', 'capital_size', 'emp_amount', 'is_els', 'payment_index', 'risk_index']
    else:
        cols = []
    return res, cols

def sorted_transitions(df: DataFrame):
    df.drop(df.columns[[1, 2, 3, 4]], axis = 1, inplace = True, errors = 'ignore')
    df.rename(columns = {x : y + str(i) for i, (x, y) in enumerate(zip(df.columns.to_list(), list(df.iloc[1])))}, inplace = True, errors = 'ignore')
    df.drop([f'Объем перевозок(тн){i}' for i in range(2, len(df.columns), 2)], axis = 1, inplace = True, errors = 'ignore')
    header = list(map(convert_date, df.iloc[0].fillna('1990/01')))
    header[0] = '0'
    df.drop([0, 1], axis = 0, inplace = True, errors = 'ignore')
    df.rename(columns = {x : y for x, y in zip(df.columns.to_list(), header)}, inplace = True, errors = 'ignore')
    df = df.reindex(sorted(df.columns, key = lambda x: int(x)), axis = 1)
    return df

def transition_list(id: int, df: DataFrame):
    rows = df[df['0'] == id]
    indexes = list(rows.index.values)
    avg, last6_dynamics, common_dynamics = [], [], []
    for i in indexes:
        row = rows.loc[i]
        trans_values = list(map(int, row))
        last6_dynamics.append(avrg(trans_values[:3]) - avrg(trans_values[3:6]))
        common_dynamics.append(avrg(trans_values[:6]) - avrg(trans_values))
        avg.append(avrg(trans_values))
    return [avrg(avg), avrg(last6_dynamics), avrg(common_dynamics)], ['Avg', 'Last6', 'Common']

# Чтение таблицы обращений
def requests(id: int, df: DataFrame):
    rows = [df.iloc[i].to_list() for i in range(len(df['ID']))]
    reports = 0
    for row in rows:
        if row[0] == id and row[1] == 'Жалобы':
            reports += 1
    l = [reports]
    return l, ['reports_amount']

# Чтение таблицы интересов
def interests(id: int, df: DataFrame):
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
                res_dict[row.iloc[0]] += 1
    return list(res_dict.values()), ['fail', 'success', 'registration', 'denied', 'once_offer']

# Чтение таблицы целевых значений(для обучения)
def target(id: int, df: DataFrame):
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
        return [0], ['target']

# Получение региона для id
def get_region(id: int, df: DataFrame):
    rows = [df.iloc[i].to_list() for i in range(len(df['ID']))]
    regs = ''
    is_def = False
    for row in rows:
        if row[0] == id:
            if not (change_the_data(11,row[1]) in regs):
                regs = regs+change_the_data(11, row[1])
                is_def = True
    if not is_def:
        regs = '-'
    return [regs], ['regions']

# Функция для каждого процесса формирования ДатаСета
def task2(id_table: DataFrame, tables: list, is_for_train: bool, proc, procs):
    predataset = list()
    ids = [i for i in id_table['ID']]
    end = False
    for id in range(proc, 99, procs):
        temp = []
        end = False
        for i in range(len(tables)):
            if i < 8 and not end:
                temp1 = marketing_list(ids[id],tables[i])[0]
                if i == 0:
                    temp += temp1
                elif len(temp1) > 0:
                    temp = temp1
                if len(temp) > 0 and temp[1] != 0:
                    end = True
            elif i == 8:
                temp1 = interests(ids[id],tables[i])[0]
                temp += temp1
            elif i == 9:
                temp1 = requests(ids[id],tables[i])[0]
                temp += temp1
            elif i == 10:
                temp1 = transition_list(ids[id], tables[i])[0]
                temp += temp1
            elif i == 11:
                temp1 = get_region(ids[id], tables[i])[0]
                temp += temp1
            elif is_for_train and i == 12:
                temp1 = target(ids[id], tables[i])[0]
                temp += temp1
        predataset.append(temp)
        print('.')
    return predataset

# Главная функция создания ДатаСета
def create_dataset(paths: list, output: str, is_for_train: bool):
    id_table = pd.read_excel(paths[-1])
    tables = list()

    # Загрузка таблиц в DataFrame
    for i in range(8):
        tables.append(pd.read_excel(paths[i]).drop(columns = ['Находится в реестре МСП', 'ОКВЭД2.Наименование', 'ОКВЭД2.Код', 'Город фактический',
                                       'Город юридический', 'Грузоотправитель', 'Грузополучатель',
                                       'Карточка клиента (внешний источник).Индекс платежной дисциплины Описание',
                                       'Карточка клиента (внешний источник).Индекс финансового риска Описание',
                                       'Госконтракты.Контракт','Госконтракты.Тип контракта'], errors = 'ignore').fillna(0))
    tables.append(pd.read_excel(paths[8]).drop(columns = ['Дата', 'Тема', 'Сценарий', 'Подразделение', 'Ожидаемая выручка', 'Вероятность сделки, %', 'Дата следующей активности',
                                          'Следующая активность','Канал первичного интереса','Номер',
                                           'Ссылка (служебное поле для вывода на экран прочих реквизитов объекта)'], errors = 'ignore'))
    tables.append(pd.read_excel(paths[9]).drop(columns = ['Дата', 'Тема', 'Номер', 'Тип обращения', 'Группа вопросов', 'Количество доработок'], errors = 'ignore'))
    tables.append(sorted_transitions(pd.read_excel(paths[10])))
    tables.append(pd.read_excel(paths[10],skiprows = 2))

    # Если для обучения, то загружаем целевые значения
    if is_for_train:
        tables.append(pd.read_excel(paths[11]))
    ids = [i for i in id_table['ID']]

    # Переменные временного хранения данных для ДатаСета
    predataset1 = list()
    predataset = list()
    columns1 = list()
    columns = list()
    end = False

    # Получение возможного количества процессов
    n_proc = multiprocessing.cpu_count()

    # Приведение количества процессов к стандартному значению
    if n_proc >= 10:
        n_proc = 10
    elif n_proc >= 5:
        n_proc = 5
    elif n_proc >= 2:
        n_proc = 2

    # Создание менеджера процессов, запуск форматирования данных для ДатаСета
    with Pool(n_proc) as p:
        predataset1 = p.starmap(task2, [(id_table, tables, is_for_train, proc, n_proc) for proc in range(n_proc)])

    # Превращение в нужный формат
    for data in predataset1:
        predataset += data

    # Получение списка названия столбцов
    temp = list()
    for i in range(len(tables)):
        if i < 8 and not end:
            temp1, ctemp = marketing_list(ids[0], tables[i])
            if i == 0:
                temp += temp1
            elif len(temp1) > 0:
                temp = temp1
            if not 'ID' in columns1:
                columns1 += ctemp
            if len(temp) > 0 and temp[1] != 0:
                end = True
        elif i == 8:
            temp1, ctemp = interests(ids[0], tables[i])
            temp += temp1
            if not ctemp[0] in columns1:
                columns1 += ctemp
        elif i == 9:
            temp1, ctemp = requests(ids[0], tables[i])
            temp += temp1
            if not ctemp[0] in columns1:
                columns1 += ctemp
        elif i == 10:
            temp1, ctemp = transition_list(ids[0], tables[i])
            temp += temp1
            if not ctemp[0] in columns1:
                columns1 += ctemp
        elif i == 11:
            temp1, ctemp = get_region(ids[0], tables[i])
            temp += temp1
            if not ctemp[0] in columns1:
                columns1 += ctemp
        elif is_for_train and i == 12:
            temp1, ctemp = target(ids[0], tables[i])
            temp += temp1
            if not ctemp[0] in columns1:
                columns1 += ctemp
    columns = ['client_id'] + columns1[1:]

    #Проверка на несовпадения количества столбцов и количества значений в строках
    for data in range(len(predataset)):
        assert len(predataset[data]) == len(columns), f'id: {data} | {len(predataset[data]), predataset[data], len(columns), columns}'

    # Создание и сохранение данных для дальнейшей обработки
    dataset = pd.DataFrame(data = predataset, columns = columns)
    dataset.to_csv(output)
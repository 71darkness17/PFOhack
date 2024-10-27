from operator import index
from numpy.ma.extras import average
from pandas.core.interchange.dataframe_protocol import DataFrame

# Находим среднее значение данных в заданном столбце
def find_avg(df: DataFrame, col) -> float:
    sum = 0
    cnt = 0
    for i in df[col].values:
        sum += i
        cnt += 1
    return sum / cnt

def compare(df: DataFrame, col, id):
    current = df.loc[df['client_id'] == id, col].values[0]
    average = find_avg(df, col)
    diff = average - current
    return diff

def prepare_data(df: DataFrame):
    df.index = [str(i) for i in df['client_id']]
    return df

def find_mostly_important(maxk):
    match maxk:
        case 'is_els':
            return 'Этот пользователь никогда не имел дел с РЖД; возможно, пора его привлечь'
        case 'reports_amount':
            return 'Вам следует обратить внимание на жалобы данного клиента'
        case 'payment_index':
            return 'У этого клиента высока вероятность просрочить платежи'
        case 'fail':
            return 'С этим клиентом многие сделки завершились неудачно'
        case 'denied':
            return 'Этот клиент получил много отказов в работе'

def make_recomendation(df: DataFrame, id):
    diffs = {}
    for colmn in ['is_els', 'reports_amount', 'payment_index', 'fail', 'denied']:
        diffs[colmn] = compare(df, colmn, id)
    maxvl = max(diffs.values())
    for k, v in zip(diffs.keys(), diffs.values()):
        if v == maxvl:
            maxk = k
    return find_mostly_important(maxk)
from pickle import load
import os
try:
    from getting_DataFrame import *
    from creating_DataSet import *
    from recomendations import make_recomendation
except ImportError:
    os.system('pip install --upgrade pip > nul')
    os.system('pip install pandas click lxml xlrd openpyxl python-docx pypdf scikit-learn tensorflow > nul')
    os.system('cls')

def main():
    '''paths = []
    paths.extend(list(glob.glob("meta//Выгрузка_маркетинговые списки//*")))
    paths.extend(list(glob.glob("meta//Выгрузки_интересы+обращения+объёмы перевозок//*")))
    paths.extend(list(glob.glob("meta//Привязка ID.xlsx")))
    create_dataset(paths, 'test_input//dataset.csv', 0)'''
    data = load_all_data('test_input')
    feature_extractor, rf_model = load(open('dndt_model.sav', 'rb'))[1:]
    client_weights = {}
    for client_id in data['client_id'].unique():
        client_data = get_client_data(data, client_id)
        weight = get_client_weight(rf_model, feature_extractor, client_data)
        region  = str(client_data['regions'])
        recomendation = make_recomendation(data, client_id)
        client_weights[client_id] = (weight, region, recomendation)
    print("Ранжированный список клиентов:", sorting(client_weights.items(), data))

if __name__ == "__main__":
    main()
import CreateDataset
from CreateDataset import create_dataset
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from pypdf import PdfReader
# from docx import Document
import glob
import os

paths = ['РЖДtrain/1/1.xls','РЖДtrain/1/2.xls','РЖДtrain/1/3.xls','РЖДtrain/1/4.xls','РЖДtrain/1/5.xls','РЖДtrain/1/6.xls',
         'РЖДtrain/1/7.xls','РЖДtrain/1/8.xls','РЖДtrain/2/1.xls','РЖДtrain/2/2.xls','РЖДtrain/2/3.xls','РЖДtrain/1.xlsx',]
create_dataset(paths,'output.csv')
ds = pd.read_csv('output.csv')
spaces = []
for column in ds.columns.values[1:]:
    spaces.append(len(column)+2)
    print(column,end="  ")
print('')
for i in range(3):
    for column, space in zip(ds.columns[1:],spaces):
        print(ds[column].iloc[i],end=' '*(space - len(str(ds[column][i]))))
    print('')
# print(ds)
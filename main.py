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
ds = create_dataset(paths)
for column in ds.columns.values:
    print(column,end="\t")
print('')
for column in ds.columns:
    print(ds[column][0],end="\t")
#print(ds)
import pandas as pd
import re
import os
import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()
file_path = filedialog.askdirectory(parent=root,
                                    initialdir="/",
                                    title='Please select a directory')
file_list=os.listdir(file_path)
file_list_py = [file for file in file_list]

df = pd.DataFrame()
data = pd.DataFrame()
for i in file_list_py:
    data_path=file_path + "/"+ i
    data_pa=pd.read_csv(data_path, delimiter='\n')
    new_columns=data_pa.iloc[0,0]
    new_columns=re.sub("Source 1:","",new_columns)
    data=data_pa.rename(columns={"Sample Rate: 250.0000":new_columns})
    data=data.drop(index=[0])
    df=pd.concat([df, data], axis=1)
df=df.reset_index(drop=True)
Brain_waves=df.dropna(axis=0)
Brain_waves
csv_path = filedialog.askdirectory(parent=root,
                                    initialdir="/",
                                    title='Please select a directory')
csv_path = csv_path + '/Brain_waves.csv'
Brain_waves.to_csv(csv_path, index=False)

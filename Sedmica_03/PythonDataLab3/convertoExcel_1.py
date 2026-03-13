

import pandas as pd
import openpyxl


read_file = pd.read_excel(r"C:\Users\korisnik\Downloads\Test.xlsx")

read_file.to_csv("Test.csv", index=None, header=True)

df = pd.DataFrame(pd.read_csv("Test.csv"))
print(df)
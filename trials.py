import numpy as np
import pandas as pd

df = pd.read_csv("sample.txt", sep = "\t")
df['Timestamp'] = pd.to_datetime(df['Open time'], unit = 'ms')
data = df[['Timestamp', 'Close']]

result = 6938.17 * 0.2510734011859392

print(result)
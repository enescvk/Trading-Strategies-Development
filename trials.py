import numpy as np
import pandas as pd

df = pd.read_csv("sample.txt", sep = "\t")
df['Timestamp'] = pd.to_datetime(df['Open time'], unit = 'ms')
data = df[['Timestamp', 'Close']]

print(data[data['Timestamp'] == "2019-09-20 03:05:00"])

dictlist = [{'type': 'buy', 'position_type': 'long', 'price': 10209.81, 'quantity': 0.09794501562712725, 'wallet_balance': 0.0, 'timestamp': '2019-08-18 09:29:00'}, {'type': 'sell', 'position_type': 'long', 'price': 10677.77, 'quantity': 0.09794501562712725, 'wallet_balance': 1045.8343495128706, 'timestamp': '2019-08-19 07:14:00'}, {'type': 'sell', 'position_type': 'short', 'price': 10658.29, 'quantity': -0.0981240282928003, 'wallet_balance': 2091.6686990257413, 'timestamp': '2019-08-19 07:17:00'}, {'type': 'buy', 'position_type': 'short', 'price': 10198.75, 'quantity': -0.0981240282928003, 'wallet_balance': 3092.411132576938, 'timestamp': '2019-09-20 03:04:00'}, {'type': 'buy', 'position_type': 'long', 'price': 10203.64, 'quantity': 0.3030694078365111, 'wallet_balance': 4.547473508864641e-13, 'timestamp': '2019-09-20 03:05:00'}, {'type': 'sell', 'position_type': 'long', 'price': 9714.59, 'quantity': 0.3030694078365111, 'wallet_balance': 2944.195038674493, 'timestamp': '2019-09-23 21:21:00'}, {'type': 'sell', 'position_type': 'short', 'price': 9693.66, 'quantity': -0.3037237780853148, 'wallet_balance': 5888.390077348986, 'timestamp': '2019-09-23 22:12:00'}]
print(dictlist[1]['timestamp'])

# 391. timestamp'te 10209.81'den longluyor.. 
# 1696. index'te 10677.77'den long kapatıyor.
# 1699. da 10658.29'den shortluyor.
# 47525'de satıyor. 4442'de satması gerekirdi. Hemen shortlama ve short kapama algolarını düzelt.


#Buy Lines: [7031.5, 7585.0, 8569.0, 9122.5, 10198.75, 11213.5, 12607.5]
#Sell Lines: [6688.5, 7215.0, 8151.0, 8677.5, 9701.25, 10666.5, 11992.5]
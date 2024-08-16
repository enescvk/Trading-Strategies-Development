import numpy as np
import pandas as pd

df = pd.read_csv("sample.txt", sep = "\t")
df['Timestamp'] = pd.to_datetime(df['Open time'], unit = 'ms')
data = df[['Timestamp', 'Close']]

lst = [
    {'index': 389, 'type': 'buy', 'position_type': 'long', 'price': 10209.81, 'quantity': 0.09794501562712725, 'wallet_balance': 0.0, 'timestamp': Timestamp('2019-08-18 09:29:00')}, 
    {'index': 1694, 'type': 'sell', 'position_type': 'long', 'price': 10677.77, 'quantity': 0.09794501562712725, 'wallet_balance': 1045.8343495128706, 'timestamp': Timestamp('2019-08-19 07:14:00')}, 
    {'index': 1694, 'type': 'sell', 'position_type': 'short', 'price': 10677.77, 'quantity': -0.09794501562712725, 'wallet_balance': 2091.6686990257413, 'timestamp': Timestamp('2019-08-19 07:14:00')}, 
    {'index': 4440, 'type': 'buy', 'position_type': 'short', 'price': 10197.19, 'quantity': -0.09794501562712725, 'wallet_balance': 3090.432632928527, 'timestamp': Timestamp('2019-08-21 05:00:00')}, 
    {'index': 4440, 'type': 'buy', 'position_type': 'long', 'price': 10197.19, 'quantity': 0.30306708347383216, 'wallet_balance': 0.0, 'timestamp': Timestamp('2019-08-21 05:00:00')}, 
    {'index': 15318, 'type': 'sell', 'position_type': 'long', 'price': 9688.23, 'quantity': 0.30306708347383216, 'wallet_balance': 2936.183610123685, 'timestamp': Timestamp('2019-08-28 18:18:00')}, 
    {'index': 15318, 'type': 'sell', 'position_type': 'short', 'price': 9688.23, 'quantity': -0.30306708347383216, 'wallet_balance': 5872.36722024737, 'timestamp': Timestamp('2019-08-28 18:18:00')}, 
    {'index': 22621, 'type': 'buy', 'position_type': 'short', 'price': 10211.03, 'quantity': -0.30306708347383216, 'wallet_balance': 8966.994301611174, 'timestamp': Timestamp('2019-09-02 20:01:00')}, 
    {'index': 22621, 'type': 'buy', 'position_type': 'long', 'price': 10211.03, 'quantity': 0.8781674622061802, 'wallet_balance': 0.0, 'timestamp': Timestamp('2019-09-02 20:01:00')}, 
    {'index': 23657, 'type': 'sell', 'position_type': 'long', 'price': 10678.89, 'quantity': 0.8781674622061802, 'wallet_balance': 9377.853730478955, 'timestamp': Timestamp('2019-09-03 13:17:00')}, 
    {'index': 23657, 'type': 'sell', 'position_type': 'short', 'price': 10678.89, 'quantity': -0.8781674622061802, 'wallet_balance': 18755.70746095791, 'timestamp': Timestamp('2019-09-03 13:17:00')}, 
    {'index': 31947, 'type': 'buy', 'position_type': 'short', 'price': 10177.06, 'quantity': -0.8781674622061802, 'wallet_balance': 27692.87041387794, 'timestamp': Timestamp('2019-09-09 07:27:00')}, 
    {'index': 31947, 'type': 'buy', 'position_type': 'long', 'price': 10177.06, 'quantity': 2.721107118743325, 'wallet_balance': 0.0, 'timestamp': Timestamp('2019-09-09 07:27:00')}, 
    {'index': 46086, 'type': 'sell', 'position_type': 'long', 'price': 9666.7, 'quantity': 2.721107118743325, 'wallet_balance': 26304.1261847561, 'timestamp': Timestamp('2019-09-19 03:06:00')}, 
    {'index': 46086, 'type': 'sell', 'position_type': 'short', 'price': 9666.7, 'quantity': -2.721107118743325, 'wallet_balance': 52608.2523695122, 'timestamp': Timestamp('2019-09-19 03:06:00')}, 
    {'index': 47101, 'type': 'buy', 'position_type': 'short', 'price': 10260.31, 'quantity': -2.721107118743325, 'wallet_balance': 80527.65495102553, 'timestamp': Timestamp('2019-09-19 20:01:00')}, 
    {'index': 47101, 'type': 'buy', 'position_type': 'long', 'price': 10260.31, 'quantity': 7.848462176194046, 'wallet_balance': 0.0, 'timestamp': Timestamp('2019-09-19 20:01:00')}]
print(len(lst))
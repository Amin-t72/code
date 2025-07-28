import math
import os
import random
import re
import sys
from datetime import datetime, timedelta


H = 5
W = 2
D = 1

data = ['timestap: 2000-01-01 06:00:01.123, price: 100.45', 'timestap: 2000-01-01 06:00:05.561, price: 100.21', 'timestap: 2000-01-01 06:00:08.468, price: 102.68', 'timestap: 2000-01-01 06:00:12.359, price: 105.97', 'timestap: 2000-01-01 06:00:13.497, price: 103.85', 'timestap: 2000-01-01 06:00:16.525, price: 101.73', 'timestap: 2000-01-01 06:00:20.965, price: 101.67']

def pnl_calculator(H,W,D, data):
    price_data = []
    all_prices = []
    all_timestamps = []

    for i in data:
        timestamp, price = i.split(',')
        timestamps = timestamp.strip('timestamp: ')
        prices = price.split('price: ')[1]
    
        all_timestamps.append(timestamps)
        all_prices.append(float(prices))
    

    dates = []




    for j in range(len(all_timestamps)):
        date = all_timestamps[j][0:10]
        datesFormat = [date[0:4], date[5:7], date[8:10]]
    
        times = all_timestamps[j][11:23]
        HH = times[0:2]
        MM = times[3:5] 
        SS = times[6:8] 
        MS = times[9:12]
            
        date_datetime = datetime(int(datesFormat[0]), int(datesFormat[1]), int(datesFormat[2]), int(HH), int(MM), int(SS))
        date_with_ms = date_datetime + timedelta(milliseconds=int(MS))
        dates.append(date_with_ms)


    date_price = []
    for i in range(len(dates)):
        date_price.append((dates[i], all_prices[i]))

    pnl = 0 
    time_stamps_of_buys = []
    time_stamps_of_sells = []                                               

    time_stamps_sells = []                                                      
    time_stamps_buys = []      

    last_trade_time = datetime(1000, 1, 1, 1, 1, 1, 100)


    # Keep in mind we are at time dates[i+1] in this loop because we compare with the previous time 
    for i in range(len(date_price) - 1):
        d = ((date_price[i+1][1] - date_price[i][1])/date_price[i+1][1]) * 100
    
        if d >= D:
            if last_trade_time != 0.0 and (dates[i+1] - last_trade_time).total_seconds() > W:
                if len(time_stamps_of_buys) == 0:
                    pnl = pnl - all_prices[i+1]
                    time_stamps_of_buys.append(dates[i+1])
                    last_trade_time = dates[i+1]
                    for j in range(len(date_price)):
                        diff_secs = (dates[j] - dates[i+1]).total_seconds()
                        if j > i and diff_secs > H:
                            pnl = pnl + all_prices[j-1]
                            time_stamps_of_sells.append(dates[j-1])
                            break
                elif len(time_stamps_of_buys) >= 1: 
                    diff_secs = (dates[i+1] - time_stamps_of_buys[-1]).total_seconds()
                    if diff_secs >= W:
                        pnl = pnl - all_prices[i+1]
                        time_stamps_of_buys.append(dates[i+1])
                        last_trade_time = dates[i+1]
                        for j in range(len(date_price)):
                            H_secs = (dates[j] - dates[i+1]).total_seconds()
                            if j > i and H_secs > H:
                                pnl = pnl + all_prices[j-1]
                                time_stamps_of_sells.append(dates[j-1])
                                break
            else:
                print('we need to skip this trade because we waited: ', (dates[i+1] - last_trade_time).total_seconds(),' seconds')
                        
        if d <= -D: 
            if (dates[i+1] - last_trade_time).total_seconds() > W:
                if len(time_stamps_sells) == 0:
                    pnl = pnl + all_prices[i+1]
                    time_stamps_sells.append(dates[i+1])
                    last_trade_time = dates[i+1]
                    for j in range(len(dates)):
                        difference_secs = (dates[j] - dates[i+1]).total_seconds()
                        if j > i and difference_secs > H: 
                            pnl = pnl - all_prices[j-1]
                            time_stamps_buys.append(dates[j-1])
                            break
                        if (dates[len(dates)- 1] -dates[i+1]).total_seconds() < H:
                            pnl = pnl - all_prices[len(dates)-1]
                            time_stamps_buys.append(dates[len(dates)-1])
                            break
                        
                elif len(time_stamps_sells) >= 1:
                    diff_secs = (dates[i+1] - time_stamps_sells[-1]).total_seconds()
                    if diff_secs >= W:
                        pnl = pnl + all_prices[i+1]
                        time_stamps_sells.append(dates[i+1])
                        last_trade_time = dates[i+1]
                        for j in range(len(date_price)):
                            H_secs = (dates[j] - dates[i+1]).total_seconds()
                            if j > i and H_secs > H:
                                pnl = pnl - all_prices[j-1]
                                time_stamps_buys.append(dates[j-1])
                                break
                            if j > i and H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():
                                pnl = pnl - all_prices[len(dates)-1]
                                time_stamps_buys.append(dates[len(dates)-1])
                                break
            else:
                print('we need to skip this trade because we waited: ', (dates[i+1] - last_trade_time).total_seconds(),' seconds')
        
    return round(pnl,2)


print(pnl_calculator(H,W,D, data))
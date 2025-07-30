from datetime import datetime


H = 5
W = 2
D = 1

data = ['timestap: 2000-01-01 06:00:01.123, price: 121.45', 'timestap: 2000-01-01 06:00:04.561, price: 120.21', 'timestap: 2000-01-01 06:00:08.468, price: 100.68', 'timestap: 2000-01-01 06:00:09.359, price: 95.97', 'timestap: 2000-01-01 06:00:11.497, price: 99.85', 'timestap: 2000-01-01 06:00:14.525, price: 150.73', 'timestap: 2000-01-01 06:00:17.965, price: 200.67']
          
          
def pnl(H,W,D, data):
    
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
    last_trade_time = 0

    #Keep in mind we are at time dates[i+1] in this loop, because we compare with the previous time

    for i in range(len(date_price) - 1):

        d = ((date_price[i+1][1] - date_price[i][1]) / date_price[i+1][1]) * 100
        
        
        if d >= D: 
            #We should buy a stock here
            if last_trade_time == 0:                                                        #distinguish the cases where we have a last_trade_time because we have to wait W seconds before the next trade
                pnl = pnl - all_prices[i+1]                                                 #update pnl by buying a stock
                last_trade_time = dates[i+1]                                                #update last_trade_time to current time
                
                for j in range(len(date_price)):                                            #we sell the stock after holding it for H seconds here
                    H_secs = (dates[j] - dates[i+1]).total_seconds()
                    if j > i and H_secs > H:
                        pnl = pnl + all_prices[j-1]
                        break
                    elif H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():
                            pnl = pnl + all_prices[len(all_prices) - 1]
                            break
                    
            elif last_trade_time != 0:                                                      #case where we have a last_trade_time so we check if we waited W seconds and do the same actions (buy and sell after holding for H seconds)
                W_secs = (dates[i+1] - last_trade_time).total_seconds()
                if W_secs >= W:
                    pnl = pnl - all_prices[i+1]
                    last_trade_time = dates[i+1]
                    for j in range(len(date_price)):
                        H_secs = (dates[j] - dates[i+1]).total_seconds()
                        if j > i and H_secs > H:
                            pnl = pnl + all_prices[j-1]
                            break
                        elif H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():
                            pnl = pnl + all_prices[len(all_prices) - 1]
                            break
            
                            
        if d <= -D:                                                     
            #We should sell a stock here
            if last_trade_time == 0:                                                        #same principles, distinguish the cases where we have a last_trade_time because we have to wait W seconds before the next trade
                pnl = pnl + all_prices[i+1]                                                 #update pnl by selling a stock
                last_trade_time = dates[i+1]                                                #update last_trade_time to current time
                for j in range(len(date_price)):                                            #in this loop we buy the stock again after H seconds
                    H_secs = (dates[j] - dates[i+1]).total_seconds()
                    if j > i and H_secs > H: 
                        pnl = pnl - all_prices[j-1]
                        break 
                    elif H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():     #this elif statement is there to check if we can wait more than H seconds otherwise we sell at the final time
                            pnl = pnl - all_prices[len(all_prices)- 1]
                            break 
            
            elif last_trade_time != 0:                                                      #this is the case where we have a last_trade_time so we have to check if we waited W seconds before making a trade
                W_secs = (dates[i+1] - last_trade_time).total_seconds()
                if W_secs >= W:
                    pnl = pnl + all_prices[i+1]
                    last_trade_time = dates[i+1]
                    for j in range(len(date_price)):
                        H_secs = (dates[j] - dates[i+1]).total_seconds()
                        if j >i and H_secs > H:
                            pnl = pnl - all_prices[j-1]
                            break 
                        elif H_secs == (dates[len(dates)- 1] - dates[i+1]).total_seconds():
                            pnl = pnl - all_prices[len(all_prices)- 1]
                            break 

    return(round(pnl,2))

print(pnl(H,W,D,data))

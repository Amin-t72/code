Algorithm of calculating pnl

H = Holding time in seconds
D = Difference in precentage
W = Waiting time in seconds

Algorithm 
  - We assume that the algorithm is continuosly getting price updates with their associated time stamp.
  - Let P1 be the last price and T1 the last time associated to the last price P1
  - When we get an update of P2 at time T2, we calculate the precentage change in price: d = (P2-P1)/P1.
  - If d >= D, then the algorithm buys a stock. If d <= D, then we sell a stock.
  - Now we hold the stock for H seconds and we do the opposite trade after H seconds. This happens at the latest price the algorithm has seen.
  - We can not do another trade until W seconds have passed from T2. 

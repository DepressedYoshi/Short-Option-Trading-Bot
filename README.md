# Short-Option-Trading-Bot

## Intro
This is a algorism trading project that uses [quantconnect's](https://github.com/QuantConnect) framework and back testing data. The primary strategy is to short any abnormal rise in the market using options. This strategy is inspired by a period of personal experimentation during covid and the rise of meme stock like GameStop. Make no mistake, my intension was to profit off of the eventual failure of wall street bet and not support them. 
I notice that sudden spike in prices that exceeds 20% are quite common and, logically, all of them should be shorted. For a short while I check the market weekly to select 1-4 "abnormal" stocks to short with option (not all of them can be traded with option) and it was medium successful. By that, I means 80% of the time my prediction would be correct however I make mistakes due to the emotional impact of the volatile movements, which led to me turn to algorism based trading, to both better filter, evaluate, and execute a trade. It all seems intuitive, it is a highly structured and calculated strategy with high ROT but also high risk. It deals with stocks that has significantly increase or decreased in a short timeframe, highly volatile movement means this is def not "investment" and more "trading. Hence, it is handled by a algorism and not human. 
Option are chosen for the sake of leverage and profit. This is purely an experimental component to see if algorism can limit the risk of option trading to justify it. Moreover, I am lazy and I have other things to do in life. This trading strategy require constant monitoring but not high frequency trading which seems perfect to be managed by a bot that can be deployed by average joe like myself. 

## Design 
the trading system can be broken down into 4 parts 
1. [[#Stock selection and Filter]] 
2. [[#Trade evaluation / risk calculation]]  
3. [[#Trade execution]]
4. [[#Portfolio management]] 
### Stock selection and Filter 
Stock selection is done after market on a bi-weekly basis to avoid taking up too much time and optimized the initialization time. The only thing that should be initialize and tightly monitored on daily basis is the portfolio manager. 
The filter produce a list of 20 final stocks picks from the entire market. this task will take some time but it is okay because it is done after market. To optimize the process however, the filter is divided into 2 layer. Frist rough filter has 2 criteria that should be easy to evaluate 
1.  Option trading is available for the said stock 
2.  the trading price of the said stock is above 15$
The second layer of refined filter produce the top  20 stock that has the biggest movement in the last week. The second layer is essentially sorting all of the remaining stock from the biggest mover to the smaller mover, and then only return the top 20 stocks. It does not have to return minimum 20, just maximum of 20. The minimum increase in the last 5 days has to be above 5% for its to be the list, so there is a possibility that the list have less then 20 stocks, but for sake of simplicity, the following instruction will assume there are 20 stocks in the final list. This list of twenty stocks is then send to trade evaluation 
### Trade evaluation / risk calculation  
This part is done after stock selection, it follows the same pattern of bi-weekly execution. It will take in a list of 20 stock names and return maximum of 10 trade order, but it is never forced to produce a trade order, if it calculated none of the stocks in the given list has profitable trade then it will simply wait another 2 week. It is broken down as following 
#### short profitability evaluation 
This part will iterate through the list of stocks that will be given as input,  then determine if the stock have a high likelihood of going down in the future. and then remove stock form the list if it dos not have a high likelihood of going down in the future. Or, if the number of stocks in the list exceeds The number of stock that should remind in the list, it will remove the few stock that has the least potential to profit, keep in mind the profit strategy is shorting that stock. 
The number of stock that should remind in the list is determined by the maximum position allowed minus  the current existing position that is still open in the portfolio. 
The potential to profit is calculated bas on technical analysis and return a number between 0 and 100. It that does the following  
- check if it has mid to long term down trends
	- yes
		- given a score between 50-70, the bigger the increase in prices (in percent) in the last week the bigger the score. E.G. if a stock that as been going down for 3+ month had a 15+% increase it will have a score of 65-70; whereas stock with 5% increase will have a score toward the lower ends. The duration of down trend can also influence the score, if it had a short down trend then score should be in the lower range and vice versa. 
	- no
		- given a score between 10-50, same logic of scoring base on the relative difference in long term downtrend and short term increase, but change of score range since it does not have a long term down trend. A sudden huge increase in prices (in percentage in the last week) will have a score around 50 such that even if the stock usually does well, a huge increase is still abnormal and should be shorted.
- check all the over bought indicator. this step will use a lot of technical indicator to analyze  the stock. Each of the indicator below will return a score that is between 1-5, 1 being highly bullish, 3 being neutral, and 5 being highly bearish. This score is then added to the score from down trend.
	- Volume and candle stick pattern 
	- PE 
	- OSC
	- RSI12
	- RSI 20
	- RSI 24
	- BR 
	- VR
	- AR
	- BIAS
	- MA
- check if the company finance 
	- if it just released its quarterly report, then subtract 7 point. 
if it has a score lower then 75, it is considered not having a string likelihood of going down. 
#### option strategy evaluation 
demine how many leg the option strategy should be, 
determine the length and 
#### option risk evolution 
To be researched, check academia for best equation to mathematically evaluate the risk of an option trade and use that data to modify the stop loss, position size, strike price, strike date, etc. 
This sets the parameter of a option trade order 

### Trade execution 
executed when there is a order pending from the Trade evaluation / risk calculation or Portfolio management. for the sake of testing each order should be logged in counsel. 
- start trade
	- receive target from Trade evaluation
	- send in order 
		- send in stop loss 
	- add stock to portfolio
- end trade 
	- Receive order from PM
	- close position 
	- remove stock from portfolio
### Portfolio management 
executed on daily basis, this monitor the existing positions. 
has status variables that tells trade execution 
stop loss 
end for profit 
never allow an option to execute 
if cash > 80% --> invest in SPY, sell later if needed
## Testing 
#### Default Parameter for initialization 
- **Initial Fund** : $100,000
- **Timeframe** : 2015 - 2019, 2012-2016, 2010-2020, 2019-2022, 
- **Cash Reserve** : 20%
- **Stop Loss** : 20%
- **bench mark** : SPY
- **Max Number of Position** : 10
- **Max $ per position** : 10%

## Deployment 


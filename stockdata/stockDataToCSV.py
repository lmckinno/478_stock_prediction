import csv
import requests
stocks = ['AAPL']


def calculateIndicators(history):
	# Indicators to calculate:
	# SMA (8 or 10, 50, 100, 200)
	# EMA (same as above)
	# RSI (14 period)
	# Prvious candlestick shape?
	# Relative Volume of day based on recent history of volumes (you determine the number of days to average)
	# Stochastic oscillator - value
	# Stochastic oscillator - difference between k and d
	# MACD
	# Bollinger band value
	# Current position with relation to BB
	# DONE!
	

	pass

def calculateTarget(history):
	"""
	Add a column to the end of history
	This column should simply be the percent change of the day t+1
	It's forecasting the percent change from one close to the next close.
	Practical applications might make use of percent change from the open to a close of a day, based on the time when someone should purchase the stocks
	Other possible targets could include the perceived value change overnight (model can tell you what part of the day to buy)
	REmember, possible times to buy are after 9:30AM EST all the way to 4:00PM EST

	"""
	pass


def getInformation(sym):
	historyString = "https://api.iextrading.com/1.0/stock/" + sym + "/chart/5y"
	history = requests.get(historyString).json()
	return history



def getSMA(h):
	ret10 = []
	ret50 = []
	for i in range(0, len(h)):
		if h < 50:
			ret10.append(0)
			ret50.append(0)
		else:
			ret10.append(sum(h[i-10:i]) / len(h[i-10:i]))
			ret50.append(sum(h[i-50:i]) / len(h[i-50:i]))
	return ret10, ret50

def getEMA(h):
	alpha10 = 2 / (10 + 1)
	alpha50 = 2 / (50 + 1)
	ret10 = []
	ret50 = []
	for i in range(0, len(h)):
		if h < 50:
			ret10.append(0)
			ret50.append(0)
		else:
			ret10.append(sum(h[i-10:i]) / len(h[i-10:i]))
			ret50.append(sum(h[i-50:i]) / len(h[i-50:i]))
	return ret10, ret50

def main():

	history = getInformation(stocks[0])

	# Calculate the other indicators
	
	sma10, sma50 = getSMA(history)
	ema10, ema50 = getEMA(history)
	rsi = getRSI(history)
	relativeVolume = getRelativeVolume(history)
	stochastics, stochasticKDdifferentiation = getStochastics(history)
	macd = getMACD(history)
	bb, relativeBB = getBB(history)

	with open('AAPLhistory.csv', 'w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
		writer.writerow(['date', 'open', 'high', 'low', 'close', 'volume', 'unadjustedVolume', 'vwap', 'change', 'changeOverTime', 'percent change'])
		for el in history:
			writer.writerow([el['date'], el['open'], el['high'], el['low'], el['close'], el['volume'], el['unadjustedVolume'], el['vwap'], el['change'], el['changeOverTime'], el['changePercent']])


main()
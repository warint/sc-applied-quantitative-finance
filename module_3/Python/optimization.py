
# See here for source: https://towardsdatascience.com/how-to-be-a-successful-investor-simple-portfolio-analysis-with-python-7b66fc90fa68

import pandas_datareader as web
import pandas as pd
import numpy as np

tslaQuote = web.DataReader('TSLA', data_source = 'yahoo', start = '2010-01-01', ends = '2018-12-31')

print(tslaQuote)

stocks = ['GOOGL', 'TM', 'KO', 'PEP']
numAssets = len(stocks)
source = 'yahoo'
start = '2010-01-01'
end = ' 2019-5-31'

data = pd.DataFrame(columns=stocks)
for symbol in stocks:
  data[symbol] = web.DataReader(symbol, data_source=source, start=start, end=end)['Adj Close']
  
list(data)
data['GOOGL']




# Calculating log returns

percent_change = data.pct_change()
returns  np.log(1+percent_change)

returns.head()

meanDailyRetruns = returns.mean()
covMatrix = returns.cov()


# Returns we are getting on average per day from these companies

meanDailyReturns

covMatrix


# Calculate epected portfolio performance

weights = np.array([0.5, 0.2, 0.2, 0.1])
portReturn = np.sum(meanDailyReturns*weights)
portStdDev = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights)))

# Daily returns
portReturn

# Yearly returns
portReturn*365

portStdDev

portStdDev*portStdDev*365



# Visualizations

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))
for c in returns.columns.values:
  plt.plot(returns.index, returns[c], lw=3, alpha=0.8, label=c)

plt.legend(loc='upper left', fontsize=12)
plt.ylabel('returns')



# Optimizing our portfolio weights

import scipy.optimize as sco

def calcPortfolioPerf(weights, meanReturns, covMatrix):
  
  portReturn = np.sum(meanReturns*weights)
  portStdDev = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights)))
  return portReturn, portStdDev


## Sharpe ratio

def negSharpeRatio(weights, meanReturns, covMatrix, riskFreeRate):
  
  p_ret, p_var = calcPortfolioPerf(weights, meanReturns, covMatrix)
  
  return -(p_ret - riskFreeRate) / p_var

## Negative Sharpe ratio

def getPortfolioVol(weights, meanReturns, covMatrix):
  return calcPortfolioPerf(weights, meanReturns, covMatrix)[1]
  
def findMaxSharpeRatioPortfolio(meanReturns, covMatrix, riskFreeRate):
  
  numAssets = len(meanReturns)
  args = (meanReturns, covMatrix, riskFreeRate)
  constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
  bounds = tuple((0,1) for asset in range(numAssets))
  
  opts = sco.minimize(negSharpeRatio, numAssets*[1./numAssets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
  
  return opts

## Minimizing volatility

def findEfficientReturn(meanReturns, covMatrix, targetReturn):
  numAssets = len(meanReturns)
  args = (meanReturns, covMatrix)
  
  def getPortfolioReturn(weights):
    return calcPortfolioPerf(weights, meanReturns, covMatrix)[0]
  
  constraints = ({'type': 'eq', 'fun': lambda x: getPortfolioReturn(x) - targetReturn},
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
  bounds = tuple((0,1) for asset in range(numAssets))
  
  return sco.minimize(getPortfolioVol, numAssets*[1./numAssets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
  
def findEfficientFrontier(meanReturns, covMatrix, rangeOfReturns):
  efficientPortfolios = []
  for ret in rangeOfReturns:
    efficientPortfolios.append(findEfficientReturn(meanReturns, covMatrix, ret))
    
  return efficientPortfolios

findEfficientReturn(meanReturns, covMatrix, 0.1)

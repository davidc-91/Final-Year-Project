# -*- coding: utf-8 -*-
"""AR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14mG7tUwB0_6lYLfDCeNMlidRPJINxV0I
"""

!pip install statsmodels --upgrade

import pandas as pd
import numpy as np
from pandas import read_csv
from matplotlib import pyplot
series = read_csv('VF Test.csv', header=0, index_col=0)
df = pd.DataFrame(series)
df.describe()

"""**LINE PLOT**"""

from pandas import read_csv
from matplotlib import pyplot
series = read_csv('VF Test.csv', header=0, index_col=0)
print(series.head())
series.plot(rot=45)
pyplot.title('Line Plot')
pyplot.xlabel('Dates')
pyplot.ylabel('PCT')
pyplot.show()

"""**CHECK FOR AUTOCORRELATION**"""

from pandas import read_csv
from matplotlib import pyplot
from pandas.plotting import lag_plot
series = read_csv('VF Test.csv', header=0, index_col=0)
lag_plot(series)
pyplot.title('Lag Plot')
pyplot.show()

from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from matplotlib import pyplot
series = read_csv('VF Test.csv', header=0, index_col=0)
values = DataFrame(series.values)
dataframe = concat([values.shift(1), values], axis=1)
dataframe.columns = ['t-1', 't+1']
result = dataframe.corr()
print(result)

"""**AUTOCORRELATION PLOTS**"""

from pandas import read_csv
from matplotlib import pyplot 
from pandas.plotting import autocorrelation_plot
series = read_csv('VF Test.csv', header=0, index_col=0)
series.iloc[0] = 0
ax = autocorrelation_plot(series)
ax.set_xlim([0, 30])
pyplot.title('Pandas AutoCorrelation Plot')
pyplot.show()

# Autocorrelation Plot
from pandas import read_csv
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
series = read_csv('VF Test.csv', header=0, index_col=0)
series.iloc[0] = 0 
plot_acf(series)
pyplot.title('Statsmodels AutoCorrelation Plot')
pyplot.show()

# Partial Autocorrelation Plot
from statsmodels.graphics.tsaplots import plot_pacf
series.iloc[0] = 0  
plot_pacf(series)
pyplot.title('Partial Autocorrelation Plot')
pyplot.show()

"""**PERSISTENCE MODEL**"""

from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
series = read_csv('VF Test.csv', header=0, index_col=0)
# create lagged dataset
values = DataFrame(series.values)
dataframe = concat([values.shift(1), values], axis=1)
dataframe.columns = ['t-1', 't+1']
# split into train and test sets
X = dataframe.values
train, test = X[1:len(X)-7], X[len(X)-7:]
train_X, train_y = train[:,0], train[:,1]
test_X, test_y = test[:,0], test[:,1]

# persistence model
def model_persistence(x):
	return x

# walk-forward validation
predictions = list()
for x in test_X:
	yhat = model_persistence(x)
	predictions.append(yhat)
test_score = mean_squared_error(test_y, predictions)
print('Test MSE: %.3f' % test_score)
# plot predictions vs expected
pyplot.plot(test_y)
pyplot.plot(predictions, color='red')
pyplot.title('Persistence Model')
pyplot.xlabel('Days')
pyplot.ylabel('PCT')
pyplot.show()

"""**AUTOREGRESSION MODEL**"""

# create and evaluate a static autoregressive model
from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt
# load dataset
series = read_csv('VF Test.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
# split dataset
X = series.values
train, test = X[1:len(X)-7], X[len(X)-7:]
# train autoregression
model = AutoReg(train, lags=29)
model_fit = model.fit()
print('Coefficients: %s' % model_fit.params)
# make predictions
predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
for i in range(len(predictions)):
	print('predicted=%f, expected=%f' % (predictions[i], test[i]))
rmse = sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)
# plot results
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.xlabel('Days')
pyplot.ylabel('PCT')
pyplot.title('AR Model')
pyplot.show()

# create and evaluate an updated autoregressive model
from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt
# load dataset
series = read_csv('VF Test.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
# split dataset
X = series.values
train, test = X[1:len(X)-7], X[len(X)-7:]
# train autoregression
window = 29
model = AutoReg(train, lags=29)
model_fit = model.fit()
coef = model_fit.params
# walk forward over time steps in test
history = train[len(train)-window:]
history = [history[i] for i in range(len(history))]
predictions = list()
for t in range(len(test)):
	length = len(history)
	lag = [history[i] for i in range(length-window,length)]
	yhat = coef[0]
	for d in range(window):
		yhat += coef[d+1] * lag[window-d-1]
	obs = test[t]
	predictions.append(yhat)
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
rmse = sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)
# plot
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.xlabel('Days')
pyplot.ylabel('PCT')
pyplot.title('Rolling AR Model')
pyplot.show()
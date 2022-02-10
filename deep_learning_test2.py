import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 説明変数 = Year, Month, Day, 1日後の終値, 
# 目的変数 = 株価
def transform_df(df):
  df.loc[:,'Datetime'] = df.index
  df.loc[:,'Year'] = df.loc[:,'Datetime'].dt.year
  df.loc[:,'Month'] = df.loc[:,'Datetime'].dt.month
  df.loc[:,'Day'] = df.loc[:,'Datetime'].dt.day
  df = df.drop(['Datetime'], axis=1)
  df = df.reset_index()
  df = df.drop(['Date'], axis=1)
  return df

# 入力変数を整形
df = web.DataReader("4689.T", "yahoo", start=datetime.date(2017,1,1), end=datetime.date(2022,2,7))
df = transform_df(df)
x = df.drop('Adj Close', axis=1).values

df['Tommorow Adj Close'] = 0
for i, data in enumerate(df['Adj Close']):
  if (i+1) >= len(df['Adj Close']): continue
  df['Tommorow Adj Close'][i] = df['Adj Close'][i+1]

t = df['Tommorow Adj Close'].values
df = df.drop(['Adj Close', 'Tommorow Adj Close'], axis=1)

x_train, x_test, t_train, t_test = train_test_split(x, t, test_size=0.3, random_state=0)
model = LinearRegression()
model.fit(x_train, t_train)

train_score = model.score(x_train, t_train)
test_score = model.score(x_test, t_test)
print(train_score, test_score)

try_date = datetime.date(2022,2,8)
try_df = web.DataReader("4689.T", "yahoo", start=try_date, end=try_date)
try_df = transform_df(try_df)
try_x = try_df.drop('Adj Close', axis=1).values

result = model.predict(try_x)
print(result)
print(f'{try_date.year}年{try_date.month}月{try_date.day}日の株価終値予想は、{result}円です')
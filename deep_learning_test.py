import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sea
from sklearn.datasets import load_boston
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

dataset = load_boston()
x, t = dataset.data, dataset.target
columns = dataset.feature_names

df = pd.DataFrame(x, columns=columns)
df = pd.read_csv("regression_pls.csv")

t = df['Target'].values
x = df.drop(labels=['Target'], axis=1).values
x_train, x_test, t_train, t_test = train_test_split(x, t, test_size=0.3, random_state=0)

model = PLSRegression(n_components=11)
model.fit(x_train, t_train)

print(f'train score: {model.score(x_train, t_train)}')
print(f'test score: {model.score(x_test, t_test)}')

# ----ここまでが検証
# ----ここから推論

y = model.predict(x_test)

plt.figure(figsize=(12, 8))
sea.heatmap(df.corr().iloc[:20, :20], annot=True)
sea.jointplot(x='x1', y='x16', data=df)
plt.show()
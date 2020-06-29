import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import Lasso, Ridge, LinearRegression as LR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, explained_variance_score as EVS, mean_squared_error as MSE
from sklearn.preprocessing import PolynomialFeatures

# folder = "..\Data\data20200611_uniform_vc_4_size_8\\"
folder = "..\Data\data20200622_hotspot_vc4,8_node{0,18,36,54}_irate_0.1\\"
adv_data = pd.read_csv(folder + "fitdata.csv")
x = adv_data[['hop', 'localage', 'vcoccu']]
y = adv_data['latency']
# print(x.shape)
# print(x.head())
# print(y.head())
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
# print(x_train.shape)

reg = LR().fit(x_train, y_train)
yhat = reg.predict(x_test)
# print(yhat)
# 展示回归系数和截距
print(reg.coef_)
print(reg.intercept_)

print("均方差：", end='')
print(MSE(y_test, yhat))
print("平均值误差相对于样本真实值平均值的比例：", end='')
print(np.sqrt(MSE(y_test, yhat)) / y_test.mean())
# print(-cross_val_score(reg, x, y, cv=5, scoring="neg_mean_squared_error"))
print("可解释方差：", end='')
print(cross_val_score(reg, x, y, cv=5, scoring="explained_variance").mean())
print("r2 分数: ", cross_val_score(reg, x, y, cv=5, scoring="r2").mean(), r2_score(y_test, yhat),
      reg.score(x_test, y_test))

plt.plot(range(len(yhat)), yhat, 'b', label="predict")
# 显示图像
# plt.savefig("predict1.png")
plt.show()

plt.figure()
plt.plot(range(len(yhat)), yhat, 'b', label="predict")
plt.plot(range(len(yhat)), y_test, 'r', label="test")
plt.legend(loc="upper right")  # 显示图中的标签
plt.xlabel("the number of latency")
plt.ylabel('value of latency')
# plt.savefig("ROC1.png")
plt.show()


'''
多元非线性回归！
a^2, b^2, ab...
本质还是线性回归
'''
print("非线性——数据预处理")
po = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)
x_poly = po.fit_transform(x)
# print(pd.DataFrame(x_poly).head())
x_poly = pd.DataFrame(x_poly, columns=['hop', 'localage', 'vcoccu', 'hop^2', 'hop_localage', 'hop_vcoccu', 'localage^2',
                                       'localage_vcoccu', 'vcoccu^2'])
print(x_poly.head())

# train and predict
x_train2, x_test2, y_train2, y_test2 = train_test_split(x_poly, y, test_size=0.2, random_state=1)
reg2 = LR().fit(x_train2, y_train2)
yhat2 = reg2.predict(x_test2)
# print(yhat2)
# 展示回归系数和截距
print(reg2.coef_)
print(reg2.intercept_)

print("平均值误差相对于样本真实值平均值的比例：", end='')
print(np.sqrt(MSE(y_test2, yhat2)) / y_test2.mean())
print("可解释方差：", end='')
print(cross_val_score(reg2, x_poly, y, cv=5, scoring="explained_variance").mean())
print("r2 分数: ", cross_val_score(reg2, x_poly, y, cv=5, scoring="r2").mean(), r2_score(y_test2, yhat2))


plt.plot(range(len(yhat2)), yhat2, 'b', label="predict")
# 显示图像
# plt.savefig("predict2.png")
plt.show()

plt.figure()
plt.plot(range(len(yhat2)), yhat2, 'b', label="predict")
plt.plot(range(len(yhat2)), y_test2, 'r', label="test")
plt.legend(loc="upper right")  # 显示图中的标签
plt.xlabel("the number of latency")
plt.ylabel('value of latency')
# plt.savefig("ROC2.png")
plt.show()
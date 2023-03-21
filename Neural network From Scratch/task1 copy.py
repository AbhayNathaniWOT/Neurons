from sklearn.model_selection import train_test_split
from sklearn import datasets
from NN_from_Scratch import Network, Dense, ReLU, TanH
import matplotlib.pyplot as plt
import numpy as np

# Prepare Data
data_size = 1000
# noise = np.array([0.1 for i in range(data_size)])
X = np.array([[np.random.randint(-100, 100), np.random.randint(-100,
             100), np.random.randint(-100, 100)] for i in range(data_size)])


def func(X):
    return (X[:, 0]**3)+(X[:, 1]**2)+(X[:, 2]) + 6


y = func(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
y_train = y_train.reshape((y_train.shape[0], 1))

lr = 0.0000000001

NN = Network()
NN.add(Dense(X.shape[1], 8, learning_rate=lr))
NN.add(ReLU())
NN.add(Dense(8, 10, lr))
NN.add(ReLU())
NN.add(Dense(10, 10, lr))
NN.add(ReLU())
NN.add(Dense(10, 10, lr))
NN.add(ReLU())
NN.add(Dense(10, 1, lr))
epochs = 1000
for epoch in range(epochs):
    print("Epoch:", epoch)
    print(NN.train(X=X_train, y=y_train))
    train_acc = NN.predict(X)


y_pred = NN.predict(X_test)
print(y_pred)
# plt.scatter(X_test[:, 1], y_test, s=2, color="black", linewidth=0.5)
# plt.scatter(X_test[:, 1], y_pred, s=5, color="red", linewidth=0.5)


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(X_test[:, 0].flatten(), X_test[:, 2].flatten(),
           y_test.flatten(), s=1, color="black", linewidth=0.5)
ax.scatter(X_test[:, 0].flatten(), X_test[:, 2].flatten(),
           y_pred.flatten(), color="red", s=1, linewidth=0.5)

plt.show()

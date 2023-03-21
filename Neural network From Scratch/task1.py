from sklearn.model_selection import train_test_split
from sklearn import datasets
from NN_from_Scratch import Network, Dense, ReLU
import matplotlib.pyplot as plt
import numpy as np

# Prepare Data
data_size = 10000

X = np.array([[np.random.uniform(low=-3, high=3),
                  np.random.uniform(low=-3, high=3),
               np.random.uniform(low=-3, high=3),] for i in range(data_size)])


def func(X):
    return (X[:, 0]**3)+(X[:, 1]**2)+(X[:,2])+6


y = func(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
y_train = y_train.reshape((y_train.shape[0], 1))

lr = 0.000001

NN = Network()
NN.add(Dense(X.shape[1], 50, learning_rate=lr))
NN.add(ReLU())
NN.add(Dense(50, 50, lr))
NN.add(ReLU())
NN.add(Dense(50, 50, lr))
NN.add(ReLU())
NN.add(Dense(50, 1, lr))
epochs = 500

for i in range(epochs):
    NN.train(X_train, y_train)
y_pred = NN.predict(X_test)




fig = plt.figure("Actual")

ax = plt.axes(projection='3d')
ax.scatter(X_test[:, 0].flatten(), X_test[:, 1].flatten(),
           y_test.flatten(), s=1, color="#1b1b1b")


fig = plt.figure("Predicted")

ax2 = plt.axes(projection='3d')

ax2.scatter(X_test[:, 0].flatten(), X_test[:, 1].flatten(),
            y_pred.flatten(), color="green", s=1)


fig = plt.figure("Combined")

ax3 = plt.axes(projection='3d')
ax3.scatter(X_test[:, 0].flatten(), X_test[:, 1].flatten(),
            y_test.flatten(), s=1, color="#1b1b1b")
ax3.scatter(X_test[:, 0].flatten(), X_test[:, 1].flatten(),
            y_pred.flatten(), color="blue", s=1)

plt.show()

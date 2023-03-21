from sklearn.model_selection import train_test_split
from sklearn import datasets
from NN_from_Scratch import Network, Dense, ReLU
import matplotlib.pyplot as plt


X, y = datasets.make_regression(
    n_samples=1000, n_features=1, noise=20, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

y_train = y_train.reshape((y_train.shape[0], 1))

NN = Network()
NN.add(Dense(1, 8))
NN.add(ReLU())
NN.add(Dense(8, 10))
NN.add(ReLU())
NN.add(Dense(10, 1))
epochs = 1000

for epoch in range(epochs):
    print("Epoch:", epoch)
    print(NN.train(X=X_train, y=y_train))

y_pred = NN.predict(X_test)

plt.scatter(X_test, y_test, s=2, color="black", linewidth=0.5)
plt.scatter(X_test, y_pred, s=2, color="red", linewidth=0.5)

plt.show()

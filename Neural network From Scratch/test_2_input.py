from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from NN_from_Scratch import Network, Dense, TanH
from mpl_toolkits import mplot3d


NN = Network()
NN.add(Dense(2, 8))
NN.add(TanH())
NN.add(Dense(8, 8))
NN.add(TanH())
NN.add(Dense(8, 1))
epochs = 1000
X = np.array([[np.random.uniform(low=-3, high=3),
               np.random.uniform(low=-3, high=3)] for i in range(20000)])


y = np.array([[5*(i[0]**2) + 6*i[1]] for i in X])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

y_train = y_train.reshape((y_train.shape[0], 1))

for epoch in range(epochs):
    print("Epoch:", epoch)
    print(NN.train(X=X_train, y=y_train))
    train_acc = NN.predict(X)

y_pred = NN.predict(X_test)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(X_test[:, 0].flatten(), X_test[:, 1].flatten(),
           y_test.flatten(), s=1, color="black", linewidth=0.5)
ax.scatter(X_test[:, 0].flatten(), X_test[:, 1].flatten(),
           y_pred.flatten(), color="red", s=1, linewidth=0.5)
ax.set_title('wireframe')
plt.show()

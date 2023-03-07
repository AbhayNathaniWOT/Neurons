import numpy as np


def unit_step_func(x):
    return np.where(x > 0, 1, 0)


class Perceptron:

    def __init__(self, learning_rate, n_iters) -> None:
        self.learning_rate = learning_rate
        self.n_iters = n_iters
        self.activation_func = unit_step_func
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # init params
        self.weights = np.zeros(n_features)
        self.bias = 0

        # Convert to binary Classes
        y_ = np.where(y > 0, 1, 0)

        # learn Weights
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_pred = self.activation_func(linear_output)

                # Perceptron Update Rule
                update = self.learning_rate * (y_[idx]-y_pred)
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        return self.activation_func(np.dot(X, self.weights) + self.bias)

    def accuracy(self, X_test, y_test):
        return np.sum(y_test-self.predict(X_test))/len(y_test)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn.model_selection import train_test_split

    X, y = datasets.make_blobs(
        n_samples=1500, n_features=2, centers=2, cluster_std=1.55, random_state=2)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=30)
############################################################
    p = Perceptron(learning_rate=0.00001, n_iters=5)
    p.fit(X_train, y_train)
    print("Accuracy: ", p.accuracy(X_test, y_test))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.scatter(X_train[:, 0], X_train[:, 1], marker="o", c=y_train)

    x0_1 = np.amin(X_train[:, 0])
    x0_2 = np.amax(X_train[:, 0])

    x1_1 = (-p.weights[0] * x0_1 - p.bias) / p.weights[1]
    x1_2 = (-p.weights[0] * x0_2 - p.bias) / p.weights[1]

    ax.plot([x0_1, x0_2], [x1_1, x1_2], "r")

    ymin = np.amin(X_train[:, 1])
    ymax = np.amax(X_train[:, 1])
    ax.set_ylim([ymin - 3, ymax + 3])
###########################################################
    p = Perceptron(learning_rate=0.0001, n_iters=10)
    p.fit(X_train, y_train)
    print("Accuracy: ", p.accuracy(X_test, y_test))


    x1_1 = (-p.weights[0] * x0_1 - p.bias) / p.weights[1]
    x1_2 = (-p.weights[0] * x0_2 - p.bias) / p.weights[1]

    ax.plot([x0_1, x0_2], [x1_1, x1_2], "k")

    ymin = np.amin(X_train[:, 1])
    ymax = np.amax(X_train[:, 1])
    ax.set_ylim([ymin - 3, ymax + 3])
########################################################
    p = Perceptron(learning_rate=0.0000001, n_iters=100)
    p.fit(X_train, y_train)
    print("Accuracy: ", p.accuracy(X_test, y_test))



    x1_1 = (-p.weights[0] * x0_1 - p.bias) / p.weights[1]
    x1_2 = (-p.weights[0] * x0_2 - p.bias) / p.weights[1]

    ax.plot([x0_1, x0_2], [x1_1, x1_2], "b")

    ymin = np.amin(X_train[:, 1])
    ymax = np.amax(X_train[:, 1])
    ax.set_ylim([ymin - 3, ymax + 3])

    plt.show()

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
import matplotlib.pyplot as plt

class LinearRegression:
    def __init__(self, learning_rate=0.00001, n_iter=1000):
        self.learning_rate = learning_rate
        self.n_iter = n_iter
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iter):
            # Predict y = wX + b

            # w dot(.) X + b
            y_pred = np.dot(X, self.weights) + self.bias

            # Not summing while using Dot product
            # np.dot includes summation

            # Derivatives of weights and bias for Gradient Descent
            # Gradients ->
            dw = (1/n_samples) * np.dot(X.T, (y_pred-y))
            db = (1/n_samples) * np.sum(y_pred-y)

            # Update Weights
            self.weights -= self.learning_rate*dw
            self.bias -= self.learning_rate*db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias
    def test_mse(self,X_test,y_test):
        # returns Mean Square Error(y_a-y_pred)
        return np.mean((y_test-self.predict(X_test))**2)
    def plot(self,color="red"):
        x_ = np.linspace(-2, 2, 100)
        y_ = np.multiply(reg.weights,x_) + reg.bias
        plt.plot(x_, y_,color=color)
        


if __name__=="__main__":
    # Generating Data for Regression
    X,y = datasets.make_regression(n_samples=100,n_features=1,noise=20,random_state=1)
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
    
    fig = plt.figure(figsize=(8,6))
    plt.scatter(X[:,0],y,color="b",marker="o",s=30)    
    
    
    reg = LinearRegression(learning_rate=0.01,n_iter=10000)
    reg.fit(X_train,y_train)
    testing_error = reg.test_mse(X_test,y_test)
    print("Testing Error",testing_error)
    reg.plot("red")
    
    reg = LinearRegression(learning_rate=0.01, n_iter=100)
    reg.fit(X_train, y_train)
    testing_error = reg.test_mse(X_test, y_test)
    print("Testing Error", testing_error)
    reg.plot("Yellow")

    reg = LinearRegression(learning_rate=0.0001,n_iter=1000)
    reg.fit(X_train,y_train)
    testing_error = reg.test_mse(X_test,y_test)
    print("Testing Error",testing_error)
    reg.plot("orange")
    
    plt.show()
    
    
    
    
    
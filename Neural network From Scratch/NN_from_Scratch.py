import numpy as np


class Layer:
    """
    Building Block.
    Job:
        1. Process Input to Generate Output (Foward Prop)
        2. Propogate Gradients thorugh itseld (Backward Prop)  

    """

    def __init__(self):
        pass

    def forward(self, input):
        """
        params:
        --------------
        Takes input Data of Shape [Batch,input_units]
        --------------------------------------------------------

        returns:
        Output Data of Shape [Batch,output_units]
        --------------------------------------------------------
        """

        # A dummy layer returns whatever input it gets
        return input

    def backward(self, input, grad_output):
        """
        Discription:
        ---------------
        Performs a backprop step through the layer, w.r.t. given input
        --------------------------------------------------------



        params:
        ---------------
        Takes input Data of Shape [Batch,input_units]
        --------------------------------------------------------

        return:
        ---------------
        Output Data of Shape [Batch,output_units]
        --------------------------------------------------------
        """
        # To compute backprop w.r.t input we need to apply chain rule
        # d_loss / d_input = (d_loss/d_layer) * (d_layer/d_input)
        # We already have d_loss/d_layer from prev calculation
        # we just need to multiply it by (d_layer/d_input)

        # In case of parameters in layer (e.g. Dense Layer) we need
        # to update them using (d_loss/d_layer)

        # The Gradient of dummy layer is preciesly grad_output, but we'll
        # write it more explicitly
        num_units = input.shape[1]
        d_layer_d_input = np.eye(num_units)
        return np.dot(grad_output, d_layer_d_input)  # Chainrule


class ReLU(Layer):
    def __init__(self):
        # Relu Layer Simply Applies ElementWise operation to all inputs
        pass

    def forward(self, input):
        # Appliying ReLU to [batch,input_units] matrix
        return np.maximum(0, input)

    def backward(self, input, grad_output):
        # Relu gradient: 1 if x > 0 else 0
        relu_grad = input > 0

        # To return grad_output(previous grads) * relu_grad (current_grad)
        # print("Gradient",grad_output)
        return relu_grad * grad_output


class TanH(Layer):
    def __init__(self):
        # TanH Layer Simply Applies ElementWise operation to all inputs
        pass

    def forward(self, input):
        # Appliying TanH to [batch,input_units] matrix
        return (np.exp(input)-np.exp(-input))/(np.exp(input)+np.exp(-input))

    def backward(self, input, grad_output):
        # Relu gradient: 1 if x > 0 else 0
        relu_grad = 1-np.square(self.forward(input))

        # To return grad_output(previous grads) * tanh_grad (current_grad)
        # print("Gradient",grad_output)
        return relu_grad * grad_output


class SampleLayer(Layer):
    def __init__(self):
        pass

    def forward(self, input):
        pass

    def backward(self, input, grad_output):
        pass


class Dense(Layer):
    def __init__(self, input_units, output_units, learning_rate=0.000001):
        # A dense layer is a layer which a learned affine transformation : f(x)= W@X +b
        self.weights = np.random.normal(loc=0.0, scale=np.sqrt(
            2/(input_units+output_units)), size=(input_units, output_units))
        self.biases = np.zeros(output_units)
        self.learning_rate = learning_rate

    def forward(self, input):
        # Perform an affine transformation
        # f(x)= W@X +b

        # input_shape : [batch,input_shape]
        # output_shape : [batch,output_shape]

        return np.dot(input, self.weights) + self.biases

    def backward(self, input, grad_output):
        # Compute df/d_input = df/d_dense * d_dense/d_input
        # Where d_dense/d_input = Weights.T

        grad_input = np.dot(grad_output, self.weights.T)

        # compute gradient w.r.t. W and B
        grad_weights = np.dot(input.T, grad_output)
        grad_biases = grad_output.mean(axis=0)*input.shape[0]
        assert grad_weights.shape == self.weights.shape and grad_biases.shape == self.biases.shape

        # Here we update weights or say perform a SGD Step
        self.weights -= self.learning_rate*grad_weights
        self.biases -= self.learning_rate*grad_biases
        return grad_input


class Loss:
    @staticmethod
    def loss(y_pred, y_actual):
        """
        Computes Mean Squared error/loss between targets
        and predictions.
        Input: predictions (N, k) ndarray (N: no. of samples, k: no. of output nodes)
            targets (N, k) ndarray        (N: no. of samples, k: no. of output nodes)
        Returns: scalar
        """

        return np.sum(np.square(y_pred-y_actual)) / y_pred.shape[1]

    @staticmethod
    def grad_loss(y_pred, y_actual):
        """
        Computes mean squared error gradient between targets 
        and predictions. 
        Input: predictions (N, k) ndarray (N: no. of samples, k: no. of output nodes)
            targets (N, k) ndarray        (N: no. of samples, k: no. of output nodes)
        Returns: (N,k) ndarray

        """

        return 2*(y_pred-y_actual)/y_pred.shape[1]


class Network:
    def __init__(self):
        self.network = list()

    def add(self, layer):
        self.network.append(layer)

    def forward(self, X):
        # Compute Actiavtions of all layers by appling them sequentially
        # Return a list of activations for each layer
        activations = []
        # Initial input
        input = X

        # Looping to each layer: Forward Propogation
        for l in self.network:
            activations.append(l.forward(input))
            # Updating input to last layer output
            input = activations[-1]
        assert len(activations) == len(self.network)
        return activations

    def predict(self, X):
        # Compute network predictions
        # Return Last Layer Output
        return self.forward(X)[-1]

    def backward(self, grad_output):
        loss_grad = grad_output
        for layer_idx in reversed(range(len(self.network))):
            layer = self.network[layer_idx]
            # Grad w.r.t inputs gathered in fwd prop
            # Also does GD Step
            loss_grad = layer.backward(self.layer_inputs[layer_idx], loss_grad)

    def train(self, X, y):
        # Train on given Batch of X And y
        # Steps:
        #       1. Perform Forward Propogation
        #       2. Perform layer.backward from last to first
        #       Thus, After step 2. All dense layers have
        #       performed A Gradient Step

        # Step 1. Get the Activations [ Forward Propogation]
        layers_activation = self.forward(X)

        # layer_input[i] is input for layer i
        # Eg. for network[0] or say first hidden dense layer ->  layer_input[0] = X
        self.layer_inputs = [X] + layers_activation

        # Output from the network
        logits = layers_activation[-1]

        # Compute the loss and the Initial gradient
        # This Initial Gradient will help us to propogate backwards
        # Similar as X in forward propogation
        loss = Loss.loss(logits, y)
        grad_loss = Loss.grad_loss(logits, y)

        self.backward(grad_loss)

        return np.mean(loss)

    def __str__(self):
        string = ""
        for i, l in self.network:
            string += F"Layer: {i+1} -> {l}\n"
        return string


if __name__ == "__main__":
    pass

from copy import deepcopy

import numpy

from source.constants import SCAN_RADIUS, MOVES


class Brain:
    WEIGHTS_LENGTH = 16
    MUTATION_FACTOR = 4
    DECAY = 250

    def __init__(self) -> None:
        self._weights_ = [numpy.random.random_sample(((SCAN_RADIUS * 2 + 1) ** 2, self.WEIGHTS_LENGTH)),
                          # numpy.random.random_sample((self.WEIGHTS_LENGTH, self.WEIGHTS_LENGTH)),
                          numpy.random.random_sample((self.WEIGHTS_LENGTH, len(MOVES)))]
        self._biases_ = [numpy.random.random_sample((1, self.WEIGHTS_LENGTH)),
                         # numpy.random.random_sample((1, self.WEIGHTS_LENGTH)),
                         numpy.random.random_sample((1, len(MOVES)))]
        self._layers_ = [numpy.zeros((1, (SCAN_RADIUS * 2 + 1) ** 2)),
                         # numpy.zeros((1, self.WEIGHTS_LENGTH)),
                         numpy.zeros((1, self.WEIGHTS_LENGTH)), numpy.zeros((1,  len(MOVES)))]
        self._activations_ = [
            self.relu,
            # numpy.tanh,
            self.softmax]

    def forward(self, input_data: numpy.ndarray) -> int:
        if input_data.shape != self._layers_[0].shape:
            input_layer = input_data.reshape(self._layers_[0].shape).copy()
        else:
            input_layer = input_data.copy()

        numpy.copyto(self._layers_[0], input_layer)

        for index in range(len(self._weights_)):
            numpy.copyto(self._layers_[index + 1], self.dense(self._layers_[index], index))

        return self._layers_[-1].argmax()  # noqa

    def dense(self, input_data: numpy.ndarray, weights_index: int) -> numpy.ndarray:
        return self._activations_[weights_index](
            input_data.dot(self._weights_[weights_index]) + self._biases_[weights_index])

    def mutate(self, epoch: int) -> None:
        if epoch > self.DECAY * 5:
            return

        for weights, biases in zip(self._weights_, self._biases_):
            for weight in weights:
                weight[numpy.random.randint(len(weight), size=(len(weight) // self.MUTATION_FACTOR))] \
                    *= 1 - ((numpy.random.rand() * 4 - 2) / numpy.exp(epoch / self.DECAY))
            for bias in biases:
                bias[numpy.random.randint(len(bias), size=(len(bias) // self.MUTATION_FACTOR))] \
                    *= 1 - ((numpy.random.rand() * 4 - 2) / numpy.exp(epoch / self.DECAY))

    @property
    def weights(self) -> ...:
        return deepcopy(self._weights_), deepcopy(self._biases_)

    @weights.setter
    def weights(self, value: tuple[numpy.ndarray, ...]) -> None:
        self._weights_, self._biases_ = value

    @staticmethod
    def relu(x: numpy.array) -> numpy.ndarray:
        return numpy.maximum(0, x)

    @staticmethod
    def softmax(x: numpy.array):
        exp_x = numpy.exp(x - numpy.max(x))

        return exp_x / numpy.sum(exp_x)

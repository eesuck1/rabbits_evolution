import matplotlib.pyplot as plt
import numpy


def draw() -> None:
    t = numpy.arange(3000)
    w = numpy.full(t.shape, numpy.random.rand())

    y_1 = 1 - (1 / (1 + t / 250) ** 2)
    y_2 = 1 - 1 / numpy.exp(t / 250)

    w_1 = 10 * numpy.log10(w / (w * y_1))
    w_2 = 10 * numpy.log10(w / (w * y_2))

    plt.plot(w_1, label="W1")
    plt.plot(w_2, label="W2")

    plt.grid()
    plt.legend()
    plt.show()


if __name__ == '__main__':
    draw()

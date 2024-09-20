from source.constants import SCREEN_WIDTH, SCREEN_HEIGHT

import numpy


def get_random_coordinate() -> tuple[float, float]:
    return numpy.random.randint(0, SCREEN_WIDTH - 1), numpy.random.randint(0, SCREEN_HEIGHT - 1)

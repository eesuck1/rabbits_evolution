import random
import sys
from typing import Callable

import matplotlib.pyplot as plt
import pygame

pygame.init()
pygame.font.init()

from source.agent import Rabbit, Agent, Food, Fox
from source.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_WIDTH, WINDOW_HEIGHT, GRASS_COLOR
from source.utils import get_random_coordinate


class Simulation:
    def __init__(self, rabbits_number: int, foxes_number: int, food_number: int) -> None:
        self._screen_ = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._display_ = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._clock_ = pygame.time.Clock()

        self._rabbits_number_ = rabbits_number
        self._foxes_number_ = foxes_number
        self._food_number_ = food_number

        self._agents_: list[Agent, ...] | list = []
        self._agents_position_: dict[tuple[float, float], Agent] = {}
        self._epoch_ = 0

        self._font_ = pygame.font.SysFont("Arial", 24)

        self._counters_ = {
            "food": [],
            "rabbit": [],
            "fox": [],
        }

    def __del__(self) -> None:
        self.draw_end()

    def draw_end(self) -> None:
        plt.plot(self._counters_.get("food"), label="Food", color="green")
        plt.plot(self._counters_.get("rabbit"), label="Rabbit", color="gray")
        plt.plot(self._counters_.get("fox"), label="Fox", color="orange")

        plt.grid()
        plt.legend()
        plt.show()

    def fill_unit(self, class_to_fill: Callable, range_to_fill: int) -> None:
        for index in range(range_to_fill):
            unit = class_to_fill(self._agents_position_)

            while unit.position in self._agents_position_:
                unit.position = get_random_coordinate()

            self._agents_.append(unit)
            self._agents_position_[unit.position] = unit

    def fill_world(self) -> None:
        self.fill_unit(Rabbit, self._rabbits_number_)
        self.fill_unit(Food, self._food_number_)
        self.fill_unit(Fox, self._foxes_number_)

    def draw_world(self) -> None:
        self._screen_.fill(GRASS_COLOR)

        for agent in self._agents_:
            agent.draw(self._screen_)

    def move_agents(self) -> None:
        for agent in self._agents_:
            agent.move()

    def check_dead(self) -> None:
        for agent in self._agents_:
            if agent.is_dead:
                self._agents_.remove(agent)

                if agent.position in self._agents_position_:
                    del self._agents_position_[agent.position]

    def check_reproduce(self) -> None:
        for agent in self._agents_:
            if agent.can_reproduce:
                new_agent = type(agent)(self._agents_position_)

                if new_agent.brain:
                    new_agent.brain.weights = agent.brain.weights
                    new_agent.brain.mutate(self._epoch_)

                new_agent.position = (agent.position[0] + random.randint(-7, 7),
                                      agent.position[1] + random.randint(-7, 7))

                self._agents_.append(new_agent)
                self._agents_position_[new_agent.position] = new_agent

                agent.reproduce_done()

    def count_agents(self) -> None:
        food_counter = 0
        fox_counter = 0
        rabbit_counter = 0

        for agent in self._agents_:
            if isinstance(agent, Food):
                food_counter += 1
            elif isinstance(agent, Fox):
                fox_counter += 1
            else:
                rabbit_counter += 1

        # if rabbit_counter == 0 or fox_counter == 0:
        #     pygame.quit()
        #     sys.exit()

        self._counters_["food"].append(food_counter)
        self._counters_["fox"].append(fox_counter)
        self._counters_["rabbit"].append(rabbit_counter)

    def run(self) -> None:
        self.fill_world()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.fill_world()
                    if event.key == pygame.K_c:
                        self._agents_.clear()
                    if event.key == pygame.K_s:
                        self.draw_end()

            self.move_agents()
            self.check_dead()
            self.check_reproduce()
            self.count_agents()
            self.draw_world()

            self._display_.blit(pygame.transform.scale(self._screen_, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
            self._display_.blit(self._font_.render(f"Epoch: {self._epoch_}", True, (0, 0, 0)), (25, 25))
            self._clock_.tick(FPS)
            self._epoch_ += 1

            pygame.display.update()

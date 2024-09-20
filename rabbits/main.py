from source.simulation import Simulation


def main() -> None:
    simulation = Simulation(150, 150, 2500)
    simulation.run()


if __name__ == '__main__':
    main()

import abc

class Day(abc.ABC):

    @abc.abstractmethod
    def part1(self):
        pass

    @abc.abstractmethod
    def part2(self):
        pass
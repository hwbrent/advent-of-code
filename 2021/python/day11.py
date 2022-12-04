from utils import get_input
from typing import Iterator

'''
--- Day 11: Dumbo Octopus ---

You enter a large cavern full of rare bioluminescent dumbo octopuses! They
seem to not like the Christmas lights on your submarine, so you turn them
off for now.

There are 100 octopuses arranged neatly in a 10 by 10 grid. Each octopus
slowly gains energy over time and flashes brightly for a moment when its
energy is full. Although your lights are off, maybe you could navigate
through the cave without disturbing the octopuses if you could predict when
the flashes of light will happen.

Each octopus has an energy level - your submarine can remotely measure the
energy level of each octopus (your puzzle input). For example:

5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526

The energy level of each octopus is a value between 0 and 9. Here, the
top-left octopus has an energy level of 5, the bottom-right one has an
energy level of 6, and so on.

You can model the energy levels and flashes of light in steps. During a
single step, the following occurs:

• First, the energy level of each octopus increases by 1.
• Then, any octopus with an energy level greater than 9 flashes. This
  increases the energy level of all adjacent octopuses by 1, including
  octopuses that are diagonally adjacent. If this causes an octopus to
  have an energy level greater than 9, it also flashes. This process
  continues as long as new octopuses keep having their energy level
  increased beyond 9. (An octopus can only flash at most once per step.)
• Finally, any octopus that flashed during this step has its energy level
  set to 0, as it used all of its energy to flash.

Adjacent flashes can cause an octopus to flash on a step even if it begins
that step with very little energy. Consider the middle octopus with 1 energy
in this situation:

Before any steps:
11111
19991
19191
19991
11111

After step 1:
34543
40004
50005
40004
34543

After step 2:
45654
51115
61116
51115
45654

An octopus is highlighted when it flashed during the given step.

Here is how the larger example above progresses:

Before any steps:
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526

After step 1:
6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637

After step 2:
8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848

After step 3:
0050900866
8500800575
9900000039
9700000041
9935080063
7712300000
7911250009
2211130000
0421125000
0021119000

After step 4:
2263031977
0923031697
0032221150
0041111163
0076191174
0053411122
0042361120
5532241122
1532247211
1132230211

After step 5:
4484144000
2044144000
2253333493
1152333274
1187303285
1164633233
1153472231
6643352233
2643358322
2243341322

After step 6:
5595255111
3155255222
3364444605
2263444496
2298414396
2275744344
2264583342
7754463344
3754469433
3354452433

After step 7:
6707366222
4377366333
4475555827
3496655709
3500625609
3509955566
3486694453
8865585555
4865580644
4465574644

After step 8:
7818477333
5488477444
5697666949
4608766830
4734946730
4740097688
6900007564
0000009666
8000004755
6800007755

After step 9:
9060000644
7800000976
6900000080
5840000082
5858000093
6962400000
8021250009
2221130009
9111128097
7911119976

After step 10:
0481112976
0031112009
0041112504
0081111406
0099111306
0093511233
0442361130
5532252350
0532250600
0032240000

After step 10, there have been a total of 204 flashes. Fast forwarding, here
is the same configuration every 10 steps:

After step 20:
3936556452
5686556806
4496555690
4448655580
4456865570
5680086577
7000009896
0000000344
6000000364
4600009543

After step 30:
0643334118
4253334611
3374333458
2225333337
2229333338
2276733333
2754574565
5544458511
9444447111
7944446119

After step 40:
6211111981
0421111119
0042111115
0003111115
0003111116
0065611111
0532351111
3322234597
2222222976
2222222762

After step 50:
9655556447
4865556805
4486555690
4458655580
4574865570
5700086566
6000009887
8000000533
6800000633
5680000538

After step 60:
2533334200
2743334640
2264333458
2225333337
2225333338
2287833333
3854573455
1854458611
1175447111
1115446111

After step 70:
8211111164
0421111166
0042111114
0004211115
0000211116
0065611111
0532351111
7322235117
5722223475
4572222754

After step 80:
1755555697
5965555609
4486555680
4458655580
4570865570
5700086566
7000008666
0000000990
0000000800
0000000000

After step 90:
7433333522
2643333522
2264333458
2226433337
2222433338
2287833333
2854573333
4854458333
3387779333
3333333333

After step 100:
0397666866
0749766918
0053976933
0004297822
0004229892
0053222877
0532222966
9322228966
7922286866
6789998766

After 100 steps, there have been a total of 1656 flashes.

Given the starting energy levels of the dumbo octopuses in your cavern,
simulate 100 steps. How many total flashes are there after 100 steps?
'''

''' ****************************************************************** '''

class Octopus:
    '''
    - Each octopus slowly gains energy over time and flashes brightly for a moment when its energy is full.
    - Each octopus has an energy level.
    - The energy level of each octopus is a value between 0 and 9.
    - Any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent
    - An octopus can only flash at most once per step.
    - If an octopus flashed during a particular step, it has its energy level set to 0, as it used all of its energy to flash.
    '''

    def __init__(self,energy,i,j):
        self.energy = energy
        self.i = i
        self.j = j
        self.has_flashed_in_this_step = False

    def __str__(self) -> 'str':
        return str(self.energy)

    def increment(self) -> 'None':
        self.energy += 1

    def should_flash(self) -> 'bool':
        return self.energy > 9 and not self.has_flashed_in_this_step

    def flash(self, cavern: 'Cavern') -> 'None':
        '''
        - Any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent.
        - If this causes an octopus to have an energy level greater than 9, it also flashes.
        '''
        self.has_flashed_in_this_step = True
        cavern.flash_count += 1

        ##### Increase the energy level of all adjacent octopi by 1 #####
        for adjacent_octopus in cavern.get_adjacent(self):
            adjacent_octopus.increment()

        ##### Trigger adjacent octopi to flash (if eligible) #####
        for adjacent_octopus in cavern.get_adjacent(self):
            if adjacent_octopus.should_flash():
                adjacent_octopus.flash(cavern)

    def reset_energy(self) -> 'None':
        self.energy = 0

class Cavern:
    def __init__(self, input):
        self.input = input
        self.octopi = [[Octopus(energy,i,j) for j,energy in enumerate(row)] for i,row in enumerate(input)]
        self.flash_count = 0

    def __getitem__(self,key) -> 'Octopus|list[Octopus]':
        ''' Allow for indexing via tuple (e.g. `self[1,2]`) as well as solitary `int`. '''
        return self.octopi[key[0]][key[1]] if (type(key) == tuple) else self.octopi[key]

    def __str__(self):
        out = '\n'
        for row in self.octopi:
            out += "".join([str(octopus) for octopus in row])
            out += '\n'
        return out

    def step(self):
        '''
        You can model the energy levels and flashes of light in steps. During
        a single step, the following occurs:
        • First, the energy level of each octopus increases by 1.
        • Then, any octopus with an energy level greater than 9 flashes.
          This increases the energy level of all adjacent octopuses by 1,
          including octopuses that are diagonally adjacent. If this causes
          an octopus to have an energy level greater than 9, it also flashes.
          This process continues as long as new octopuses keep having their
          energy level increased beyond 9. (An octopus can only flash at most
          once per step.)
        • Finally, any octopus that flashed during this step has its energy
          level set to 0, as it used all of its energy to flash.
        '''

        ##### Increment each octopus' energy #####
        for row in self.octopi:
            for octopus in row:
                octopus.increment()

        ##### Trigger flashes #####
        for row in self.octopi:
            for octopus in row:
                if octopus.should_flash():
                    # Pass `self` so the octopus can use Cavern.get_adjacent
                    # and trigger those neighbouring octopi to increment
                    octopus.flash(self)
        
        ##### Reset flashed octopi's energy and flag #####
        for row in self.octopi:
            for octopus in row:
                if octopus.has_flashed_in_this_step == True:
                    octopus.has_flashed_in_this_step = False
                    octopus.reset_energy()

    def get_adjacent(self, param_octopus: 'Octopus' = None) -> 'Iterator[Octopus]':
        ''' Gets every `Octopus` adjacent to `param_octopus` (not including `param_octopus` itself). '''
        for i,row in enumerate(self.octopi):
            if not param_octopus.i in range(i-1,i+2):
                continue
            for j, cavern_octopus in enumerate(row):
                if not param_octopus.j in range(j-1,j+2):
                    continue
                if not cavern_octopus is param_octopus:
                    yield cavern_octopus

    # def increment_flash_count(self) -> 'None':
    #     self.flash_count += 1

''' ****************************************************************** '''

def part1(input):
    cavern = Cavern(input)
    for _ in range(100):
        cavern.step()
    print('Part 1 -->', cavern.flash_count)

''' ****************************************************************** '''

def part2(input):
    pass

''' ****************************************************************** '''

if __name__ == "__main__":
    input = [[int(num) for num in row] for row in get_input().strip().split("\n")]
    test_input = [
        [1,1,1,1,1],
        [1,9,9,9,1],
        [1,9,1,9,1],
        [1,9,9,9,1],
        [1,1,1,1,1]
    ]
    part1(input)
    part2(input)

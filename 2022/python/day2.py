from utils import get_input

'''
https://adventofcode.com/2022/day/2

--- Day 2: Rock Paper Scissors ---

The Elves begin to set up camp on the beach. To decide whose tent gets to
be closest to the snack storage, a giant Rock Paper Scissors tournament is
already in progress.

Rock Paper Scissors is a game between two players. Each game contains many
rounds; in each round, the players each simultaneously choose one of Rock,
Paper, or Scissors using a hand shape. Then, a winner for that round is
selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats
Rock. If both players choose the same shape, the round instead ends in a
draw.

Appreciative of your help yesterday, one Elf gives you an encrypted
strategy guide (your puzzle input) that they say will be sure to help you
win. "The first column is what your opponent is going to play: A for Rock,
B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is
called away to help with someone's tent.

The second column, you reason, must be what you should play in response:
X for Rock, Y for Paper, and Z for Scissors. Winning every time would be
suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score.
Your total score is the sum of your scores for each round. The score for a
single round is the score for the shape you selected (1 for Rock, 2 for
Paper, and 3 for Scissors) plus the score for the outcome of the round
(0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you
should calculate the score you would get if you were to follow the
strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should
choose Paper (Y). This ends in a win for you with a score of 8 (2 because
you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should
choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you
a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a
total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your
strategy guide?

--- Part Two ---

The Elf finishes helping with the tent and sneaks back over to you. "Anyway,
the second column says how the round needs to end: X means you need to lose,
Y means you need to end the round in a draw, and Z means you need to win.
Good luck!"

The total score is still calculated in the same way, but now you need to
figure out what shape to choose so the round ends as indicated. The example
above now goes like this:

In the first round, your opponent will choose Rock (A), and you need the round
to end in a draw (Y), so you also choose Rock. This gives you a score of
1 + 3 = 4.
In the second round, your opponent will choose Paper (B), and you choose Rock
so you lose (X) with a score of 1 + 0 = 1.
In the third round, you will defeat your opponent's Scissors with Rock for a
score of 1 + 6 = 7.
Now that you're correctly decrypting the ultra top secret strategy guide, you
would get a total score of 12.

Following the Elf's instructions for the second column, what would your total
score be if everything goes exactly according to your strategy guide?
'''

''' ****************************************************************** '''

# Converts a letter (e.g. 'X') to its equivalent shape (e.g. 'Rock').
letter_to_shape = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors"
}

# Converts a shape (e.g. 'Rock') to a numeric score.
shape_to_score = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3
}

# Converts a tuple of letters (e.g. ('A', 'Y')) to a numeric outcome for the left person.
letters_to_score = {
    ("A","X"): 0, # Rock - Rock -> left Draw
    ("A","Y"): -1, # Rock - Paper -> left Lose
    ("A","Z"): 1, # Rock - Scissors -> left Win

    ("B","X"): 1, # Paper - Rock -> left Win
    ("B","Y"): 0, # Paper - Paper -> Left Draw
    ("B","Z"): -1, # Paper - Scissors -> Left Lose

    ("C","X"): -1, # Scissors - Rock -> left Lose
    ("C","Y"): 1, # Scissors - Paper -> left Win
    ("C","Z"): 0, # Scissors - Scissors -> left 
}

# Converts a numeric outcome (e.g. 1) to a score (e.g. 6).
outcome_to_score = {
    1: 6, # Win
    0: 3, # Draw
    -1: 0, # Lose
}

def part1(input: 'list[str]') -> 'None':
    total = 0
    for line in input:
        left_letter, right_letter = line.split()

        right_shape_score = shape_to_score[letter_to_shape[right_letter]]
        right_outcome_score = outcome_to_score[letters_to_score[(left_letter,right_letter)]*-1]

        total += right_shape_score + right_outcome_score

    print('Part 1 ->', total)

''' ****************************************************************** '''

# Converts a letter (e.g. 'X' to an outcome (win/draw/lose) ONLY FOR THE PERSON ON THE RIGHT (e.g. -1)).
letter_to_outcome = {
    "X": -1,
    "Y": 0,
    "Z": 1
}

def get_right_letter(left_letter: 'str', right_outcome: 'int') -> 'str':
    '''
    i.e. Given the letter representing the shape that the left person used
    (e.g. Rock) and the outcome of the game, this function finds the letter
    corresponding to the shape that the right person had to have used in
    order to achieve this outcome
    '''
    for left, right in letters_to_score.keys():
        if left != left_letter:
            continue
        left_outcome = letters_to_score[(left, right)]
        if left_outcome == -1 * right_outcome:
            return right

def part2(input: 'list[str]') -> 'None':
    total = 0
    for line in input:
        left_letter, right_letter = line.split()

        # The outcome that MUST happen
        right_person_outcome = letter_to_outcome[right_letter]

        # So we know what shape the left person used.
        # And we know what their outcome was.
        # With those two bits of info, we can figure out
        # the person on the right's outcome and which
        # shape they used.

        right_person_shape = letter_to_shape[get_right_letter(left_letter, right_person_outcome)]
        right_person_shape_score = shape_to_score[right_person_shape]

        turn_score = right_person_shape_score + outcome_to_score[right_person_outcome]
        total += turn_score

    print('Part 2 ->', total)

if __name__ == '__main__':
    input = get_input().split("\n")
    part1(input)
    part2(input)

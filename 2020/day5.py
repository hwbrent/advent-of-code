# Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where 
# F means "front", B means "back", L means "left", and R means "right"
# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter
# tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in
# the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until
# you're left with exactly one row.

# F means "front", B means "back", L means "left", and R means "right"

# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter 
# tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in
# the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until 
# you're left with exactly one row

# Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357

# As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?

infile = open("5input.txt","r")

seats = []
for l in infile:
    if l.endswith("\n"):
        line = l[:-1]
    else:
        line = l
    #print(line)
    seats.append(line)

for i in seats:
    rowcode = i[:7] # letters specifying the row
    column = i[8:] # letters specifying the column

count = [1]
def func(rowcode):
    letter = rowcode[0]
    print(letter)
    rowcode = rowcode[count[0]:] # shortens the code
    #print(f" {rowcode}")

print("FBFBBFFRLR")
func("FBFBBFFRLR")

infile.close()

'''
Whole range: rows 0 through 127.
F - take lower half, keeping rows 0 through 63.
B - take upper half, keeping rows 32 through 63.
F means to take the lower half, keeping rows 32 through 47.
B means to take the upper half, keeping rows 40 through 47.
The final letter keeps the lower or higher of the two
'''
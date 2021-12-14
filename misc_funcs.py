

from random import randrange


# Define basic miscellaneous functions:


# return True if the colour at position in grid is equal to ref_colour
def same_colour_checker(position, grid, ref_colour):

    # Define bool to be returned
    colour_is_same = True

    # Iterate through the RGB values
    for i in range(3):
        # If the R/G/B value at the position in grid doesn't
        # match that of ref_colour, bool becomes false
        if(grid[int(position[0]), int(position[1]), i] != ref_colour[i]):
            colour_is_same = False

    return colour_is_same


# If the ant goes off the grid, "wrap it around" to the other side
def position_fixer(position, grid_size):

    # For each coordinate of the ant position,
    for pos_number in range(len(position)):

        # if the coordinate is larger than the grid size,
        if position[pos_number] >= grid_size:
            # subtract the grid size from the coordinate, so it
            # "goes to the other side"
            position[pos_number] -= grid_size

        # if the coordinate is negative,
        if position[pos_number] < 0:
            # Add the grid size to the coordinate, so it
            # "goes to the other side"
            position[pos_number] += grid_size

    return position


# Deals with negative indicies, and indicies larger than the length of the list
def index_corrector(list, wanted_index):

    # If the index is negative
    if (wanted_index <= 0):
        return list[-(abs(wanted_index) % len(list))]

    # If the index is greater than 0
    if (wanted_index > 0):
        return list[wanted_index % len(list)]


# Returns a list of colours (where each colour
# is a list of length 3 containing RGB values),
# given a required number of colours
def colour_maker(colour_num):

    # Empty list to contain the colours
    colours = []

    # Iterate through the number of required colours
    for colour in range(colour_num):
        # Make a list of three random numbers, and add it to colours
        colours.append([randrange(0, 250), randrange(0, 250),
                        randrange(0, 250)])

    return colours



import numpy as np


# Define functions for fixing the hexagonal grid problem:

"""
(This is a problem which arose because the hexagonal grid system which I
designed my functions with (https://en.wikipedia.org/wiki/Root_system) was
not the same as the one used by hexalattice, the external module used here
for image generation. More info about implementing hexagonal grids can be
found here: https://www.redblobgames.com/grids/hexagons/)
"""


# Takes a list, and shifts the elements one to the right. For example,
# [0,1,2,3] -> [3,0,1,2]
def shift_list_right(lst):

    # Last element becomes the first element, the second last element becomes
    # the last element, and everything in between is shifted
    shifted_list = np.array([lst[-1]] + [lst[i] for i in range(0, len(lst)-2)]
                            + [lst[-2]])

    return shifted_list


# Takes a list, and shifts the elements one to the left. For example,
# [0,1,2,3] -> [1,2,3,0]
def shift_list_left(lst):

    # Second element becomes the first element, the first element becomes the
    # last element, and everything else is shifted
    shifted_list = np.array([lst[1]] + [lst[i] for i in range(2, len(lst))]
                            + [lst[0]])

    return shifted_list


# "Fix" the hexagonal grid. This function is used before passing the grid array
# to the image generation functions.
def hex_grid_fixer(hex_grid):

    # For each row in the grid,
    for row_num in range(len(hex_grid)):

        # Shift the row to the right enough times so
        # that it moves half way across the grid
        for i in range(int((row_num+1)/2)):
            hex_grid[row_num] = shift_list_right(hex_grid[row_num])

    return hex_grid


# "Unfix" the hexagonal grid, i.e. undo the "fix" function above. This function
#  is used after passing the grid to the image generation functions, so the
# simulation remains unaffected.
def hex_grid_unfixer(hex_grid):

    # For each row in the grid,
    for row_num in range(len(hex_grid)):

        # Shift the row to the left enough times so
        # that it moves half way across the grid
        for i in range(int((row_num + 1)/2)):
            hex_grid[row_num] = shift_list_left(hex_grid[row_num])

    return hex_grid

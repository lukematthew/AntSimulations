

from misc_funcs import same_colour_checker, index_corrector


# Define functions for hexagonal ant movement:


# Point ant in the correct direction based on the colour of the hexagon
# it's on, then change the colour of the hexagon
def hex_ant_pointer(position, grid, bearing, colours, rules):

    # Go through all the colours in the colours list
    for colour in colours:

        # For each colour, check if it matches the
        # colour of the current hexagon
        if(same_colour_checker(position, grid, colour)):

            # If it does, get the colour's position in the colours list
            colour_index = colours.index(colour)

            # Appropriate change in bearing can be found in the rules list
            direction = rules[colour_index]

            # Change the direction the ant is facing
            bearing += direction

            # Change the colour of the current hexagon to
            # the next colour along in the colours list
            grid[int(position[0]), int(position[1])] = \
                index_corrector(colours, (colour_index + 1))

            return bearing


# Move ant based on the direction it's facing
def hex_ant_mover(bearing, position):

    if (bearing % 360 == 0):  # If bearing = 0, move upwards
        position[1] += 1

    if (bearing % 360 == 60):  # If bearing = 60,
        position[0] += 1       # move diagonally up to the right

    if (bearing % 360 == 120):  # If bearing = 120,
        position[0] += 1        # move diagonally down to the right
        position[1] -= 1

    if (bearing % 360 == 180):  # If bearing = 180, move downwards
        position[1] -= 1

    if (bearing % 360 == 240):  # If bearing = 240,
        position[0] -= 1        # move diagonally down to the left

    if (bearing % 360 == 300):  # If bearing = 300,
        position[0] -= 1        # move diagonally up to the left
        position[1] += 1

    return position

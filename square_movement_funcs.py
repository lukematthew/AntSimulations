

from misc_funcs import same_colour_checker, index_corrector


# Define functions for square ant movement:


# Move ant based on the direction it's facing
def ant_mover(bearing, position):

    if(bearing % 360 == 0):  # Move up if bearing = 0
        position[0] -= 1

    if(bearing % 360 == 90):  # Move right if bearing = 90
        position[1] += 1

    if (bearing % 360 == 180):  # Move down if bearing = 180
        position[0] += 1

    if (bearing % 360 == 270):  # Move left if bearing = 270
        position[1] -= 1

    return position


# Point ant in correct direction based on the colour of the square it's on,
# and change the colour of the current square.
def new_ant_pointer(position, grid, bearing, colours, rules):

    # Goes through all the colours
    for colour in colours:

        # For each colour, check if it matches the colour of the current square
        if(same_colour_checker(position, grid, colour)):

            # If it does, get the colour's position in the colours list
            colour_index = colours.index(colour)

            # Figure out which direction the colour corresponds to
            direction = rules[colour_index]

            # If it is a "left colour"
            if (direction == "L"):
                # Rotate ant direction 90 deg anticlockwise
                bearing -= 90

                # Set current square's colour to the next
                # colour along in the colours list
                grid[position[0], position[1]] = \
                    index_corrector(colours, (colour_index + 1))

                return bearing

            # If it is a "right colour"
            if (direction == "R"):
                # Rotate ant direction 90 deg clockwise
                bearing += 90

                # Set current square's colour to the next
                # colour along in the colours list
                grid[position[0], position[1]] = \
                    index_corrector(colours, (colour_index + 1))

                return bearing

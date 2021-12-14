# LUKE MATTHEW PROGRAMMING FOR GEOSCIENTISTS FINAL COURSEWORK #

# EXPLANATION #
"""
This program is based on Langton's ant (https://en.wikipedia.org/
wiki/Langton%27s_ant), but with some extensions. For example, you can run
multiple ants at once or add more complex movement patterns (Langton's ant
is the ant defined by "LR", which means go left for the first colour, and go
right for the second colour. Longer patterns, such as "LRRRRRLLR", allow for
more interesting results!).

I've also made the program work on a hexagonal
grid. This makes use of an external module called hexalattice (https://github.
com/alexkaz2/hexalattice), paired with matplotlib.

Finally, for both types of
grid, generation of a gif is possible, so you can watch how the ant(s) grow the
pattern over time! Keep in mind the functions used for the hexagonal grid are
quite computationally expensive, so parameters such as the number of frames
and the size of the grid will have to be limited compared to square grid runs,
unless your machine is very powerful.

The end result will be saved as output.png for the square grid, and shown as a
matplotlib plot for the hexagonal grid. If you ask for a gif, it will be saved
as mygif.gif.
"""

# import modules
import numpy as np
import imageio
from random import randrange
from hexalattice.hexalattice \
    import create_hex_grid, plot_single_lattice_custom_colors
import matplotlib.pyplot as plt
# You may need to install hexalattice before being able to run this script; run
# pip install hexalattice on mac!


# FUNCTION DEFINITIONS #

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


# Define functions for interpreting the rules from an input:

# START OF CODE FROM
# https://scipython.com/blog/langtons-ant-on-a-hexagonal-plane/
def parse_rules_string(s):

    # Each 'character' corresponds to a change in direction
    move_dict = {'N': 0, 'L2': -120, 'L1': -60, 'R1': 60, 'R2': 120, 'U': 180}
    rules = []
    i = 0

    # Takes a string such as "L2NNL1L2L1" and turns it into a list such as
    # [L2, N, N, L1, L2, L1]
    while i < len(s):
        t = s[i]
        if t in 'LR':
            i += 1
            t += s[i]
        try:
            rules.append(move_dict[t])
        except KeyError:
            raise ValueError('Unidentified move {} in rules {}'
                             .format(t, s))
        i += 1
    return rules
# END OF CODE FROM scipython.com


# Takes a square grid movement pattern such as "LRRL" and turns
# it into a list such as [L, R, R, L]
def square_rule_maker(movement_pattern):

    # Split the string into a list of letters
    movement_pattern_split = [letter for letter in movement_pattern]

    return movement_pattern_split


# Define functions which actually carry out the runs:

# Mega function which uses the functions defined above
# to run the square grid simulation
def square_run(runtime, ant_num, grid_size, make_gif,
               initial_pos, movement_pattern):

    # Make a list containing the movement pattern
    rules = square_rule_maker(movement_pattern)

    # Make a list containing the colours
    colours = colour_maker(len(rules))

    # Array which will be used as the main grid
    main_grid = np.zeros((grid_size, grid_size, 3), dtype=np.uint8)

    # Set all the squares in the grid to the first colour
    main_grid[:, :] = colours[0]

    # Dictionary to contain information about each ant
    master_dict = {}

    # For each ant, make an addition to the dictionary. Each addition is in
    # turn a dictionary, containing the position and direction of the ant.
    for ant in range(ant_num):
        master_dict.update({ant: {"ant_pos": initial_pos, "ant_direction": 0}})

    # Number of frames the gif will have. This can be changed, but making it
    # too small makes it hard to see what's happening, and making it too large
    # makes the gif feel slow.
    gif_frame_num = 100

    # Define variables for gif/image generation
    imagecounter = 0
    images = []
    imgs = []

    # Do the following for each iteration
    for iteration in range(runtime):

        # For each ant,
        for ant in range(ant_num):

            # Make sure ant hasn't gone off the grid - if it has,
            # wrap it around to the other side
            master_dict[ant]["ant_pos"] = \
                position_fixer(master_dict[ant]["ant_pos"], grid_size)

            # Update the direction the ant is facing
            master_dict[ant]["ant_direction"] = \
                new_ant_pointer(master_dict[ant]["ant_pos"], main_grid,
                                master_dict[ant]["ant_direction"],
                                colours, rules)

            # Update the position of the ant
            master_dict[ant]["ant_pos"] = \
                ant_mover(master_dict[ant]["ant_direction"],
                          master_dict[ant]["ant_pos"])

        # Every 10% through the total runtime, print a message
        if (iteration % (runtime/10) == 0):
            print("%g%% done..." % ((iteration/runtime) * 100))

        # If the user asked for a gif,
        if (make_gif is True):

            # Choose points through the runtime so the gif ends up
            # with the correct number of frames
            if (iteration % (runtime/gif_frame_num) == 0):

                # Generate an image with its frame number
                # (First frame is 0.png, second is 1.png...)
                imageio.imwrite("%s.png" % (imagecounter), main_grid)

                # Add the name of the image to a list
                imgs.append("%s.png" % (imagecounter))

                # Add one to counter
                imagecounter += 1

    # If the user asked for a gif,
    if (make_gif is True):

        # Following three lines are inspired by
        # a method shared by stackoverflow users
        # Almar and Matt Bierner (https://bit.ly/3ljOUGr)
        for filename in imgs:
            images.append(imageio.imread(filename))  # Add frames to "images"

        # Make gif from "images"
        imageio.mimsave(r"mygif.gif", images, fps=1200)

    # Generate an image of the final result, titled "output.png"
    imageio.imwrite("output.png", main_grid)

    # Message displayed to show everything is done
    print("Finished!")


# Mega function which uses the functions defined above
# to run the hexagonal grid simulation
def hex_run(runtime, ant_num, grid_size, make_gif,
            initial_pos, movement_pattern):

    # Create the movement ruleset from the input string
    rules = parse_rules_string(movement_pattern)

    # Make a list containing the colours
    colours = colour_maker(len(rules))

    # Dictionary to contain information about each ant
    master_dict = {}

    # Array which will be used as the main grid
    main_grid = np.zeros((grid_size, grid_size, 3), dtype=np.uint8)

    # Set all the squares in the grid to the first colour
    main_grid[:, :] = colours[0]

    # For each ant, make an addition to the dictionary. Each addition is in
    # turn a dictionary, containing the position and direction of the ant.
    for ant in range(ant_num):
        master_dict.update({ant: {"ant_pos": initial_pos, "ant_direction": 0}})

    # Number of frames the gif will have. This can be changed, but making it
    # too small makes it hard to see what's happening, and making it too large
    # makes the gif feel slow.
    gif_frame_num = 10

    # Define variables for gif/image generation
    imagecounter = 0
    images = []
    imgs = []

    # Code recommended by the hexalattice wiki
    # (https://github.com/alexkaz2/hexalattice/wiki) for setting
    # up the base for the hexagonal grid
    hex_centers, _ = create_hex_grid(nx=grid_size,
                                     ny=grid_size,
                                     do_plot=False)
    x_hex_coords = hex_centers[:, 0]
    y_hex_coords = hex_centers[:, 1]
    # End of code from hexalattice wiki

    # Do the following for each iteration
    for iteration in range(runtime):

        # For each ant,
        for ant in range(ant_num):

            # Check if the ant has gone out of the grid - if it has,
            # wrap it around to the other side
            master_dict[ant]["ant_pos"] = position_fixer(master_dict
                                                         [ant]["ant_pos"],
                                                         grid_size)

            # Update the direction the ant is facing
            master_dict[ant]["ant_direction"] = \
                hex_ant_pointer(master_dict[ant]["ant_pos"],
                                main_grid, master_dict[ant]["ant_direction"],
                                colours, rules)

            # Update the position of the ant
            master_dict[ant]["ant_pos"] = \
                hex_ant_mover(master_dict[ant]["ant_direction"],
                              master_dict[ant]["ant_pos"])

        # Every 10% through the runtime, print a message
        if (iteration % (runtime/10) == 0):
            print("%g%% done..." % ((iteration/runtime) * 100))

        # If the user asked for a gif,
        if (make_gif is True):

            # Choose points through the runtime so the gif ends
            # up with the correct number of frames
            if (iteration % (runtime/gif_frame_num) == 0):

                # Temporarily "fix" the grid, so it shows up correctly
                # in the images generated
                main_grid = hex_grid_fixer(main_grid)

                # Reshape the main grid into the format required by hexalattice
                colors = main_grid.reshape(grid_size**2, 3)

                # Divide all the RGB values by 250
                # (hexalattice requires them to be between 0 and 1)
                colors = np.multiply(colors, 1/250)

                # Plot array onto hexagonal grid
                plot_single_lattice_custom_colors(x_hex_coords, y_hex_coords,
                                                  face_color=colors,
                                                  edge_color=colors,
                                                  min_diam=0.9,
                                                  plotting_gap=0.05,
                                                  rotate_deg=0)

                # Save the figure with its frame number as its name
                # (First frame is "0.png", second frame is "1.png"...)
                plt.savefig('%s.png' % (imagecounter))

                # Add the image name to a list
                imgs.append("%s.png" % (imagecounter))

                # Add 1 to the counter
                imagecounter += 1

                # "unfix" the grid, so the run is unaffected
                main_grid = hex_grid_unfixer(main_grid)

                # Close the figure, as it is no longer needed
                plt.clf()

    # If the user asked for a gif,
    if (make_gif is True):

        # go through all the frames
        for filename in imgs:

            # and add them to "images"
            images.append(imageio.imread(filename))

        # Make a gif from the frames in "images"
        imageio.mimsave(r"mygif.gif", images, fps=1200)

    # If the user didn't ask for a gif, just generate a figure of the
    # final result and show it with matplotlib
    if (make_gif is False):
        main_grid = hex_grid_fixer(main_grid)
        colors = main_grid.reshape(grid_size**2, 3)
        colors = np.multiply(colors, 1/250)
        plot_single_lattice_custom_colors(x_hex_coords, y_hex_coords,
                                          face_color=colors,
                                          edge_color=colors,
                                          min_diam=0.9,
                                          plotting_gap=0.05,
                                          rotate_deg=0)
        plt.show()

    # Print a message to make it clear when everything is finished
    print("Finished!")


# Define user input functions:

# Asks the user whether they want a square run or a hexagonal run
def ask_for_run_type():

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Take user input
            user_input = input(
                "Enter 'h' for a hexagonal grid, or 's' for a square grid: ")

            # bool to be returned
            sim_is_hex = bool()

            # If user asks for hexagonal, set bool to true, and end loop
            if (user_input == "h"):
                sim_is_hex = True
                iteration = False
                return sim_is_hex

            # If user asks for square, set bool to false, and end loop
            elif (user_input == "s"):
                sim_is_hex = False
                iteration = False
                return sim_is_hex

            # If user inputs something else, raise an error
            else:
                raise ValueError()

        # If error, print warning
        except ValueError:
            print("Input must be 'h' or 's'.\n")


# Checks if the movement pattern given by the user is suitable
def square_pattern_check(user_pattern):

    # If input is empty, raise error
    if (user_pattern == ""):
        raise ValueError()

    # Go through the letters in the input
    for character in user_pattern:

        # If the letter isn't L or R, raise an error
        if (character != "L" and character != "R"):
            raise ValueError()


# Asks the user for a movement pattern (for square run)
def ask_for_square_pattern():

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Take input from the user
            user_pattern = input("\nEnter a string of 'L's and 'R's: ")

            # Check if the input is suitable
            square_pattern_check(user_pattern)

            # Stop iteration, and return user input
            iteration = False
            return user_pattern

        # If error, print a warning
        except ValueError:
            print("Movement pattern must be a string of" +
                  " 'L's and 'R's, such as LRRRRRLLR. ")


# Asks the user for a movement pattern (for hexagonal run)
def ask_for_hex_pattern():

    # Explain what can be input
    print("\nA hexagonal movement pattern can take the following:\n\
          'N', 'R1', 'R2', 'U', 'L2', 'L1'.\n")

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Take user input
            user_pattern = input("Enter a hexagonal movement pattern string: ")

            # Try putting the user input through the parse_rules_string
            # function, as it raises a ValueError if input is unsuitable
            parse_rules_string(user_pattern)

            # End iteration, and return result
            iteration = False
            return user_pattern

        # If error, print a warning
        except ValueError:
            print("Must be a suitable pattern, such as R1R2NUR2R1L2.\n")


# Ask the user if they want a gif or not
def ask_for_gif():

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Take user input
            user_input = input("Would you like to make a gif? (y/n): ")

            # Bool to be returned
            make_gif = bool()

            # If the user says yes
            if (user_input == "y" or user_input == "Y"):

                # Set bool to true, end iteration and return result
                make_gif = True
                iteration = False
                return make_gif

            # If the user says no
            elif (user_input == "n" or user_input == "N"):

                # Set bool to false, end iteration and return result
                make_gif = False
                iteration = False
                return make_gif

            # If the user inputs something unsuitable, raise error
            else:
                raise ValueError()

        # If error, print a warning
        except ValueError:
            print("Input must be 'y' or 'n'.\n")


# Warns the user if the number of ants is large, and gives them the
# option to continue or change the number
def custom_antnum_warning(user_input):

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Ask user if they want to go ahead
            keep_going = input("%g is a lot of ants! Are you sure you want" +
                               " to continue? (y/n): " % user_input)

            # Bool to be returned
            keep_going_bool = bool()

            # If the user says yes
            if (keep_going == "y" or keep_going == "Y"):

                # Set the bool to true, end iteration and return result
                keep_going_bool = True
                iteration = False
                return keep_going_bool

            # If the user says no
            elif (keep_going == "n" or keep_going == "N"):

                # Set the bool to False, and return result
                keep_going_bool = False
                return keep_going_bool

            # If user input is unsuitable, raise error
            else:
                raise ValueError()

        # If error, print a warning
        except ValueError:
            print("Input must be 'y' or 'n'. \n")


# Ask the user for the number of ants they want
def ask_for_antnum():

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Bool to be used later
            keep_going_bool = False
            while (keep_going_bool is False):

                # Take user input
                user_input = int(input("\nHow many ants would you like? "))

                # If user inputs negative number, raise error
                if (user_input <= 0):
                    raise ValueError()

                # If user input is large
                elif (user_input > 10):

                    # Use function to make sure if user is sure about what
                    # they're doing, and set bool accordingly
                    keep_going_bool = custom_antnum_warning(user_input)

                    # If user wants to continue,
                    if (keep_going_bool is True):

                        # End iteration and return result
                        iteration = False
                        return user_input

                # If user input wasn't either negative or too big,
                # simply return it
                else:
                    return user_input

        # If error, print a warning
        except ValueError:
            print("Number of ants must be an integer greater than 0.\n")


# Warns the user if grid size is large, and gives them the
# option to continue or enter a new number
def custom_gridsize_warning(user_input):

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Ask user if they want to continue
            keep_going = input("%g is a large grid size! Are you sure you" +
                               " want to continue? (y/n): " % user_input)

            # Define bool to be returned
            keep_going_bool = bool()

            # If user says yes
            if (keep_going == "y" or keep_going == "Y"):

                # Set bool to true, end iteration and return result
                keep_going_bool = True
                iteration = False
                return keep_going_bool

            # If user says no
            elif (keep_going == "n" or keep_going == "N"):

                # Set bool to false and return result
                keep_going_bool = False
                return keep_going_bool

            # If user inputs something unsuitable, raise error
            else:
                raise ValueError()

        # If error, print a warning
        except ValueError:
            print("Input must be 'y' or 'n'. \n")


# Asks the user for the grid size they want
def ask_for_gridsize():

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Bool to be used later
            keep_going_bool = False
            while (keep_going_bool is False):

                # Take user input
                user_input = int(input("\nWhat would you like" +
                                       " your grid size to be? "))

                # If user input is negative, raise error
                if (user_input <= 0):
                    raise ValueError()

                # If user input is large, call warning function to
                # confirm if they want to continue
                elif (user_input >= 1000):
                    keep_going_bool = custom_gridsize_warning(user_input)

                    # If user wants to continue, end
                    # iteration and return result
                    if (keep_going_bool is True):
                        iteration = False
                        return user_input

                # If user inputs something not negative or large, return result
                else:
                    return user_input

        # If error, print a warning
        except ValueError:
            print("Grid size must be an integer greater than 0.\n")


# Warns the user if the runtime is very long, and gives them
# the option to continue or enter a different number.
def custom_runtime_warning(user_input):

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Ask user if they want to continue
            keep_going = input("%g is a long runtime! Are you sure you want" +
                               "to continue? (y/n): " % user_input)

            # Define bool to be returned
            keep_going_bool = bool()

            # If the user says yes, set bool to true, end
            # iteration and return result
            if (keep_going == "y" or keep_going == "Y"):
                keep_going_bool = True
                iteration = False
                return keep_going_bool

            # If the user says no, set bool to false and return result
            elif (keep_going == "n" or keep_going == "N"):
                keep_going_bool = False
                return keep_going_bool

            # Raise error if user inputs something unsuitable
            else:
                raise ValueError()

        # If error, print a warning
        except ValueError:
            print("Input must be 'y' or 'n'. \n")


# Asks the user for the runtime they want
def ask_for_runtime():

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Bool to be used later
            keep_going_bool = False
            while (keep_going_bool is False):

                # Take user input
                user_input = int(input("Please enter the runtime: "))

                # Raise error if input is negative
                if (user_input <= 0):
                    raise ValueError()

                # If user input is large, call warning function to
                # confirm if they want to continue
                elif (user_input > 2000000):
                    keep_going_bool = custom_runtime_warning(user_input)

                    # If user wants to keep going, end iteration
                    # and return result
                    if (keep_going_bool is True):
                        iteration = False
                        return user_input

                # If user inputs something not negative or too
                # large, return input
                else:
                    return user_input

        # If error, print a warning
        except ValueError:
            print("Runtime must be an integer greater than 0.\n")


# Main function for setting the initial position of the ant(s)
def init_position_setter(ant_num, grid_size):

    # If there is only one ant, user can choose where they want it to start
    if (ant_num == 1):
        user_choice = ant_position_chooser(grid_size)
        return user_choice

    # If there are multiple ants, they all start at random positions
    else:
        return [int(randrange(grid_size)), int(randrange(grid_size))]


# Lets user choose starting position of the ant
def ant_position_chooser(grid_size):

    # Bool to keep asking until an answer is reached
    iteration = True
    while (iteration is True):
        try:

            # Take user input
            user_input = input("Enter 'r' for a random position, " +
                               "'c' to start in the centre, or 'i' to " +
                               "start in a custom position: ")

            # If user asks for random starting position, end
            # iteration and return a random positoin
            if (user_input == "r"):
                iteration = False
                return [randrange(grid_size), randrange(grid_size)]

            # If user asks to start in the centre, end iteration
            # and return central position
            elif (user_input == "c"):
                iteration = False
                return [int(grid_size/2), int(grid_size/2)]

            # If user asks to specify position,
            # call the custom_coords function
            elif (user_input == "i"):
                user_coords = custom_coords(grid_size)
                iteration = False
                return user_coords

            # If the user inputs something else, raise an error
            else:
                raise ValueError()

        # If error, print a warning
        except ValueError:
            print("Input must be 'r', 'c' or 'i'.\n")


# Gets the user to input a custom starting position on the grid
def custom_coords(grid_size):

    # Bool to keep asking until an answer is reached
    iteration1 = True
    while (iteration1 is True):
        try:

            # Ask the user to input the first coordinate
            first_coord = int(input("Enter the first coordinate: "))

            # If coordinate is negative, raise error
            if (first_coord < 0):
                raise ValueError()

            # If coordinate is outside the grid, raise error
            elif (first_coord >= grid_size):
                raise IndexError()

            # If neither of the above, input is suitable so end iteration
            else:
                iteration1 = False

        # If error, print a warning
        except ValueError:
            print("Coordinate must be an integer between 0 and grid bound.\n")

        # If error, print a warning
        except IndexError:
            print("Your input is greater than the max grid size!\n")

    # Bool to keep asking until an answer is reached
    iteration2 = True
    while (iteration2 is True):
        try:

            # Ask the user to input the second coordinate
            second_coord = int(input("Enter the second coordinate: "))

            # If coordinate is negative, raise error
            if (second_coord < 0):
                raise ValueError()

            # If coordinate is outside the grid, raise error
            elif (second_coord >= grid_size):
                raise IndexError()

            # If neither of the above, input is suitable so end iteration
            else:
                iteration2 = False

        # If error, print a warning
        except ValueError:
            print("Coordinate must be an integer between 0 and grid bound.\n")

        # If error, print a warning
        except IndexError:
            print("Your input is greater than the max grid size!\n")

    # Return the starting position
    return ([first_coord, second_coord])


# END OF FUNCTION DEFINITIONS #

# MAIN #

# Bool which determines the type of run (square or hexagonal).
# False for a square grid run, and True for a hexagonal grid run.
sim_is_hex = ask_for_run_type()

# The movement pattern for the run. For a square grid run, this is a string of
# 'R's and 'L's, such as "LRRRRRLLR". For a hexagonal grid run, this is a
# string of 'N's, 'R1's, 'R2's, 'U's, 'L2's and 'L1's, such as "L1L2NUL2L1R2"
if (sim_is_hex is False):
    movement_pattern = ask_for_square_pattern()

elif (sim_is_hex is True):
    movement_pattern = ask_for_hex_pattern()

# Decide whether a gif will be made or not
make_gif = ask_for_gif()

# Choose the number of ants
ant_num = ask_for_antnum()

# Set the size of the grid
grid_size = ask_for_gridsize()

# Decides the initial positon of the ant(s). If there are multiple ants,
# random positions are chosen for each one. If there is only one ant, the
# user can choose whether they want the ant to start in the centre of the
# grid or a random position. They can also choose a custom position on
# the grid.
initial_pos = init_position_setter(ant_num, grid_size)

# Set the run time
runtime = ask_for_runtime()

# If a square run is selected
if (sim_is_hex is False):

    # Carry out a square run
    square_run(runtime, ant_num, grid_size, make_gif,
               initial_pos, movement_pattern)

# If a hexagonal run is selected
elif (sim_is_hex is True):

    # Carry out a hexagonal run
    hex_run(runtime, ant_num, grid_size, make_gif,
            initial_pos, movement_pattern)

# END OF MAIN #

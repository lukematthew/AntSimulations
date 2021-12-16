

from rule_maker_funcs import parse_rules_string
from random import randrange

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
            keep_going = input("%g is a lot of ants! " % user_input +
                               "Are you sure you want to continue? (y/n): ")

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
            keep_going = input("%g is a large grid size! " % int(user_input) +
                               "Are you sure you want to continue? (y/n): ")

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
            keep_going = input("%g is a long runtime! " % user_input +
                               "Are you sure you want to continue? (y/n): ")

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
            user_input = input("\nEnter 'r' for a random position, " +
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



from rule_maker_funcs import square_rule_maker, parse_rules_string
from misc_funcs import colour_maker, position_fixer
from square_movement_funcs import new_ant_pointer, ant_mover
from hexagonal_movement_funcs import hex_ant_mover, hex_ant_pointer
from grid_problem_funcs import hex_grid_fixer, hex_grid_unfixer
import numpy as np
import imageio
import matplotlib as plt
from hexalattice.hexalattice \
    import create_hex_grid, plot_single_lattice_custom_colors


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

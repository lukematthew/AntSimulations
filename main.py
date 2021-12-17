

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

# WARNING FOR MARKER: please install an external module called hexalattice!

# import functions
from user_input_funcs import ask_for_antnum, ask_for_gif, ask_for_gridsize,\
     ask_for_hex_pattern, ask_for_square_pattern, ask_for_run_type, \
     init_position_setter, ask_for_runtime
from execution_funcs import square_run, hex_run


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
initial_pos_list = []
for i in range(ant_num):
    initial_pos_list.append(init_position_setter(ant_num, grid_size))

# Set the run time
runtime = ask_for_runtime()

# If a square run is selected
if (sim_is_hex is False):

    # Carry out a square run
    square_run(runtime, ant_num, grid_size, make_gif,
               initial_pos_list, movement_pattern)

# If a hexagonal run is selected
elif (sim_is_hex is True):

    # Carry out a hexagonal run
    hex_run(runtime, ant_num, grid_size, make_gif,
            initial_pos_list, movement_pattern)


# END OF MAIN #

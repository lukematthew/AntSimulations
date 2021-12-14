# AntSimulations
Creation of images and gifs of runs of Langton's ant extended to multiple colours, ants, including a hexagonal grid system.

# Explanation
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

# To use
Please run main.py, with all the other files in the same directory. Alternatively, ant_full_script.py is a single document containing all of the others.
Warning: The scripts may make use of Python modules you haven't installed, such as hexalattice.

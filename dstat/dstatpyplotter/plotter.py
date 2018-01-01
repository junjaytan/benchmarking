"""Utility functions for plotting results using matplotlib."""
import matplotlib.pyplot as plt
import numpy as np


def create_line_graph(data, labels, title=None, legend_loc='upper right'):
    """Create a line graph with one or more lines.

    Example:
        t = np.arange(0., 5., 0.2)
        t2 = np.arange(0., 5.6, 0.2)
        mystuff = [t, t, t2, t2**2, t, t**3]
        legend = ('No mask', 'Masked if > 0.5', 'Masked if < -0.5')
        title = 'Line graph demo'
        create_line_graph(mystuff, legend, title)

    Args:
        data: A list of x, y vectors. E.g., for 3 lines you would provide
              list [x1, y1, x2, y2, x3, y3].
        labels: A tuple of strings corresponding to each line.
        title: String representing title of graph.
        legend_loc: String specifying legend location

    Returns:
        Nothing
    """

    # TODO: Probably need to add some error checking of dimensions and
    # such.
    plt.plot(*data)
    # TODO: Add functionality to shut off legend
    plt.legend(labels, loc='upper right')
    if title:
        plt.title(title)
    plt.show()

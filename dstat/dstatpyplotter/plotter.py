"""Utility functions for plotting results using matplotlib."""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def create_line_graph(data, labels, title=None, legend_loc='upper right',
                      x_lims=None, y_lims=None):
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
        x_lims: A two element tuple or list representing min/max limits for
                x-axis. Use None for an element if you only care about setting
                one of these.
        y_lims: A two element tuple or list representing min/max limits for
                y-axis. Use None for an element if you only care about setting
                one of these.

    Returns:
        Nothing
    """

    # TODO: Probably need to add some error checking of dimensions and
    # such.
    fig, ax = plt.subplots()
    ax.plot(*data)
    # TODO: Add functionality to shut off legend
    plt.legend(labels, loc='upper right')
    if title:
        plt.title(title)
    # TODO: Add more options to revise x-axis format. Currently shows integer
    #       values but might want to support actual timestamps
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%1i'))
    if x_lims:
        if len(x_lims) != 2:
            raise ValueError('x_lims must have two elements')
        ax.set_xlim(bottom=x_lims[0], top=x_lims[1])
    if y_lims:
        if len(y_lims) != 2:
            raise ValueError('y_lims must have two elements')
        ax.set_ylim(bottom=y_lims[0], top=y_lims[1])
    plt.show()

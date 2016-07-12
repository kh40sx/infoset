#!/usr/bin/env python3
"""FCGI script to show customer trend data."""

import datetime
import numpy as np

# MatPlotLib imports. No pop up windows on a web server (order important)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors

# Import Colovore libraries
from infoset.db import db_data

__author__ = 'peter@colovore.com (Peter Harrison)'


class Chart(object):
    """Class to create charts.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx, config, start=None, stop=None):
        """Function for intializing the class.

        Args:
            idx: idx of datapoint
            config: Config object
            start: Starting timestamp
            stop: Ending timesta

        Returns:
            None

        """
        # Get data as dict
        datapointer = db_data.GetIDX(idx, config, start=start, stop=stop)
        self.data = datapointer.everything()

    def single_line(self, title, label, color, filepath):
        """Create chart from data.

        Args:
            label: Label for line in chart
            color: Color of chart
            filepath: Name of output file

        Returns:
            None

        """
        # Initialize key variables
        lines2plot = []
        labels = []

        # Get global parameters
        parameters = _image_parameters(None)

        #####################################################################
        #
        # Create Charts
        #
        #####################################################################

        # Create chart object
        fig, axes = plt.subplots()

        # Convert data dict to two lists for matplotlib
        (x_values, y_values) = _timestamps2dates(self.data)

        # Create chart
        _chart_setup(fig, axes, parameters, ymax=max(y_values))

        # Define chart labels
        axes.set_xlabel(
            'Date / Time', color=parameters['text_color'],
            size=parameters['font_size_label'])
        axes.set_ylabel(
            'Values', color=parameters['text_color'],
            size=parameters['font_size_label'])

        # Create chart.
        data_line = _chart_generic(
            (x_values, y_values), axes, color, fill=True)
        lines2plot.append(data_line)
        labels.append(label)

        # Create legend
        fig.legend(
            tuple(lines2plot), tuple(labels),
            loc='lower center', fontsize=10, ncol=2, frameon=False)

        # Define chart title
        axes.set_title(
            title,
            size=parameters['font_size_title'], y=1.01)

        # Create image file
        fig.savefig(filepath)

        # Close figure to conserve memory
        plt.close(fig)


def _chart_generic(power, axes, line_color, fill=True):
    """Return total power consumption over time period as PNG HTML link.

    Args:
        power: Tuple of lists of data to plot
        axes: Matplotlib axis object
        line_color: Image parameters
        fill: Fill in under the line if True

    Returns:
        plot_line: Plot plot_line for creating a legend

    """
    # Convert power dict to two lists for matplotlib
    (x_values, y_values) = power

    #####################################################################
    #
    # Create Charts
    #
    #####################################################################

    # Create chart plot object (Array)
    plot_line, = axes.plot(
        x_values, y_values, line_color, linewidth=1)

    #####################################################################
    # Gradient fill under line (start)
    #####################################################################
    if fill is True:

        # Get limits of X and Y axis values
        xmin = min(x_values)
        xmax = max(x_values)
        ymin = 0
        ymax = max(y_values)

        # Create an object that will be used to gradient fill under the line
        fill_color = plot_line.get_color()
        zorder = plot_line.get_zorder()
        alpha = plot_line.get_alpha()
        alpha = 1.0 if alpha is None else alpha
        gradient = np.empty((100, 1, 4), dtype=float)
        rgb = mcolors.colorConverter.to_rgb(fill_color)
        gradient[:, :, :3] = rgb
        gradient[:, :, -1] = np.linspace(0, alpha, 100)[:, None]

        # Magic to create a polygon shaped area under the curve. This will
        # be used as a bitmap mask later
        column_stacked_array = np.column_stack(
            [x_values, y_values])
        vstacked_array = np.vstack(
            [[xmin, ymin], column_stacked_array, [xmax, ymin], [xmin, ymin]])
        clip_path = Polygon(
            vstacked_array, facecolor='none', edgecolor='none', closed=True)
        axes.add_patch(clip_path)

        # Plot data, with gradient shading that only exposes
        # what the mask allows
        axes.imshow(
            gradient,
            aspect='auto',
            origin='lower',
            zorder=zorder,
            interpolation="bicubic",
            clip_path=clip_path, clip_on=True,
            extent=[xmin, xmax, 0, ymax])

        #####################################################################
        # Gradient fill under line (stop)
        #####################################################################

    # Return
    return plot_line


def _chart_setup(fig, axes, parameters, ymin=0, ymax=None):
    """Do basic chart setup.

    Args:
        fig: Matplotlib figure object
        axes: Matplotlib axis object
        parameters: Image parameters to use
        ymin: Minimum Y value
        ymax: Maximum Y value

    Returns:
        plot_line: Plot plot_line for creating a legend

    """
    # Start y-axis at zero, versus autoscaling to lowest Y value
    if ymax is None:
        axes.set_ylim(ymin=ymin)
    else:
        axes.set_ylim(ymin=ymin, ymax=ymax)

    # Turn on autoscaling for X axis
    axes.autoscale_view()

    # Auto rotate x-axis labels if too big
    fig.autofmt_xdate()

    # Set figure size
    fig.set_size_inches(
        parameters['image_width'], parameters['image_height'])

    # Define how dates are placed on the x-axis
    xtick_locator = mdates.AutoDateLocator()
    xtick_formatter = mdates.AutoDateFormatter(xtick_locator)
    axes.xaxis.set_major_locator(xtick_locator)
    axes.xaxis.set_major_formatter(xtick_formatter)

    # Tick label colors
    axes.tick_params(
        colors=parameters['text_color'],
        labelsize=parameters['font_size_tick'])

    # Turn on grid lines
    axes.grid(True, color=parameters['text_color'], linestyle='-')


def _image_parameters(parameters):
    """Return dict of parameters for charts.

    Args:
        parameters: Matplotlib graph parameters

    Returns:
        values: Dict of new parameters

    """
    # Define parameters
    defaults = {
        'font_size_label': 15,
        'font_size_title': 20,
        'font_size_tick': 10,
        'text_color': '#808080',
        'line_color': '#000000',
        'max_color': '#FF0000',
        'commit_color': '#0000FF',
        'image_width': 8,
        'image_height': 8
    }
    values = {}

    # Process parameters
    if isinstance(parameters, dict) is False:
        return defaults
    else:
        for key in defaults.keys():
            values[key] = defaults[key]
        for key in parameters.keys():
            values[key] = parameters[key]

    # Return
    return values


def _timestamps2dates(data):
    """Convert dict keyed by timestamp to tuple of two lists.

    Args:
        data: Dict of values keyed by timestamp

    Returns:
        (x_values (datetime instances), y_values (dict values)

    """
    # Initialize key variables
    y_values = []
    x_timestamps = []

    # Convert data dict to two lists for matplotlib
    for key, value in sorted(data.items()):
        y_values.append(value)
        x_timestamps.append(key)

    # Convert timestamp list to a list of datetime objects
    dates = [
        datetime.datetime.fromtimestamp(
            timestamp) for timestamp in x_timestamps]
    x_values = mdates.date2num(dates)

    # Return
    return (x_values, y_values)

#!/usr/bin/env python3
"""FCGI script to show customer trend data."""

import datetime
import io
import pprint
import numpy as np

# MatPlotLib imports. No pop up windows on a web server (order important)
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors


# Import Colovore libraries
from infoset.db import db_data

__author__ = 'peter@colovore.com (Peter Harrison)'


class ChartParameters(object):
    """Class to manage chart parameters.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, **kwargs):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Set initial values
        defaults = {
            'font_size_label': 15,
            'font_size_title': 20,
            'font_size_legend': 10,
            'font_size_tick': 10,
            'text_color': '#777777',
            'line_color': '#000000',
            'image_width': 8,
            'image_height': 8
        }
        for key, value in defaults.items():
            setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set(self, **kwargs):
        """Set chart parameters.

        Args:
            kwargs: Whatever you want

        Returns:
            None

        """
        # Initialize key variables
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get(self, **kwargs):
        """get chart parameters.

        Args:
            kwargs: Whatever you want

        Returns:
            None

        """
        # Initialize key variables
        for key, value in kwargs.items():
            getattr(self, key, value)


class Chart(object):
    """Class to create charts.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, data, start=None, stop=None, **kwargs):
        """Function for intializing the class.

        Args:
            idx: idx of datapoint
            start: Starting timestamp
            stop: Ending timesta
            **kwargs: Used by ChartParameters

        Returns:
            None

        """
        self.data = data

        # Get parameters
        self.paramx = ChartParameters(**kwargs)

    def single_line(self, title, label, color, filepath, **kwargs):
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

        #####################################################################
        #
        # Create Charts
        #
        #####################################################################

        # Create chart object
        fig, axes = plt.subplots()

        # Convert data dict to two lists for matplotlib
        (x_values, y_values) = _timestamps2dates(self.data)

        #####################################################################
        # Apply generic chart settings that don't require custom variables
        #####################################################################
        # Create chart
        self._generic_settings(fig, axes, ymax=max(y_values) * 1.1)

        #####################################################################
        # Apply image specific settings that are not part of subplots and
        # require custom variables
        #####################################################################

        # Define chart title
        axes.set_title(
            title,
            size=self.paramx.font_size_title,
            y=1.01)

        # Define chart labels

        # axes.set_xlabel(
        #    'Date / Time',
        #    color=self.paramx.text_color,
        #    size=self.paramx.font_size_label)
        axes.set_ylabel(
            'Values',
            color=self.paramx.text_color,
            size=self.paramx.font_size_label)

        #####################################################################
        # Create chart for each sub plot.
        #####################################################################

        data_line = _subplot(
            (x_values, y_values), axes, color, fill=True)
        lines2plot.append(data_line)
        labels.append(label)

        # Create legend for each sub plot
        fig.legend(
            tuple(lines2plot), tuple(labels),
            loc='lower center',
            fontsize=self.paramx.font_size_legend, ncol=2, frameon=False)

        # Add space below chart for legend
        fig.subplots_adjust(bottom=0.2)

        #####################################################################
        # Finish up
        #####################################################################
        # Create image file
        fig.savefig(filepath, bbox_inches='tight')

        # Close figure to conserve memory
        plt.close(fig)

    def api_single_line(self, title, label, color, filepath, **kwargs):
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

        #####################################################################
        #
        # Create Charts
        #
        #####################################################################

        # Create chart object
        fig, axes = plt.subplots()
        # Convert data dict to two lists for matplotlib
        (x_values, y_values) = _timestamps2dates(self.data)
        #####################################################################
        # Apply generic chart settings that don't require custom variables
        #####################################################################

        # Create chart
        ymax = max(tmpval for tmpval in y_values if tmpval is not None)
        self._generic_settings(fig, axes, ymax=ymax * 1.1)

        #####################################################################
        # Apply image specific settings that are not part of subplots and
        # require custom variables
        #####################################################################


        # Define chart title
        axes.set_title(
            title,
            size=self.paramx.font_size_title,
            y=1.01)

        # Define chart labels

        # axes.set_xlabel(
        #    'Date / Time',
        #    color=self.paramx.text_color,
        #    size=self.paramx.font_size_label)
        axes.set_ylabel(
            'Values',
            color=self.paramx.text_color,
            size=self.paramx.font_size_label)

        #####################################################################
        # Create chart for each sub plot.
        #####################################################################

        data_line = _subplot(
            (x_values, y_values), axes, color, fill=True)
        lines2plot.append(data_line)
        labels.append(label)

        # Create legend for each sub plot
        fig.legend(
            tuple(lines2plot), tuple(labels),
            loc='lower center',
            fontsize=self.paramx.font_size_legend, ncol=2, frameon=False)

        # Add space below chart for legend
        fig.subplots_adjust(bottom=0.2)

        #####################################################################
        # Finish up
        #####################################################################

        # Create image file
        fig.patch.set_facecolor('white')
        # fig.savefig(filepath, bbox_inches='tight')
        fig.savefig(filepath)
        canvas = FigureCanvas(fig)
        plt.close(fig)
        png_output = io.BytesIO()
        canvas.print_png(png_output)
        return png_output

    def create_stacked(self, name, title, colors, labels, filepath):
        """Create stacked chart from data.

        Args:
            title: Title of chart
            color: Color of chart
            filepath: Name of output file

        Returns:
            None

        """
        # Random colors for each plot
        fig, axes = plt.subplots()


        prop_iter = iter(plt.rcParams['axes.prop_cycle'])

        y_list = []

        for datapoint in self.data:
            (x_values, y_values) = _timestamps2dates(datapoint)
            y_list.append(y_values)
            ymax = max(tmpval for tmpval in y_values if tmpval is not 0)            
        

        #####################################################################
        # Apply generic chart settings that don't require custom variables
        #####################################################################
        # Create chart
        self._generic_settings(fig, axes, ymax=ymax * 2.4)
        
        plt.stackplot(x_values, y_list, edgecolor="white" ,colors=colors)

        # Create image file
        fig.patch.set_facecolor('white')
        fig.savefig(filepath, bbox_inches='tight')
        canvas = FigureCanvas(fig)
        plt.close(fig)
        png_output = io.BytesIO()
        canvas.print_png(png_output)
        return png_output

    def _generic_settings(self, fig, axes, ymin=0, ymax=None):
        """Do basic chart setup.

        Args:
            fig: Matplotlib figure object
            axes: Matplotlib axis object
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

        # Define how dates are placed on the x-axis
        xtick_locator = mdates.AutoDateLocator()
        xtick_formatter = mdates.AutoDateFormatter(xtick_locator)
        axes.xaxis.set_major_locator(xtick_locator)
        axes.xaxis.set_major_formatter(xtick_formatter)

        # Remove scientific notation in subplot
        axes.xaxis.get_offset_text().set_visible(False)
        axes.yaxis.get_offset_text().set_visible(False)

        #####################################################################
        # Start setting **kwargs values
        #####################################################################

        # Set figure size
        fig.set_size_inches(
            self.paramx.image_width, self.paramx.image_height)

        # Turn on grid lines
        axes.grid(True, color=self.paramx.text_color, linestyle='-')

        # Tick label colors
        axes.tick_params(
            colors=self.paramx.text_color,
            labelsize=self.paramx.font_size_tick)


def _subplot(data, axes, line_color, fill=True):
    """Return total data consumption over time period as PNG HTML link.

    Args:
        data: Tuple of lists of data to plot
        axes: Matplotlib axis object
        line_color: Image parameters
        fill: Fill in under the line if True

    Returns:
        plot_line: Plot plot_line for creating a legend

    """
    # Convert data dict to two lists for matplotlib
    (x_values, y_values) = data

    # NOTE!!!
    # Replace None values in y_values with zeros to prevent line fill
    # errors
    y_new = [0] * len(y_values)
    for (idx, item) in enumerate(y_values):
        if item is None:
            continue
        y_new[idx] = y_values[idx]

    #####################################################################
    #
    # Create Charts
    #
    #####################################################################

    # Create chart plot object (Array)
    plot_line, = axes.plot(
        x_values, y_new, line_color, linewidth=1)

    #####################################################################
    # Gradient fill under line (start)
    #####################################################################
    if fill is True:

        # Get limits of X and Y axis values
        xmin = min(x_values)
        xmax = max(x_values)
        ymin = 0
        ymax = max(tmpval for tmpval in y_values if tmpval is not None)

        # Create an object that will be used to gradient fill under the line
        zorder = plot_line.get_zorder()
        alpha = plot_line.get_alpha()
        alpha = 1.0 if alpha is None else alpha
        gradient = np.empty((100, 1, 4), dtype=float)

        # Magic to create a polygon shaped area under the curve. This will
        # be used as a bitmap mask later
        column_stacked_array = np.column_stack([x_values, y_new])
        vstacked_array = np.vstack(
            [[xmin, ymin], column_stacked_array, [xmax, ymin], [xmin, ymin]])
        clip_path = Polygon(
            vstacked_array, facecolor=line_color,
            edgecolor=line_color, closed=True)
        axes.add_patch(clip_path)

        # Plot data, with gradient shading that only exposes
        # what the mask allows
        axes.imshow(
            gradient,
            aspect='auto',
            origin='lower',
            zorder=zorder,
            interpolation="none",
            clip_path=clip_path, clip_on=True,
            extent=[xmin, xmax, 0, ymax])

        #####################################################################
        # Gradient fill under line (stop)
        #####################################################################

    # Return
    return plot_line


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

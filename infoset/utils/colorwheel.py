"""Classes for setting the colors needed for charts."""


class ColorWheel(object):
    """Defines the colors to be used for each type of chart created."""

    def __init__(self, agent_label):
        """Instantiate the class.

        Args:
            agent_label: Label for the agent that is charted.

        Returns:
            None

        """
        # Initialize key varibles
        self.agent_label = agent_label

        self.color_palette = {
            'memory': '#00c8a4',
            'disk': '#0291D9',
            'load': '#f37372',
            'cpu': '#009DB2',
            'network': '#025AD9',
        }

        # Define color schemes for stacked charts
        self.memory_stacked = [
            '#00c8a4', '#0291D9', '#f37372', '#009DB2', '#025AD9']
        self.network_stacked = [
            '#00c8a4', '#0291D9', '#f37372', '#009DB2', '#025AD9']

    def get_scheme(self):
        """Return color scheme depending on the type of agent label.

        Args:
            None

        Returns:
            None

        """
        # Set color values depending on the agent_label
        if 'memory' in self.agent_label:
            return self.color_palette['memory']
        elif 'disk' in self.agent_label:
            return self.color_palette['disk']
        elif 'network' in self.agent_label:
            return self.color_palette['network']
        elif 'load' in self.agent_label:
            return self.color_palette['load']
        elif 'cpu' in self.agent_label:
            return self.color_palette['cpu']

    def get_palette(self):
        """Return a palette of colors for stacked charts by agent label.

        Args:
            None

        Returns:
            None

        """
        # Return
        if 'memory' in self.agent_label:
            return self.memory_stacked

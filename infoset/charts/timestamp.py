"""Library of miscellaneous charting classes."""

import time


class TimeStamp(object):
    """Calculates the timestamps for predefined chart timeframes."""

    def __init__(self):
        """Instantiate the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        seconds_per_day = 86400
        self.presets = [
            seconds_per_day,
            7 * seconds_per_day,
            30 * seconds_per_day,
            365 * seconds_per_day
        ]

        # Define descriptions for each graph type
        self.descriptions = [
            'Today', 'This Week', 'This Month', 'This Year']

        # Define labels for each graph type to be used in templates
        self.id_labels = [
            'one-hour', 'twenty-four-hours', 'one-week', 'one-month']

        # Process data
        self._process()

    def _process(self):
        """Process the data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        now = int(time.time()) - 300
        self.start_times = []
        self.stop_times = []

        # Process data. Create lists of start/stop times and descriptions
        for timestamp in self.presets:
            start = now - timestamp
            self.start_times.append(start)
            self.stop_times.append(now)
        self.times = list(zip(
            self.start_times, self.stop_times,
            self.descriptions, self.id_labels))

    def get_times(self):
        """Return chart duration data.

        Args:
            None

        Returns:
            value: tuple of lists of (start times, stop times, descriptions)
                for each timeframe of chart

        """
        # Return
        value = self.times
        return value

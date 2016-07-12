"""Module of infoset database functions.

Classes for agent data

"""
# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db_datapoint
from infoset.db import db


class GetIDX(object):
    """Class to return agent data.

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
            stop: Ending timestamp

        Returns:
            None

        """
        # Initialize important variables
        self.data = defaultdict(dict)

        # Get the datapoint's base_type
        datapointer = db_datapoint.GetIDX(idx, config)
        self.base_type = datapointer.base_type()

        # Redefine start / stop times
        if start is None:
            ts_start = 0
        else:
            # Adjust for counters
            if self.base_type == 1:
                ts_start = start
            else:
                ts_start = start - 300
        if stop is None:
            ts_stop = jm_general.normalized_timestamp()
        else:
            ts_stop = stop
        if ts_start > ts_stop:
            ts_start = ts_stop

        # Prepare SQL query to read a record from the database.
        # Only active oids
        sql_query = (
            'SELECT value, timestamp '
            'FROM iset_data '
            'WHERE '
            '(timestamp >= %s AND timestamp <= %s) AND '
            'idx_datapoint=\'%s\'') % (
                ts_start, ts_stop, idx)

        # Do query and get results
        database = db.Database(config)
        query_results = database.query(sql_query, 1301)

        # Massage data
        for row in query_results:
            # uid found?
            if not row[0]:
                log_message = ('idx %s not found.') % (idx)
                log.log2die(1302, log_message)

            # Assign values
            timestamp = row[1]
            value = row[0]
            self.data[timestamp] = value

    def everything(self):
        """Get all datapoints.

        Args:
            None

        Returns:
            value: Dictionary of data_points

        """
        # Return data
        if self.base_type == 1:
            value = self.data
        else:
            value = _counter(self.data, base_type=self.base_type)
        return value


def _counter(data, base_type=1):
    """Convert counter data to gauge.

    Args:
        data: Dict of data keyed by timestamp

    Returns:
        values: Converted dict of data keyed by timestamp

    """
    # Initialize key variables
    count = 0
    values = defaultdict(dict)

    # Start conversion
    for timestamp, value in sorted(data.items()):
        # Skip first value
        if count == 0:
            old_timestamp = timestamp
            count += 1
            continue

        # Get new value
        new_value = value - data[old_timestamp]

        # Do conversion
        if new_value >= 0:
            values[timestamp] = new_value
        else:
            if base_type == 32:
                fixed_value = 4294967296 + abs(value) - 1
            else:
                fixed_value = (4294967296 * 4294967296) + abs(value) - 1
            values[timestamp] = fixed_value

        # Save old timestamp
        old_timestamp = timestamp

    # Return
    return values

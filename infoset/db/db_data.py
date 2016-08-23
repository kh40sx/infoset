"""Module of infoset database functions.

Classes for agent data

"""
# Python standard libraries
from collections import defaultdict
from sqlalchemy import and_

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db_datapoint
from infoset.db import db
from infoset.db.db_orm import Data


class GetIDX(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx, start=None, stop=None):
        """Function for intializing the class.

        Args:
            idx: idx of datapoint
            start: Starting timestamp
            stop: Ending timestamp

        Returns:
            None

        """
        # Initialize important variables
        self.data = defaultdict(dict)

        # Get the datapoint's base_type
        datapointer = db_datapoint.GetIDX(idx)
        self.base_type = datapointer.base_type()

        # Redefine start times
        if start is None:
            self.ts_start = jm_general.normalized_timestamp() - (3600 * 24)
        else:
            self.ts_start = jm_general.normalized_timestamp(start)

        # Redefine stop times
        if stop is None:
            self.ts_stop = jm_general.normalized_timestamp()
        else:
            self.ts_stop = jm_general.normalized_timestamp(stop)

        # Fix edge cases
        if self.ts_start > self.ts_stop:
            self.ts_start = self.ts_stop

        # Make sure datapoint exists
        if db_datapoint.idx_exists(idx) is False:
            log_message = ('idx %s not found.') % (idx)
            log.log2die(1049, log_message)

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Data.timestamp, Data.value).filter(and_(
            Data.timestamp >= self.ts_start,
            Data.timestamp <= self.ts_stop,
            Data.idx_datapoint == idx))

        # Massage data
        for instance in result:
            self.data[instance.timestamp] = instance.value

        # Return the session to the database pool after processing
        session.close()

    def everything(self):
        """Get all datapoints.

        Args:
            None

        Returns:
            value: Dictionary of data_points

        """
        # Return data
        value = self._counter()
        return value

    def _counter(self):
        """Convert counter data to gauge.

        Args:
            None

        Returns:
            values: Converted dict of data keyed by timestamp

        """
        # Initialize key variables
        count = 0

        # Populate values dictionary with zeros. This ensures that
        # all timestamp values are covered if we have lost contact
        # with the agent at some point along the time series.
        if self.base_type == 1:
            values = dict.fromkeys(
                range(self.ts_start, self.ts_stop + 300, 300), 0)
        else:
            values = dict.fromkeys(
                range(self.ts_start + 300, self.ts_stop + 300, 300), 0)

        # Start conversion
        for timestamp, value in sorted(self.data.items()):
            # Process counter values
            if self.base_type != 1:
                # Skip first value
                if count == 0:
                    old_timestamp = timestamp
                    count += 1
                    continue

                #############################################################
                # Skip calculation if the difference in timestamps is > step.
                # This helps to prevent spikes in the data due to outages
                #############################################################
                if timestamp - old_timestamp > step:
                    old_timestamp = timestamp
                    continue

                # Get new value
                new_value = value - self.data[old_timestamp]

                # Do conversion
                if new_value >= 0:
                    values[timestamp] = new_value
                else:
                    if self.base_type == 32:
                        fixed_value = 4294967296 + abs(value) - 1
                    else:
                        fixed_value = (
                            4294967296 * 4294967296) + abs(value) - 1
                    values[timestamp] = fixed_value
            else:
                # Process gauge values
                values[timestamp] = self.data[timestamp]

            # Save old timestamp
            old_timestamp = timestamp

        # Return
        return values

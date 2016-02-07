#!/usr/bin/env python3
"""Classes for polling remote hosts for SNMP data."""

import tempfile
import time
import os
import queue as Queue
import threading


import jm_general
from snmp import snmp_manager
from snmp import snmp_info


# Define a key global variable
THREAD_QUEUE = Queue.Queue()


class PollAllSNMP(threading.Thread):
    """Threaded polling.

    Graciously modified from:
    http://www.ibm.com/developerworks/aix/library/au-threadingpython/

    """

    def __init__(self, queue):
        """Initialize the threads."""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """Update the database using threads."""
        while True:
            # Get the data_dict
            data_dict = self.queue.get()
            host = data_dict['host']
            config = data_dict['config']
            verbose = data_dict['verbose']
            temp_dir = data_dict['temp_dir']

            # Show host information
            validate = snmp_manager.Validate(host, config.snmp_auth())
            snmp_params = validate.credentials()

            # Verbose output
            if verbose is True:
                output = ('Processing on: host %s') % (host)
                print(output)

            # Skip invalid, and uncontactable hosts
            if bool(snmp_params) is False:
                if verbose is True:
                    log_message = (
                        'Uncontactable host %s or no valid SNMP '
                        'credentials found for it.') % (host)
                    jm_general.logit(1019, log_message, False)
                continue

            # Process if valid
            if bool(snmp_params) is True:
                # Get data
                status = snmp_info.Query(snmp_params)
                data = status.everything()
                yaml_string = jm_general.dict2yaml(data)

                # Dump data
                temp_file = ('%s/%s.yaml') % (temp_dir, host)
                with open(temp_file, 'w') as file_handle:
                    file_handle.write(yaml_string)

                # Verbose output
                if verbose is True:
                    output = ('Completed run: host %s') % (host)
                    print(output)

            # Signals to queue job is done
            self.queue.task_done()


def poll(config, verbose=False):
    """Process 'poll' CLI option.

    Args:
        config: Configuration object
        verbose: Verbose output if True

    Returns:
        None

    """
    # Initialize key variables
    threads_in_pool = 10

    # Create directory if needed
    perm_dir = config.snmp_directory()
    temp_dir = tempfile.mkdtemp()

    # Delete all files in temporary directory
    jm_general.delete_files(temp_dir)

    # Spawn a pool of threads, and pass them queue instance
    for unused_var in range(threads_in_pool):
        update_thread = PollAllSNMP(THREAD_QUEUE)
        update_thread.daemon = True
        update_thread.start()

    # Get host data and write to file
    for host in config.hosts():
        ####################################################################
        #
        # Define variables that will be required for the database update
        # We have to initialize the dict during every loop to prevent
        # data corruption
        #
        ####################################################################
        data_dict = {}
        data_dict['host'] = host
        data_dict['config'] = config
        data_dict['verbose'] = verbose
        data_dict['temp_dir'] = temp_dir
        THREAD_QUEUE.put(data_dict)

    # Wait on the queue until everything has been processed
    THREAD_QUEUE.join()

    # PYTHON BUG. Join can occur while threads are still shutting down.
    # This can create spurious "Exception in thread (most likely raised
    # during interpreter shutdown)" errors.
    # The "time.sleep(1)" adds a delay to make sure things really terminate
    # properly. This seems to be an issue on virtual machines in Dev only
    time.sleep(1)

    # Cleanup, move temporary files to clean permanent directory.
    # Delete temporary directory
    if os.path.isdir(perm_dir):
        jm_general.delete_files(perm_dir)
    else:
        os.makedirs(perm_dir, 0o755)
    jm_general.move_files(temp_dir, perm_dir)
    os.rmdir(temp_dir)

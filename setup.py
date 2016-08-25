#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import os
import socket
import argparse
import sys

# Infoset libraries
try:
    from infoset.utils import log
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)

from infoset.utils import jm_configuration
from infoset.utils import jm_general
from infoset.metadata import metadata
from infoset.db.db_orm import BASE, Agent, Department, Host, BillType
from infoset.db.db_orm import Configuration, HostAgent
from infoset.db import DBURL
from infoset.db import db_agent
from infoset.db import db_configuration
from infoset.db import db_billtype
from infoset.db import db_department
from infoset.db import db_host
from infoset.db import db_hostagent
from infoset.db import db
from infoset.agents import agent
import infoset.utils


class Install(object):
    """Class to install infoset.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize important variables

    def install(self):
        """Install infoset.

        Args:
            None

        Returns:
            None

        """
        # Get configuration
        config = jm_configuration.Config()

        # Run server setup if required
        if config.server() is True:
            self._server_setup()

    def _insert_department(self):
        """Insert first department in the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        if db_department.idx_exists(1) is False:
            record = Department(
                code=jm_general.encode('_SYSTEM_RESERVED_'),
                name=jm_general.encode('_SYSTEM_RESERVED_'))
            database = db.Database()
            database.add(record, 1102)

    def _insert_billtype(self):
        """Insert first billtype in the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        if db_billtype.idx_exists(1) is False:
            record = BillType(
                code=jm_general.encode('_SYSTEM_RESERVED_'),
                name=jm_general.encode('_SYSTEM_RESERVED_'))
            database = db.Database()
            database.add(record, 1104)

    def _insert_agent_host(self):
        """Insert first agent and host in the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        idx_agent = 1
        idx_host = 1
        agent_name = '_infoset'

        # Add agent
        if db_agent.idx_exists(idx_agent) is False:
            record = Agent(
                id=jm_general.encode('_SYSTEM_RESERVED_'),
                name=jm_general.encode(agent_name))
            database = db.Database()
            database.add(record, 1109)

            # Generate a UID
            uid = agent.get_uid(agent_name)
            database = db.Database()
            session = database.session()
            record = session.query(Agent).filter(Agent.idx == idx_agent).one()
            record.id = jm_general.encode(uid)
            database.commit(session, 1073)

        # Add host
        if db_host.idx_exists(idx_host) is False:
            record = Host(
                description=jm_general.encode('Infoset Server'),
                hostname=jm_general.encode(socket.getfqdn()))
            database = db.Database()
            database.add(record, 1106)

        # Add to Agent / Host table
        if db_hostagent.host_agent_exists(idx_host, idx_agent) is False:
            record = HostAgent(idx_host=idx_host, idx_agent=idx_agent)
            database = db.Database()
            database.add(record, 1107)

    def _insert_config(self):
        """Insert first config in the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        key_values = [('version', '0.0.0.0')]

        # Cycle through all the key value pairs
        for item in key_values:
            key = item[0]
            value = item[1]

            # Check if value exists and insert if not
            if db_configuration.config_key_exists(key) is False:
                record = Configuration(
                    config_key=jm_general.encode(key),
                    config_value=jm_general.encode(value))
                database = db.Database()
                database.add(record, 1108)

    def _server_setup(self):
        """Setup server.

        Args:
            None

        Returns:
            None

        """
        # Use newly installed sqlalchemy package
        # to create the database tables
        from sqlalchemy import create_engine

        # Initialize key variables
        use_mysql = True
        pool_size = 25
        max_overflow = 25

        # Get configuration
        config = jm_configuration.Config()

        # Create DB connection pool
        if use_mysql is True:
            # Add MySQL to the pool
            engine = create_engine(
                DBURL, echo=True,
                encoding='utf8',
                max_overflow=max_overflow,
                pool_size=pool_size, pool_recycle=3600)

            # Try to create the database
            print('Attempting to create database tables')
            try:
                sql_string = (
                    'ALTER DATABASE %s CHARACTER SET utf8mb4 '
                    'COLLATE utf8mb4_general_ci') % (config.db_name())
                engine.execute(sql_string)
            except:
                log_message = (
                    'Cannot connect to database %s. '
                    'Verify database server is started. '
                    'Verify database is created. '
                    'Verify that the configured database authentication '
                    'is correct.') % (config.db_name())
                log.log2die(1036, log_message)

            # Apply schemas
            print('Applying Schemas')
            BASE.metadata.create_all(engine)

            # Insert database entries
            self._insert_agent_host()
            self._insert_billtype()
            self._insert_department()
            self._insert_config()


def cli():
    """Return all the CLI options.

    Args:
        None

    Returns:
        args: Argument values

    """
    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    # CLI argument for installing
    parser.add_argument(
        '--install',
        required=False,
        default=False,
        action='store_true',
        help='Install infoset.'
    )

    # CLI argument for upgrading
    parser.add_argument(
        '--upgrade',
        required=False,
        default=False,
        action='store_true',
        help='Upgrade infoset.'
    )

    # Get the parser value
    args = parser.parse_args()

    # Print help if required
    if args.install == args.upgrade:
        parser.print_help()
        sys.exit(0)

    # Return
    return args


def main():
    """Process agent data.

    Args:
        None

    Returns:
        None

    """
    # Get CLI values
    cli_args = cli()

    #########################################################################
    # Install required PIP packages
    #########################################################################

    print('Installing required pip3 packages')
    pip3 = infoset.utils.jm_general.search_file('pip3')
    if pip3 is None:
        log_message = ('Cannot find python "pip3". Please install.')
        log.log2die(1052, log_message)

    utils_directory = jm_general.root_directory()
    requirements_file = ('%s/requirements.txt') % (utils_directory)
    script_name = (
        'pip3 install --user --requirement %s') % (requirements_file)
    infoset.utils.jm_general.run_script(script_name)

    #########################################################################
    # Setup database
    #########################################################################
    if cli_args.install is True:
        install = Install()
        install.install()

    # Try some additional statements
    metadata.insert_oids()

    # Print success
    print('\nDatabase setup done!\n')

    # Export PYTHONPATH to ~/.bashrc
    python_path = os.environ['PYTHONPATH']
    script_name = (
        'echo "export PYTHONPATH=%s" >> ~/.bashrc') % (python_path)
    infoset.utils.jm_general.run_script(script_name, shell=True)

    # Say how to setup your virtual environment
    print("""\
You now need to setup your virtual environment. \
Run the following commands from the infoset root directory:

    source ~/.bashrc
    sudo make
    source venv/bin/activate
    sudo make install
""")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

"""Class to process connection."""

# Infoset libraries
from infoset.utils import log
from infoset.db import POOL


class Database(object):
    """Class interacts with the connection.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self):
        """Function for intializing the class.

        Args:
            config: Config object

        Returns:
            None

        """
        # Intialize key variables
        self.pool = POOL

    def query(self, sql_statement, error_code):
        """Do a database query.

        Args:
            sql_statement: SQL statement
            error_code: Error number to use if one occurs

        Returns:
            query_results: Query results

        """
        # Make sure this is a SELECT statement
        first_word = sql_statement.split()[0]
        if first_word.lower() != 'select':
            log_message = ('db_query function can only do SELECT: '
                           'SQL statement %s') % (sql_statement)
            log.log2die(error_code, log_message)

        # Open database connection. Prepare cursor
        session = self.pool

        try:
            # Execute the SQL command
            query_results = session.execute(sql_statement)

        except Exception as exception_error:
            log_message = (
                'Unable to fetch data from connection. '
                'SQL statement: \"%s\" Error: \"%s\"') % (
                    sql_statement, exception_error)
            log.log2die(error_code, log_message)
        except:
            log_message = ('Unexpected exception. SQL statement: \"%s\"') % (
                sql_statement)
            log.log2die(error_code, log_message)

        # Disconnect from server
        session.close()

        return query_results

    def modify(self, sql_statement, error_code, data_list=False):
        """Do a database modification.

        Args:
            sql_statement: SQL statement
            error_code: Error number to use if one occurs
            data_list: If not False, then the SQL statement is referring
                to a bulk update using a list of tuples contained in
                data_list.

        Returns:
            query_results: Query results

        """
        # Make sure this is a UPDATE, INSERT or REPLACE statement
        """
        first_word = sql_statement.split()[0]
        if ((first_word.lower() != 'update') and
                (first_word.lower() != 'delete') and
                (first_word.lower() != 'insert') and
                (first_word.lower() != 'replace')):

            log_message = ('db_modify function can only do '
                           'INSERT, UPDATE, DELETE or REPLACE: '
                           'SQL statement %s') % (sql_statement)
            log.log2die(error_code, log_message)
        """

        # Open database connection. Prepare cursor
        session = self.pool

        try:
            # If a list is provided, then do an executemany
            if data_list:
                # Execute the SQL command
                table = sql_statement
                session.execute(table.insert(), data_list)
            else:
                # Execute the SQL command
                session.execute(sql_statement)

            # Commit  change
            session.commit()

        except Exception as exception_error:
            session.rollback()
            log_message = (
                'Unable to modify connection. '
                'SQL statement: \"%s\" Error: \"%s\"') % (
                    sql_statement, exception_error)
            log.log2die(error_code, log_message)
        except:
            session.rollback()
            log_message = ('Unexpected exception. SQL statement: \"%s\"') % (
                sql_statement)
            log.log2die(error_code, log_message)

        # disconnect from server
        session.close()

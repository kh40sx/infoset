#!/usr/bin/env python3

"""Class to process database."""

# pip3 libraries
import pymysql

# Infoset libraries
import jm_general


class Database(object):
    """Class interacts with the database.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, config):
        """Function for intializing the class.

        Args:
            config: Config object

        Returns:
            None

        """
        # Intialize key variables
        self.database = pymysql.connect(
            host=config.db_hostname(),
            user=config.db_username(),
            passwd=config.db_password(),
            db=config.db_name())

    def db_query(self, sql_statement, error_code):
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
            jm_general.logit(error_code, log_message)

        # Open database connection. Prepare cursor
        cursor = self.database.cursor()

        try:
            # Execute the SQL command
            cursor.execute(sql_statement)
            query_results = cursor.fetchall()

        except Exception as exception_error:
            log_message = (
                'Unable to fetch data from database. '
                'SQL statement: \"%s\" Error: \"%s\"') % (
                    sql_statement, exception_error)
            jm_general.logit(error_code, log_message)
        except:
            log_message = ('Unexpected exception. SQL statement: \"%s\"') % (
                sql_statement)
            jm_general.logit(error_code, log_message)

        # Disconnect from server
        self.database.close()

        return query_results

    def db_modify(self, sql_statement, error_code, data_list=False):
        """Do a database modification.

        Args:
            sql_statement: SQL statement
            error_code: Error number to use if one occurs

        Returns:
            query_results: Query results

        """
        # Make sure this is a UPDATE, INSERT or REPLACE statement
        first_word = sql_statement.split()[0]
        if ((first_word.lower() != 'update') and
                (first_word.lower() != 'delete') and
                (first_word.lower() != 'insert') and
                (first_word.lower() != 'replace')):

            log_message = ('db_modify function can only do '
                           'INSERT, UPDATE, DELETE or REPLACE: '
                           'SQL statement %s') % (sql_statement)
            jm_general.logit(error_code, log_message)

        # Open database connection. Prepare cursor
        cursor = self.database.cursor()

        try:
            # If a list is provided, then do an executemany
            if data_list:
                # Execute the SQL command
                cursor.executemany(sql_statement, data_list)
            else:
                # Execute the SQL command
                cursor.execute(sql_statement)

            # Commit  change
            self.database.commit()

        except Exception as exception_error:
            self.database.rollback()
            log_message = (
                'Unable to modify database. '
                'SQL statement: \"%s\" Error: \"%s\"') % (
                    sql_statement, exception_error)
            jm_general.logit(error_code, log_message)
        except:
            self.database.rollback()
            log_message = ('Unexpected exception. SQL statement: \"%s\"') % (
                sql_statement)
            jm_general.logit(error_code, log_message)

        # disconnect from server
        self.database.close()

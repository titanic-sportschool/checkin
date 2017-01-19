"""
    Author: Nick Bout
    Class: DatabaseClass

    This class contains functions to handle everything related to the database.
    We use the PyMySQL module to connect with the database. (https://github.com/PyMySQL/PyMySQL)
"""

#Imports
import pymysql
import time
from Utils.config import DB_HOST, DB_PASS, DB_USER, DB

# Create a connection to the database
connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             passwd=DB_PASS,
                             db=DB)
current = connection.cursor(pymysql.cursors.DictCursor)


class DatabaseClass:
    """
             Databaseclass containing all the functions
    """

    def close_connection(self):
        """
            Closed the database connection.
        """
        connection.close()

    def select(self, query) -> dict:
        """
            Function to use a SQL SELECT based on a given SQL query.

            Args:
                STRING: query: SQL query
            Returns:
                select: dictionary with the data returned from the SQL query
        """
        try:
            result = ''
            current.execute(query)
            for data in current:
                result = data
            return result
        except Exception as error:
            print("Exception:", error)

    def insert(self, query):
        """
            Function to use a SQL INSERT based on a given SQL query.

            Args:
                STRING: query: SQL query
            Returns:
                --
        """
        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)

    def update(self, query):
        """
            Function to use a SQL UPDATE based on a given SQL query.

            Args:
                STRING: query: SQL query
            Returns:
                --
        """

        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)

    def delete(self, query):
        """
            Function to use a SQL DELETE based on a given SQL query.

            Args:
                STRING: query: SQL query
            Returns:
                --
        """
        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(query)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        except Exception as error:
            print("Exception:", error)

    def getCustomer(self, email, password):
        return self.select("SELECT * FROM logindata WHERE email = '" + email + "' AND password = '" + password + "' LIMIT 1")

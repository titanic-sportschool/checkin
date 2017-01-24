"""
    Author: Nick Bout
    Class: DatabaseClass

    This class contains functions to handle everything related to the database.
    We use the PyMySQL module to connect with the database. (https://github.com/PyMySQL/PyMySQL)
"""

#Imports
import pymysql
import datetime
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

    def get_customer(self, email, password) -> dict:
        query = "SELECT " \
                "Login.Email, " \
                "Login.User_ID, " \
                "Login.User_Role_ID " \
                "FROM Login WHERE email = '{0}' AND password = '{1}' LIMIT 1".format(email, password)
        return self.select(query)

    def get_check_in_state(self, user_id):
        query = "SELECT " \
                "Log.Is_checkin, " \
                "Log.Location_ID " \
                "FROM Log WHERE User_ID = '{0}' ORDER BY Date DESC LIMIT 1".format(user_id)
        return self.select(query)

    def check_in_out(self, user_id, location, is_check_in = True):
        date = datetime.datetime.now()
        query = "INSERT INTO Log(Date, Is_checkin, User_ID, Location_ID) VALUES('{0}', {1}, {2}, {3});".format(
            date,
            "true" if is_check_in else "false",
            user_id,
            location
        )
        self.insert(query)

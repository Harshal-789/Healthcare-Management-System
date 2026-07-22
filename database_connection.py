import mysql.connector
from mysql.connector import Error

from LoggerModule import logger


def get_database_connection():
    """
    Creates and returns a connection to the MySQL database.
    """

    connection = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="9494006234@Hh",
            database="hospital_management_db"
        )

        if connection.is_connected():
            logger.info("Connected to MySQL database successfully.")
            return connection

    except Error as error:
        logger.error(f"MySQL Connection Error: {error}")

    return None


def close_database_connection(connection):
    """
    Closes the database connection safely.
    """

    try:
        if connection and connection.is_connected():
            connection.close()
            logger.info("Database connection closed successfully.")

    except Error as error:
        logger.error(f"Error while closing database connection: {error}")
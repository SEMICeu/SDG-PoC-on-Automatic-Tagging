import os
import mysql.connector

os.chdir("../..")

from api.src.nlp_api.core.metatags import get_config

def set_status_busy():
    config = get_config()
    myhost = config['mysql']['host']
    mydb = config['mysql']['db']
    myuser = config['mysql']['username']
    mypass = config['mysql']['password']
    connection = None
    try:
        connection = mysql.connector.connect(host=myhost,
                                             database=mydb,
                                             user=myuser,
                                             password=mypass)

        update_query = "UPDATE  status" \
                       "SET status = 0;" \
                       "SELECT status FROM status"

        cursor = connection.cursor()
        cursor.execute(update_query)
        record = cursor.fetchone()
        print("result " + str(record[0]))
    except mysql.connector.Error as error:
        print("Failed to update table in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def set_status_available():
    config = get_config()
    myhost = config['mysql']['host']
    mydb = config['mysql']['db']
    myuser = config['mysql']['username']
    mypass = config['mysql']['password']
    connection = None
    try:
        connection = mysql.connector.connect(host=myhost,
                                             database=mydb,
                                             user=myuser,
                                             password=mypass)

        update_query = "UPDATE  status" \
                       "SET status = 1;" \
                       "SELECT status FROM status"

        cursor = connection.cursor()
        cursor.execute(update_query)
        record = cursor.fetchone()
        print("result " + str(record[0]))
    except mysql.connector.Error as error:
        print("Failed to update table in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
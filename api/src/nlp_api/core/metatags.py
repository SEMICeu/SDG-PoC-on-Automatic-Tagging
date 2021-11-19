import json

from ..web.models import Status, EnhanceRequest, EnhanceResponse, MetaTag
from flask import jsonify

import yaml
import mysql.connector

import os

os.chdir("../../../../")

#from nlp_engine.nlp_engine import execute
import nlp_engine.nlp_engine as nlp; print(nlp)
from mysql.connector import Error
from pathlib import Path

def get_config():


    my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
    config_path = my_path.parent / 'config.yaml'
    with config_path.open() as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config

def get_status():
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

        select_query = "SELECT status FROM status"
        
        cursor = connection.cursor()
        cursor.execute(select_query)
        record = cursor.fetchone()
        print("result " + str(record[0]))
        status = Status(bool(record[0]))
        return status
    
    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def enhance(request):
    
    metatags_in_request = request.metatags
    metatags_in_response = []

    #for i in metatags_in_request:
    #    metatag = MetaTag(name=i,value="Test1").
    #    metatags_in_response.append(metatag)
    
    # metatags_in_response = []
    metatags_in_response = nlp.execute(request)
    response = EnhanceResponse(metatags=metatags_in_response)
    return response


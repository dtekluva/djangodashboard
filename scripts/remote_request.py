import requests
from requests.auth import HTTPBasicAuth
import json, os
import datetime
import numpy as np

auth_url = os.getenv("auth_url")

readings_url = os.getenv("readings_url")
data_logs_url = os.getenv("data_logs_url")
last_reading_url = os.getenv("last_reading_url")

ppl_username = os.getenv("ppl_username")
password = os.getenv("ppl_password")

def make_remote_request(device_id, start_date = "2019-08-15", end_date = "2019-08-16", url = 'data_logs'):

    try:
        req = requests.get((auth_url).format(ppl_username,password))
    

        try:
            print("#####################################")
            print("#####################################")
            print("#####################################")
            print("STATUS_CODE : ", req.status_code)
            print("RESPONSE CONTENT : ", req.content)
            print("JSON RESPONSE : ", req.json())
            print("#####################################")
            print("#####################################")
            print("#####################################")
        

            auth_key_name = (list(req.cookies)[0]).name #get name of cookie unit used to be (.ASPXAUTH) chnaged to (form_p)
            auth_key_value = dict(req.cookies).get(auth_key_name) #get actual cookie unit
            cookie = {auth_key_name: auth_key_value}

            urls = {
                "readings" : readings_url.format(start_date, end_date, device_id),

                "data_logs" : data_logs_url.format(device_id, start_date, end_date),

                "last_read" : last_reading_url.format(device_id)
            }

            url = urls.get(url)
            # print(url)
            r = requests.get(url, cookies=cookie)
            print("############# AUTHENTICATED ATTEMPTING FETCH ###############")

            try:
                return r.json()

            except:
                print("#####################################")
                print("#####################################")
                print("#####################################")
                print("STATUS_CODE : ", r.status_code)
                print("RESPONSE CONTENT : ", r.content)
                print("JSON RESPONSE : ", r.json())
                print("REQUEST FAILED AT DATA READ..!!!")
                print("#####################################")
                print("#####################################")
                print("#####################################")
                return False

        except:
            print("#####################################")
            print("REQUEST FAILED AT AUTHENTICATION..!!!")
            print("#####################################")
            return False
            
    except:
        print("#####################################")
        print("REQUEST FAILED TO CONNECT AND AUTHENTICATE..!!!")
        print("#####################################")
        
def get_last_reading(device_id):
    response = make_remote_request(device_id, url="last_read")
    return response
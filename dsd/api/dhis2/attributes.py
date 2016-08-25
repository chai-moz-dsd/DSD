'''
Add New Attributes to DHIS2
'''
import json
import requests

def add_attribute(attribute):
    #get token


    print json.dump(attribute)

def parse_attributes(attributes):
    for attribute in attributes:
        # validation
        add_attribute(attribute)
import requests
import json

import pandas as pd

from operations import getrequests_property , getrequests_rent , getrequests_walk_transit_score

#returns the property params as a json from the address provided
def get_property(address):
    url = getrequests_property.url
    querystring = {"address":"{address}"}
    headers = getrequests_property.headers

    print(address)

    response = requests.get(url, headers=headers, params=querystring)

    try:
        df = pd.DataFrame.from_dict(response , orient='index')
        print(df.head(67))
        return df['zpid']
    except RuntimeError as e:
        return e

#returns the property zpid from the given address
def get_data(address):
    
    url = getrequests_property.url
    querystring = {"address":f"{address}"}
    headers = getrequests_property.headers

    try:
        response = requests.get(url, headers=headers, params=querystring).json()
        df = pd.json_normalize(response)
        df = df.dropna(axis=1)
        return df
    except TypeError as e:
        print(e)

def get_specifics(df , col_name):
    return df[col_name]
    
#returns the last sale int
def get_last_sale(zpid):

    querystring = {f"zpid":"{zpid}"}

    url = getrequests_property.url
    headers = getrequests_property.headers
    response = requests.get(url, headers=headers, params=querystring)

    df = pd.DataFrame.from_dict(response['price'] , orient='index')

    return df


#returns the walk and transit json for the area
def get_walktransit(zpid):
    url = getrequests_walk_transit_score.url
    headers = getrequests_walk_transit_score.headers
    #zpid is the id number given to a property by zillow
    querystring = {"zpid":"{zpid}"}
    response = requests.get(url, headers=headers, params=querystring)
    df = pd.DataFrame.from_dict(response , orient='index')
    return df

#returns the scorings for the area provided
def get_wt_score(zpid):
    response = get_walktransit(zpid)

    df = pd.DataFrame.from_dict(response, orient='index')

    print("=====================TRANSIT SCORE DEBUG=====================")
    df.head(5)

    #wtb dict holds the scores of walking, transit and biking
    wtb_dict = {"transit_score" : 0 ,
                "walkscore" : 0,
                "bikescore" : 0}
    #values from zillow are nested json 99% of the time
    wtb_dict['transit_score'] = df["transit_score"]
    wtb_dict['walkscore'] = df['walkscore']
    wtb_dict['bikescore'] = df['bikescore']

    return wtb_dict

def get_rent(address , diameter, p_type):
    url = getrequests_rent.url
    headers = getrequests_rent.headers
    querystring = {f"address":"{address}","d":"{diameter}","propertyType":"{p_type}","includeComps":"True"}
    response = requests.get(url, headers=headers, params=querystring)
    df = pd.DataFrame.from_dict(response, orient='index')
    return df

def get_stats(address , diameter, p_type):
    stats_dict = {"HighestRent" : 0,
                  "LowestRent" : 0,
                  "TotalCompared" : 0,
                  "MedianRent" : 0}
    
    response = get_rent(address , diameter, p_type)
    print("=====================STATS DEBUG=====================")
    print(response)

    #highest rent pulled from defined area
    stats_dict["HighestRent"] = response["highRent"]

    #lowest rent pulled from defined area
    stats_dict["LowestRent"] = response["lowRent"]

    #comparable_rentals is the total amount of rental properties compared to chosen property
    stats_dict["TotalCompared"] = response["comparableRentals"]

    #median_rent is the median rent of the area of the diameter of the address chosen
    stats_dict["MedianRent"] = response["median"]

    return stats_dict
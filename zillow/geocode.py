#!/usr/local/bin/python3
import pandas as pd
import requests as r
import urllib.parse as u
import argparse

parser = argparse.ArgumentParser(description='Geocode a csv of properties in the City of Detroit')
parser.add_argument('handle', metavar='F', type=str, help='csv file to process')

args = parser.parse_args()

f = args.handle

print('Loading file %s' % f)

df = pd.read_csv(f)

request_url = 'https://gis.detroitmi.gov/arcgis/rest/services/DoIT/AddressPointGeocoder/GeocodeServer/findAddressCandidates?{}&ZIP=&Single+Line+Input=&category=&outFields=*&maxLocations=&outSR=4326&searchExtent=&location=&distance=&magicKey=&f=pjson'

def geocode_address(addr):
    qs = {'Street': addr}
    encoded_qs = u.urlencode(qs)
    formatted_url = request_url.format(encoded_qs)
    res = r.get(formatted_url)
    data_dict = res.json()
    #take the top candidate for now for the sake of greed
    data_dict_candidates = data_dict['candidates']
    if len(data_dict_candidates) > 0:
        first_candidate = data_dict_candidates[0]
        first_candidate_location = first_candidate['location']
        first_candidate_attributes = first_candidate['attributes'] 
        return  pd.Series({'Parcel': first_candidate_attributes['User_fld'].strip(), 'Score': first_candidate_attributes['Score'], 'Long':first_candidate_location['x'], 'Lat': first_candidate_location['y']})
    else:
        return  pd.Series({'Parcel': 'Unknown', 'Score': 0})

#Get all unique addresses in the entries for asbestos notifs and geocode them
uniq_addrs = df.address.unique()
addrs = {'address': uniq_addrs}
addr_df = pd.DataFrame(data=addrs)
#geocode_slice = addr_df[:20]
geocode_result = addr_df.apply(lambda data_row: geocode_address(data_row['address']), axis=1)
merged = addr_df.merge(geocode_result, left_index=True, right_index=True) 


#This will find not perfectly matched geocode results
#unmatched_gecodes = merged.query('Score < 100.00')

#Join geocoded addresses to the originial dataframe

joined_df = df.set_index('address').join(merged.set_index('address'))
queried_df = joined_df.query('Score > 0')
bad_addresses = joined_df.query('Score == 0')

queried_df.to_csv('geocoded_addresses_%s' % f)
bad_addresses.to_csv('bad_addresses_%s' % f)

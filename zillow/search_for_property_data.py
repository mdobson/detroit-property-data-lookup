#!/usr/local/bin/python3
import requests as r
import pandas as pd
import csv
import argparse

parser = argparse.ArgumentParser(description='Search for public records for properties in the City of Detroit')
parser.add_argument('handle', metavar='F', type=str, help='csv file to process')

args = parser.parse_args()

f = args.handle



def open_data_api_lookup(url):
	res = r.get(url)
	data_dict = res.json()
	return data_dict



def lookup_foreclosure_info(parcel):
	url = 'https://data.detroitmi.gov/resource/6gee-8nht.json?parcel_id=%s'
	formatted_url = url % parcel
	return open_data_api_lookup(formatted_url)

def lookup_tax_auction_status(parcel):
	url = 'https://data.detroitmi.gov/resource/fmwx-a6vr.json?parcel_id=%s'
	formatted_url = url % parcel
	return open_data_api_lookup(formatted_url)

def parcel_points_ownership(parcel):
	url = 'https://data.detroitmi.gov/resource/snut-x2sy.json?parcelnum=%s'
	formatted_url = url % parcel
	return open_data_api_lookup(formatted_url)


df = pd.read_csv(f)

parcels = df['Parcel'].tolist()
ownership_data = []
foreclosure_info = []
tax_auction_stats = []
for p in parcels:
	ownership_data_points = parcel_points_ownership(p)
	foreclosure_data_points = lookup_foreclosure_info(p)
	tax_auction_data_points = lookup_tax_auction_status(p)
	if len(foreclosure_data_points) > 0:
		if 'payment_plan' in foreclosure_data_points[0]:
			 foreclosure_data_points[0].pop('payment_plan')
		if 'due_2014' in foreclosure_data_points[0]:
			 foreclosure_data_points[0].pop('due_2014')
		if 'due_2013' in foreclosure_data_points[0]:
			 foreclosure_data_points[0].pop('due_2013')
		foreclosure_info.append(foreclosure_data_points[0])
	if len(tax_auction_data_points) > 0:
		tax_auction_stats.append(tax_auction_data_points[0])
	if len(ownership_data_points) > 0:
		if 'owner_country' in ownership_data_points[0]:
			ownership_data_points[0].pop('owner_country')
		if 'related_parcel' in ownership_data_points[0]:
			ownership_data_points[0].pop('related_parcel')
		if 'owner2' in ownership_data_points[0]:
			ownership_data_points[0].pop('owner2')
		if 'nez' in ownership_data_points[0]:
			ownership_data_points[0].pop('nez')
		ownership_data.append(ownership_data_points[0])
	
def write_file(fname, data):
	dict_keys = data[0].keys()
	with open(fname, 'w') as f:
		w = csv.DictWriter(f, dict_keys)
		w.writeheader()
		w.writerows(data)

parcel_name = 'parcel_points_%s' % f 
foreclosure_name = 'foreclosure_data_%s' % f
tax_auction_name = 'tax_auction_data_%s' % f

write_file(parcel_name, ownership_data)
write_file(foreclosure_name, foreclosure_info)
write_file(tax_auction_name, tax_auction_stats)

parcel_df = pd.read_csv(parcel_name)
foreclosure_df = pd.read_csv(foreclosure_name)
tax_auction_df = pd.read_csv(tax_auction_name)

joined_df = df.set_index('Parcel').join(parcel_df.set_index('parcelnum'), rsuffix='_parcel_points').join(foreclosure_df.set_index('parcel_id'), rsuffix='_foreclosure').join(tax_auction_df.set_index('parcel_id'), rsuffix='_tax_auction')
joined_df.to_csv('pure_merged_%s' % f)


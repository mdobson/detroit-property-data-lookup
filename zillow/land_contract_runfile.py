import time
import datetime
import pandas as pd
import zillow_functions as zl
import chromedriver_binary

url = 'https://www.zillow.com/homes/for_sale/Detroit-MI/pmf,pf_pt/17762_rid/LAND-CONTRACT_att/globalrelevanceex_sort/42.858853,-82.409821,41.721105,-84.38736_rect/8_zm/'

output_data = []

# Initialize the webdriver.
driver = zl.init_driver(chromedriver_binary.chromedriver_filename)

# Go to www.zillow.com/homes
zl.navigate_to_website(driver, url)

raw_data = zl.get_html(driver)
print("%s pages of listings found" % str(len(raw_data)))

# Take the extracted HTML and split it up by individual home listings.
listings = zl.get_listings(raw_data)
print("%s home listings scraped\n***" % str(len(listings)))

# For each home listing, extract the 11 variables that will populate that 
# specific observation within the output dataframe.
for home in listings:
				new_obs = []
				parser = zl.html_parser(home)

				# Street Address
				new_obs.append(parser.get_street_address())

				# City
				new_obs.append(parser.get_city())

				# State
				new_obs.append(parser.get_state())

				# Zipcode
				new_obs.append(parser.get_zipcode())

				# Price
				new_obs.append(parser.get_price())

				# Sqft
				new_obs.append(parser.get_sqft())

				# Bedrooms
				new_obs.append(parser.get_bedrooms())

				# Bathrooms
				new_obs.append(parser.get_bathrooms())

				# Days on the Market/Zillow
				new_obs.append(parser.get_days_on_market())

				# Sale Type (House for Sale, New Construction, Foreclosure, etc.)
				new_obs.append(parser.get_sale_type())

				# URL for each house listing
				new_obs.append(parser.get_url())

				# Append new_obs to list output_data.
				output_data.append(new_obs)

# Close the webdriver connection.
zl.close_connection(driver)

# Write data to data frame, then to CSV file.
file_name = "scraped_land_contracts_base_%s_%s.csv" % (str(time.strftime("%Y-%m-%d")), 
									 str(time.strftime("%H%M%S")))
columns = ["address", "city", "state", "zip", "price", "sqft", "bedrooms", 
	 "bathrooms", "days_on_zillow", "sale_type", "url"]
df = pd.DataFrame(output_data, columns = columns)
today = datetime.date.today()
time_tuple = (today.year, today.month, today.day, 0, 0, 0, 0, 0, 0)
df['date_scraped'] = time.strftime('%m/%d/%Y', time_tuple)
df.drop_duplicates().to_csv(
file_name, index = False, encoding = "UTF-8"
)



# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import time
import datetime


class JobsSpider(scrapy.Spider):
	name = 'jobs'
	allowed_domains = ['craigslist.org']
	start_urls = ['https://detroit.craigslist.org/search/wyn/reo?query=detroit+land+contract&availabilityMode=0&sale_date=all+dates']

	def parse(self, response):
		titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
		time = response.xpath('//time[@class="result-date"]/text()').extract()
		links = response.xpath('//a[@class="result-title hdrlnk"]/@href').extract()
		d = { 'dates': time, 'titles': titles, 'links': links }
		today = datetime.date.today()
		time_tuple = (today.year, today.month, today.day, 0, 0, 0, 0, 0, 0)
		df['date_scraped'] = time.strftime('%m/%d/%Y', time_tuple)
		datestr = time.strftime('%m_%d_%Y', time_tuple)
		df = pd.DataFrame(data=d)
		df.to_csv('craigslist_%s.csv' % datestr, columns=['dates', 'titles', 'links'])
		

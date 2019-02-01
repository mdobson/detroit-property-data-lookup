# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class JobsSpider(scrapy.Spider):
	name = 'jobs'
	allowed_domains = ['waynecounty.com']
	start_urls = ['https://pta.waynecounty.com/Home/PropertySearch']

	def parse(self, response):
		

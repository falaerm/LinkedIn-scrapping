import scrapy, smtplib, os, time, schedule
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scrapy.crawler import CrawlerProcess, CrawlerRunner
# text cleaning
import re, csv
import pandas as pd
#from google.colab import auth
import gspread
from google.auth import default
#from gspread_dataframe import get_as_dataframe, set_with_dataframe
#import gspread_dataframe as gd

class LinkedJobsSpider1(scrapy.Spider):
    name = "linkedin_jobs1"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Graduate%20Program%20Commodities&location=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())


        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

class LinkedJobsSpider2(scrapy.Spider):
    name = "linkedin_jobs2"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())


        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

class LinkedJobsSpider3(scrapy.Spider):
    name = "linkedin_jobs3"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())


        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

class LinkedJobsSpider4(scrapy.Spider):
    name = "linkedin_jobs4"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())


        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

class LinkedJobsSpider5(scrapy.Spider):
    name = "linkedin_jobs5"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())

        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

class LinkedJobsSpider6(scrapy.Spider):
    name = "linkedin_jobs6"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())

        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

class LinkedJobsSpider7(scrapy.Spider):
    name = "linkedin_jobs7"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())

        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

class LinkedJobsSpider8(scrapy.Spider):
    name = "linkedin_jobs8"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())

        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

class LinkedJobsSpider9(scrapy.Spider):
    name = "linkedin_jobs9"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #Geneva
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trading%20Operator%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Shipping%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Invoicing%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Contract%20Commodity%20Commodities&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trainee%20Internship%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Freight%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Sales%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?l=fr_FR&keywords=Trade%20Finance%20Commodity&location=Gen%C3%A8ve%2C%20Suisse&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #UK
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Sales%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Operator%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Freight%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start=
    #'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Junior%20Commodity&location=United-Kingdom&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='
    #api_url='https://www.linkedin.com/jobs/search/?currentJobId=3813424881&geoId=104406358&keywords=junior%20commodity&location=Gen%C3%A8ve%2C%20Suisse&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    #l=fr_FR&
    title = []
    url = []
    listed_date = []
    company_name = []
    company_link = []
    company_location = []
    company_logo = []


    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("Num Jobs Returned")
        print(num_jobs_returned)

        for job in jobs:

            self.title.append(job.css("h3::text").get(default='not-found').strip())
            self.url.append(job.css(".base-card__full-link::attr(href)").get(default='not-found').strip())
            self.listed_date.append(job.css('time::attr(datetime)').get(default='not-found').strip())
            self.company_name.append(job.css('h4 a::text').get(default='not-found').strip())
            self.company_link.append(job.css('h4 a::attr(href)').get(default='not-found'))
            self.company_location.append(job.css('.job-search-card__location::text').get(default='not-found').strip())
            self.company_logo.append(job.css('img::attr(data-ghost-url)').get(default='not-found').strip())

        if num_jobs_returned > 0:
          first_job_on_page = int(first_job_on_page) + 25
          next_url = self.api_url + str(first_job_on_page)
          yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})


# Define a dictionary mapping spider names to keywords

process = CrawlerProcess()
process.crawl(LinkedJobsSpider1)
process.crawl(LinkedJobsSpider2)
process.crawl(LinkedJobsSpider3)
process.crawl(LinkedJobsSpider4)
process.crawl(LinkedJobsSpider5)
process.crawl(LinkedJobsSpider6)
process.crawl(LinkedJobsSpider7)
process.crawl(LinkedJobsSpider8)
process.crawl(LinkedJobsSpider9)
process.start()

scrappedD = [LinkedJobsSpider1,LinkedJobsSpider2,LinkedJobsSpider3,LinkedJobsSpider4,LinkedJobsSpider5, LinkedJobsSpider6, LinkedJobsSpider7, LinkedJobsSpider8, LinkedJobsSpider9]
table = []
for i in scrappedD:
    #for data, i in LinkedJobsSpider.company_name:
        #print(data)
    print()
    pt = i.__name__
    pp = i.api_url
    print(pp)
    print(pt)
    print(pt)
    data = pd.DataFrame(columns=['keyword','job_title','job_detail_url','job_listed','company_name','company_location'])
    
    start_index = pp.find('keywords=') + len('keywords=')
    end_index = pp.find('&', start_index)
    keyword = pp[start_index:end_index] if end_index != -1 else pp[start_index:]
    keyword = keyword.replace('%20', ' ')  # Replace '%20' with space
    
    data['job_title'] = i.title
    data['job_detail_url'] = i.url
    # Transform job_detail_url into hyperlinks
    #data['job_detail_url'] = [f'<a href="{url}" target="_blank">{url}</a>' for url in i.url]

    data['job_listed'] = i.listed_date
    data['company_name'] = i.company_name
    data['company_location'] = i.company_location
    data['keyword'] = f'{keyword}'
        
    data.head()
    print(data['keyword'])
    
    csv_file_path = f'./Downloads/{pt}.csv'
    data.to_csv(csv_file_path,index=False)
    # Convert DataFrames to HTML tables
    #data['job_detail_url'] = data['job_detail_url'].to_html(render_links=True, escape=False)
    html_table = data.to_html(index=False,render_links=True, escape=False)
    table.append(html_table)

# Set up email credentials
username = 'romain.afelt@gmail.com'
password = 'qwrm trmj uuzu pfpj'
#username = 'romain.afelt@hesge.ch'
#password = 'EgO-sUm1989@'

def sendMail():
   # Choose a random quote from the list
   
    # Set up the email server
    server = "smtp.gmail.com" 
    #server = "smtp.office365.com"
    port = 587 
    s = smtplib.SMTP(host = server, port = port) 
    s.starttls() 
    s.login(username, password) 
  
     # Create the email message
    msg = MIMEMultipart() 
    msg['To'] = "romain.afelt@gmail.com, romain.afelt@hesge.ch" 
    msg['From'] = username 
    msg['Subject'] = "We scrapped a List of Jobs for you!"
  
    # Combine HTML tables into a single HTML document
    #html_content = "<br><br>".join(table)

    # Attach HTML content to the email body
    #message.attach(MIMEText(html_content, "html"))  
    
    message = f"""Hi there, \n We have issued the list of jobs on LinkedIn related to Commodity for you"""
    msg.attach(MIMEText(message, 'html'))
    msg.attach(MIMEText(' '.join(table), 'html'))
  
     # Send the email
    s.send_message(msg)
    del msg
    s.quit()

# Run the `sendMail` function every day at 10:00 AM
schedule.every(2).minutes.do(sendMail)

# Keep the program running and check the schedule every minute
while True:
  schedule.run_pending()
  time.sleep(1) 

# Script for scraping data about jobs from dejobs.org

This repository contains script which scrapes data about jobs.
You can run it on your own computer by following next steps.
---

First of all you should clone this repo:
```
git clone https://github.com/RomanDomaratsky/jobby_scraper
```
Now you should download all the packages that we need:
```
pip install -r requirements.txt
```
After that go to the project folder and run command:
```
scrapy crawl job
```
You can also set number of pages by this command:
```
scrapy crawl job -a pages=<number_of_pages>
```
---
All the data will be stored into database and json file.

# Contact
Please feel free to contact us with any questions, suggestions or comments:

Roman Domaratsky 
roma.domaratsky@gmail.com

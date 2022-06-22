from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import w3lib.html
from scrapy.crawler import CrawlerProcess
from ..items import JobbyItem
import sys


class JobSpider(CrawlSpider):
    name = "job"

    rules = (
        Rule(LinkExtractor(allow='job/'),
             callback='job_parser'),
    )

    def __init__(self, pages='3', *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://dejobs.org/jobs/#{pages}']

    def job_parser(self, response):
        item = JobbyItem()
        for job in response.xpath('//div[@id="direct_innerContainer"]'):
            item['title'] = job.xpath('//span[@itemprop="title"]/text()').get()
            item['link'] = job.xpath('//div[@id="direct_applyButton"]//a/@href').get()
            item['organization'] = job.xpath('//span[@itemprop="name"]/text()').get()
            item['city'] = job.xpath('//span[@itemprop="addressLocality"]/text()').get()
            item['region'] = job.xpath('//span[@itemprop="addressRegion"]/text()').get()
            item['country'] = job.xpath('//meta[@itemprop="addressCountry"]/@content | //span['
                                       '@itemprop="addressCountry"]/text()').get()
            item['posted_date'] = job.xpath('//meta[@itemprop="datePosted"]/@content').get()
            item['description'] = w3lib.html.remove_tags(job.xpath('normalize-space(//div['
                                                                  '@id="direct_jobDescriptionText"])').get())
        yield item


process = CrawlerProcess(settings={
    'FEED_URI': 'jobs%(time)s.json',
    'FEED_FORMAT': 'json',
})

process.crawl(JobSpider)
if "twisted.internet.reactor" in sys.modules:
    del sys.modules["twisted.internet.reactor"]
process.start()

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import w3lib.html


class JobSpider(CrawlSpider):
    name = "job"
    start_urls = [
        'https://dejobs.org/jobs/',
    ]

    rules = (
        Rule(LinkExtractor(allow='job/',

                           deny_domains='https://dejobs.org/jobs/'),
             callback='job_parser'),
    )

    def job_parser(self, response):
        yield {
            'title': response.xpath('//span[@itemprop="title"]/text()').get(),
            'link': response.xpath('//div[@id="direct_applyButton"]//a/@href').get(),
            'organization': response.xpath('//span[@itemprop="name"]/text()').get(),
            'city': response.xpath('//span[@itemprop="addressLocality"]/text()').get(),
            'region': response.xpath('//span[@itemprop="addressRegion"]/text()').get(),
            'country': response.xpath(
                '//meta[@itemprop="addressCountry"]/@content | //span[@itemprop="addressCountry"]/text()').get(),
            'date': response.xpath('//meta[@itemprop="datePosted"]/@content').get(),
            'job_description': w3lib.html.remove_tags(response.xpath('normalize-space(//div['
                                                                     '@id="direct_jobDescriptionText"])').get()),
            }



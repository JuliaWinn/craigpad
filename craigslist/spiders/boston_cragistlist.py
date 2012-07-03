from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from craigslist.items import CraigslistItem

from scrapy.http import Request
import pymongo

import re

class BostonCragistlistSpider(CrawlSpider):
    name = 'craigslist'
    allowed_domains = ['boston.craigslist.org']
    start_urls = ['http://boston.craigslist.org/search/fua?query=chest+of+drawers']
    print 'started'
    
    rules = (
        Rule(SgmlLinkExtractor(allow=r'/[a-z]{3}/[a-z]{3}/.*\.html'), callback='get_image', follow=True),
        # looking for:
        # http://boston.craigslist.org/sob/fud/3111565340.html
        # http://boston.craigslist.org/gbs/fuo/3112103005.html
        Rule(SgmlLinkExtractor(allow=r'/search/fua\?query=.*'), callback='extract_links', follow=True),
    )
    
    # destination.drop()
    
    def extract_links(self, response):
        print 'extracting links'
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//p[@class="row"]//a/@href').extract()
        for link in links:
            return Request(link, callback=self.get_image)

    def get_image(self, response):
        hxs = HtmlXPathSelector(response)
        
        title = hxs.select('//h2//text()').extract()[0]
        re_money = re.search("\$([0-9]*?,[0-9]*)", title)
        if re_money:
            cost = re_money.group(1)
        else:
            cost = 0
        
        # check that it isn't a pottery barn scam
        if int(cost) > 500:
            pass
        else: 
            re_location = re.search("\((.*)\)", title)
            location = re_location.group(1)
        
            images = hxs.select('//img//@src').extract()
            if images:
                new_page = {}
                new_page['url'] = response.url
                new_page['title'] = title
                if cost == 0: cost = '????'
                new_page['cost'] = '$' + str(cost)
                if location: 
                    new_page['location'] = location
                new_page['images'] = images
                
                connection = pymongo.Connection()
                
                destination = connection['craigslist']['items']
                # def save(self, comment, db, coll):
                # x = connection[db][coll]
                destination.save(new_page, safe=True)
                # x.save(comment, safe=True)
        
        
        
        
        
        

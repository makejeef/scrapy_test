#coding:utf-8
import scrapy 
from scrapy.selector import Selector
from movie.items import MovieItem
from scrapy.http import Request
class MtimeSpider(scrapy.Spider):
	name='mtime'
	start_urls=['http://www.mtime.com/top/movie/top100/']
	url='http://www.mtime.com/top/movie/top100/'
	def parse(self,response):
		item=MovieItem()
		movies=response.xpath('.//*[@id="asyncRatingRegion"]/li')
		for movie in movies:
			num=movie.xpath('div[1]/em/text()').extract()
			name=movie.xpath('div[3]/h2/a/text()').re(r'(.*?)\(\d+\)')
			time=movie.xpath('div[3]/h2/a/text()').re(r'.*?(\d+)')
			director=movie.xpath('div[3]/p[1]/a/text()').extract()				
			actor=movie.xpath('div[3]/p[2]/a[1]/text()').extract()+movie.xpath('div[3]/p[2]/a[2]/text()').extract()
			star=movie.xpath('div[4]/b/span[1]/text()').extract()+movie.xpath('div[4]/b/span[2]/text()').extract()
			item['num']=num
			item['name']=name
			item['time']=time
			item['director']=director
			item['actor']=actor
			item['star']=star
			yield item
			
		nextlink=response.xpath('.//*[@id="PageNavigator"]/a/@href').extract()
		for link in nextlink:
			yield Request(link,callback=self.parse)

# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from shiyanlouGithub.items import repositoryItem


class GithubSpider(scrapy.Spider):
	name = 'github'
	allowed_domains=['github.com']
	
	@property
	def start_urls(self):
		url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
		return (url_tmpl.format(i) for i in range(1,5))

	def parse(self, response):
		for repo in response.css('li.public'):
			item = repositoryItem({
				'name': repo.css('div.mb-1 a::text').re_first('\n        (.+)'),
				'update_time': repo.css('div.mt-2 relative-time::attr(datetime)').extract_first()
				})
			repo_url = response.urljoin(repo.xpath('.//a/@href').extract_first())
			request = scrapy.Request(repo_url,callback = self.parse_other)
			request.meta['item'] = item
			yield request

	def parse_other(self, response):
		item = response.meta['item']
		parts = response.css('ul.numbers-summary span.num::text').re("\n\s*(.*)\n")
		log.msg('response url %s, %d found' % (response.url, len(parts)), log.DEBUG)
		if parts:
			parts[0] = parts[0].replace(',','')
			parts[1] = parts[1].replace(',','')
			parts[2] = parts[2].replace(',','')
			item['commits'] = int(parts[0])
			item['branches'] = int(parts[1])
			item['releases'] = int(parts[2])
			yield item
		else:
			yield item


# -*- coding: utf-8 -*-
import scrapy
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
        	yield item

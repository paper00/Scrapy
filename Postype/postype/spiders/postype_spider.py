# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.cookies import CookieJar
from postype.items import PostypeItem

class PostypeSpiderSpider(scrapy.Spider):
    name = 'postype_spider'
    allowed_domains = ['naneoneo.postype.com']
    login_url = 'https://www.postype.com/login'
    start_urls = ['https://naneoneo.postype.com/post/989997']

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        username = "yunduanling@naver.com"
        password = "*******"
        headerData = {
            "origin": "https://www.postype.com",
            "referer": "https://www.postype.com/login",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"
        }
        yield scrapy.FormRequest.from_response(response, formdata={'email': username, 'password': password},
                                               headers=headerData, callback=self.after_login, dont_filter=True)

    def after_login(self, response):
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)
        with open('cookies.txt', 'w') as f:
            for cookie in cookie_jar:
                f.write(str(cookie) + '\n')

        yield scrapy.Request(''.join(self.start_urls), callback=self.parse, dont_filter=True)

    def parse(self, response):
        # Save to Item
        postypeItem = PostypeItem()
        postypeItem['post_category'] = response.xpath("//div[@class='container']//div[@class='post-category text-truncate']/a/text()").extract()
        # postypeItem['post_category'] = response.xpath("//div[@class='container']//div[@class='post-category']/a/text()").extract()
        postypeItem['post_title'] = response.xpath("//div[@class='container']//h1[@class='post-title']/text()").extract()
        # postypeItem['post_title'] = response.xpath("//div[@class='container']//h1[@class='post-title']/span/text()").extract()
        postypeItem['post_subtitle'] = response.xpath("//div[@class='container']//div[@class='post-subtitle']/text()").extract()
        postypeItem['author'] = response.xpath("//div[@class='container']//div[@class='media-body']/h4/a/text()").extract()
        # postypeItem['author'] = response.xpath("//div[@class='container']//a[@class='list-inline-item']/text()").extract()
        postypeItem['post_content'] = response.xpath("//div[@class='container']//div[@id='post-content']").extract()

        print (postypeItem)
        yield postypeItem

        # Get next_link
        next_link = response.xpath("//div[@id='post-navbar']//div//ul/li/a[@class='btn-next-post btn btn-icon-text justify-content-md-end']/@href").extract()
        # next_link = response.xpath("//a[@class='btn-pager-next btn btn-icon-text justify-content-end post-bg-black']/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request(next_link, callback=self.parse, dont_filter=True)

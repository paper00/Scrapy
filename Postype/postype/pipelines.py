# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi

class PostypePipeline(object):
    def __init__(self, dbPool):
        self.dbPool = dbPool

    @classmethod
    def from_settings(cls, settings):
        adbParams = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DATABASE'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        # Connect Pool
        dbPool = adbapi.ConnectionPool('pymysql', **adbParams)

        return cls(dbPool)

    def process_item(self, item, spider):
        filename = ('').join(item['post_category']) + '.html'
        post_content = ('').join(item['post_content'])
        post_title = ('').join(item['post_title'])
        post_subtitle = ('').join(item['post_subtitle'])
        author = ('').join(item['author'])
        with open('.\\' + filename, 'a', encoding='utf-8') as f:
            f.write(post_title + '\t')
            f.write(post_subtitle + '\t')
            f.write(author)
            f.write(post_content)

        # sql -> pool
        query = self.dbPool.runInteraction(self.insert_into, item)
        query.addErrback(self.handle_error)

        return item

    def insert_into(self, cursor, item):
        sql = """
                    insert demo(title,subtitle, author) VALUES(%s,%s,%s)
        """
        cursor.execute(sql, (item['title'], item['subtitle'], item['author']))

    def handle_error(self, failure):
        if failure:
            print(failure)
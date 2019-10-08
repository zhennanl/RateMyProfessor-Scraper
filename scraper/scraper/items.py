# -*- coding: utf-8 -*-

# Define here the models for scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SchoolItem(scrapy.Item):
    # define the fields for item here like:
    name = scrapy.Field()
    score = scrapy.Field()
    rate_type = scrapy.Field()
    overall_quality_score = scrapy.Field()
    level_of_difficulty_score = scrapy.Field()
    com = scrapy.Field()
    credit = scrapy.Field()
    attendance = scrapy.Field()
    textbook = scrapy.Field()
    would_take_again = scrapy.Field()
    grade = scrapy.Field()
    comment = scrapy.Field()
    pass

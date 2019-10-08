# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Remember to add pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time


class SchoolPipeline(object):
    head_line = ["name","score","rate_type","overall_quality_score","level_of_difficulty_score",
                 "com","credit","attendance","textbook","would_take_again","grade","comment"]

    def open_spider(self, spider):
        self.f = open("./data2.csv", "a+", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(self.f, self.head_line)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(dict(item))
        # time.sleep(2)
        return item

    def close_spider(self, spider):
        self.f.close()

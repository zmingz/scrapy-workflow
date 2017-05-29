# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import os
import datetime
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from LagouSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT

from w3lib.html import remove_tags


def date_convert(value):
    try:
        date = datetime.datetime.strptime(value, SQL_DATE_FORMAT).date()
    except Exception as e:
        date = datetime.datetime.now().date()

    return date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def remove_comment_tags(value):
    # 去掉tags中提取的评论
    if "评论" in value:
        return ""
    return value


def return_value(value):
    return value


def convert_str2list(value):
    # 字符串转换为列表
    value_list = [value]
    return value_list


def remove_splash(value):
    # 去掉工作城市的斜线
    return value.replace("/", "")


def handle_jobaddr(value):
    addr_list = value.split("\n")  # 使用\n分离
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


def handle_tags(value):
    tags_list = value.replace(" ", "").split("\n")  # 去掉空格后用‘\n’组成列表
    tags = ",".join(tags_list).strip(",")  # 使用‘,’连接后把多余首尾的‘,’去除
    if tags is "":
        return "-空-"
    return tags


class LagouJobItemLoader(ItemLoader):
    # 自定义item loader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 获取拉勾网词条信息
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(input_processor=MapCompose(remove_splash))
    work_years = scrapy.Field(input_processor=MapCompose(remove_splash))
    degree_need = scrapy.Field(input_processor=MapCompose(remove_splash))
    job_type = scrapy.Field(input_processor=MapCompose(remove_splash))
    publish_time = scrapy.Field()
    tags = scrapy.Field(input_processor=MapCompose(remove_tags, handle_tags))
    job_advantage = scrapy.Field(input_processor=MapCompose(remove_tags))
    job_desc = scrapy.Field(input_processor=MapCompose(remove_tags))
    job_addr = scrapy.Field(input_processor=MapCompose(remove_tags, handle_jobaddr))
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        # 执行具体的插入
        insert_sql = """
            insert into lagou_job(url, url_object_id, title, salary, job_city, work_years, degree_need,
            job_type, publish_time, tags, job_advantage, job_desc, job_addr, company_url, company_name,
            crawl_time) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title), salary=VALUES(salary), job_city=VALUES(job_city), work_years=VALUES(work_years),
            degree_need=VALUES(degree_need), job_type=VALUES(job_type), publish_time=VALUES(publish_time), tags=VALUES(tags), job_advantage=VALUES(job_advantage), 
            job_desc=VALUES(job_desc), job_addr=VALUES(job_addr), company_url=VALUES(company_url), company_name=VALUES(company_name)
        """
        params = (
            self["url"], self["url_object_id"], self["title"], self["salary"],
            self["job_city"], self["work_years"], self["degree_need"], self["job_type"],
            self["publish_time"], self["tags"], self["job_advantage"], self["job_desc"],
            self["job_addr"], self["company_url"], self["company_name"],
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
        )

        return insert_sql, params

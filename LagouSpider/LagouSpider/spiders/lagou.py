# -*- coding: utf-8 -*-
import scrapy

from LagouSpider.items import LagouJobItemLoader, LagouJobItem
from LagouSpider.utils.common import get_md5
import datetime
import json


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    #爬去跟'爬虫'相关的职位
    start_urls = ["https://www.lagou.com"]
    #ajax请求页面
    CurPageUrl = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false"
    #搜索关键词
    keyword = "爬虫"
    #当前页面
    CurPage = 1
    #页面总数
    TotalPage = 0

    def start_requests(self):
        return [scrapy.http.FormRequest(url=self.CurPageUrl, formdata={"first":"true", "pn":str(self.CurPage), "kd":self.keyword}, callback=self.parse)]

    def parse(self, response):
        '''
        1/获取文章列表页中的具体url并交给解析函数进行页面具体字段的解析
        2/获取下一页的url并提交给scracy进行下载
        '''
        json_text = json.loads(response.body_as_unicode())
        # print(json_nodes)
        json_nodes = json_text["content"]["positionResult"]["result"]
        for json_node in json_nodes:
            post_node = "https://www.lagou.com/jobs/" + str(json_node["positionId"]) + ".html"
            yield scrapy.Request(url=post_node, callback=self.parse_job)

        # 获取职位总页面
        if json_text["content"]["pageNo"] == 1:
            TotalCount = json_text["content"]["positionResult"]["totalCount"]
            self.TotalPage = TotalCount / 15

        if self.CurPage <= self.TotalPage:
            self.CurPage = self.CurPage + 1
            yield scrapy.http.FormRequest(url=self.CurPageUrl, formdata={"first":"false", "pn":str(self.CurPage), "kd":self.keyword}, callback=self.parse)

    def parse_job(self, response):
        #解析拉勾网职位
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("tags", "ul.position-label")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.datetime.now())

        job_item = item_loader.load_item()

        return job_item



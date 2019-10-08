# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy import Request
import jsonpath, json
from school.items import SchoolItem


class TeacherSpiderSpider(scrapy.Spider):
    name = 'teacher_spider'
    allowed_domains = ['ratemyprofessors.com']
    base_url = "https://solr-aws-elb-production.ratemyprofessors.com//solr/rmp/select/?solrformat=true&rows=20&wt=json&json.wrf=noCB&callback=noCB&q=*%3A*+AND+schoolid_s%3A1232&defType=edismax&qf=teacherfirstname_t%5E2000+teacherlastname_t%5E2000+teacherfullname_t%5E2000+autosuggest&bf=pow(total_number_of_ratings_i%2C2.1)&sort=total_number_of_ratings_i+desc&siteName=rmp&rows=20&start={}&fl=pk_id+teacherfirstname_t+teacherlastname_t+total_number_of_ratings_i+averageratingscore_rf+schoolid_s&fq="
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "referer": "https://www.ratemyprofessors.com/search.jsp?queryoption=TEACHER&queryBy=schoolDetails&schoolID=1232&schoolName=University+of+North+Carolina+at+Chapel+Hill&dept=select"
    }
    headers1 = {
        "authority": "www.ratemyprofessors.com",
        "method": "GET",
        "path": "/ShowRatings.jsp?tid=2183841&showMyProfs=true",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "cookie": "notice=true; previousSchoolID=1232; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22187ba890-4e49-4ce9-8467-58604bfa0f58%22; _ga=GA1.2.1090600566.1570246267; _gid=GA1.2.478891723.1570246267; promotionIndex=0; ad_blocker_overlay_2019=true; trc_cookie_storage=taboola%2520global%253Auser-id%3D7b913cb6-22a0-4cda-b540-adecfc61f9ad-tuct429455b; showTeacherPopout=true",
        "pragma": "no-cache",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}

    def start_requests(self):
        for num in range(0, 2741, 20):
            url = self.base_url.format(num)
            yield Request(url, headers=self.headers)
            time.sleep(0.1)

    def parse(self, response):
        # print(response.status)
        text = response.text
        json_str = text[:-1].replace("noCB(", "")
        data_dict = json.loads(json_str)
        t_id_list = jsonpath.jsonpath(data_dict, "$..pk_id")
        for i in range(len(t_id_list)):
            # Get name
            name = jsonpath.jsonpath(data_dict, "$..teacherlastname_t")[i] + "," + jsonpath.jsonpath(data_dict, "$..teacherfirstname_t")[i]
            # Get score
            try:
                score =jsonpath.jsonpath(data_dict, "$..averageratingscore_rf")[i]
            except:
                print("This professor does not have an average score")
                score = None
            # Get the professor's id, used to construct the url address
            t_id = t_id_list[i]
            # The url of the first detail page
            for page in range(0, 3):
                detail_url = "https://www.ratemyprofessors.com/paginate/professors/ratings?tid={}&page={}&max=20&cache=false".format(t_id, page)
                # print(detail_url)
                yield Request(detail_url, method="GET", headers=self.headers1, callback=self.parse_json, meta={
                    "name": name, "score": score, "t_id": t_id
                })
                time.sleep(0.1)

    def parse_json(self, response):
        item = SchoolItem()
        # Take out item
        teacher_dict = response.meta
        # Get the html string of the professor's details and use xpath to parse
        # Save name
        item["name"] = teacher_dict["name"]
        # Save score
        item["score"] = teacher_dict["score"]
        json_text = response.text
        json_dict = json.loads(json_text)
        rate_list = jsonpath.jsonpath(json_dict, "$..ratings")[0]
        if not rate_list:
            yield item
        for i in range(len(rate_list)):
            # Type of review
            rate_type = jsonpath.jsonpath(json_dict, "$..quality")[i]
            # Save rate_type
            item["rate_type"] = rate_type
            # overall_quality
            overall_quality_score = jsonpath.jsonpath(json_dict, "$..rOverallString")[i]
            # Save overall_quality_score
            item["overall_quality_score"] = overall_quality_score
            # level_of_difficulty
            level_of_difficulty_score = jsonpath.jsonpath(json_dict, "$..rEasyString")[i]
            # Save level_of_difficulty
            item["level_of_difficulty_score"] = level_of_difficulty_score
            # COMP401
            com = jsonpath.jsonpath(json_dict, "$..rClass")[i]
            # Save com
            item["com"] = com
            # credit
            credit = jsonpath.jsonpath(json_dict, "$..takenForCredit")[i]
            # Save credit
            item["credit"] = credit
            # attendance
            attendance = jsonpath.jsonpath(json_dict, "$..attendance")[i]
            # Save attendance
            item["attendance"] = attendance
            # textbook
            textbook = jsonpath.jsonpath(json_dict, "$..rTextBookUse")[i]
            # Save textbook
            item["textbook"] = textbook
            # would take again
            would_take_again = jsonpath.jsonpath(json_dict, "$..rWouldTakeAgain")[i]
            # Save would_take_again
            item["would_take_again"] = would_take_again
            # grade received
            grade = jsonpath.jsonpath(json_dict, "$..teacherGrade")[i]
            # Save grade
            item["grade"] = grade
            # comment
            comment = jsonpath.jsonpath(json_dict, "$..rComments")[i]
            # Save comment
            item["comment"] = comment
            print("Operation is normal")
            yield item



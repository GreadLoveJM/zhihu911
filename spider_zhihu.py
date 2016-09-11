# coding=utf-8
import requests
import ConfigParser
import scrapy
import re
import json
import time
import datetime
import logging
from retrying import retry
from multiprocessing.pool import ThreadPool
import random
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

def remove_space(s):
    spa = re.compile('\s+')
    con = re.sub(spa, "", s)
    return con

def normolize_time(pre_time):

    '''this function is used to normolize time and return'''

    def match_partten(raw,parttenlst):
        for partten,convert in parttenlst:
            match_obj=re.match(partten,raw)
            if match_obj:
                return convert(match_obj)
        # raise myexception('can\'t normolize time')
    partten_convert_pairs=[
        (u'昨天',
            lambda m:datetime.date.today()-datetime.timedelta(days=1)),
        (u'(\d+):(\d+)',
            lambda m:datetime.date.today()),
        (u'(\d+)-(\d+)-(\d+)',
            lambda  m:datetime.date(int(m.group(1)),int(m.group(2)),int(m.group(3))))
    ]
    return match_partten(pre_time,partten_convert_pairs)

class myexception(Exception):
    def __init__(self, info):
        logging.warning(info)

_retry=retry(stop_max_attempt_number=5)

class Zhihu_spider(object):
    def __init__(self):
        self.pool = ThreadPool(20)
        conf = ConfigParser.ConfigParser()
        conf.read('config.ini')

        cookie = conf.get('webconf', 'Cookie')
        self.cook = {'Cookie': cookie}

        agent = conf.get('webconf', 'User-Agent')
        self.headers = {'User-Agent': agent}

        proxy=conf.get('proxyconf','use_proxy')
        if proxy=='false':
            self.useproxy=False

        else:
            self.useproxy=True

        print self.useproxy

    @retry(stop_max_attempt_number=3)
    def request_session(self,url,headers=None,use_proxy=None,method='get',**param):
        if not headers:
            headers={
            'Host':'www.zhihu.com',
            'Referer':url,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            }

        if self.useproxy:
            poolurl="http://10.9.8.40:9001/?max_num=5"
            html=requests.get(poolurl).text
            _json=json.loads(html)
            myproxy=_json['proxies'][0]
            use_proxy=re.sub('\s+','',myproxy)
            # use_proxy='http://179.93.163.120:8080'
        if method=='get':
            html = requests.get(url , verify=False,timeout=10, headers=headers , proxies={'http':use_proxy} , **param).text
            return html
        else:
            html = requests.post(url , verify=False, timeout=10 ,  headers=headers , proxies={'http':use_proxy} , **param)
            return html.text

    @retry(stop_max_attempt_number=3)
    def get_visitscount(self,url):
        html=self.request_session(url)
        look=re.search('itemprop="visitsCount" content="(\d+)"', html).group(1)
        return look

    def _extract_question_profile(self,ques_id):

        ''' this func used to extract the question's information '''

        url = "http://www.zhihu.com/question/{}?sort=created".format(ques_id)
        print url
        html = self.request_session(url)
        answers_count =scrapy.Selector(text=html).xpath('.//*[@id="zh-question-answer-num"]/@data-num').extract_first()
        if not answers_count:
            answers_count=0
        title=scrapy.Selector(text=html).xpath('.//span[@class="zm-editable-content"]/text()').extract_first()
        try:
            looked=self.get_visitscount(url)
        except:
            looked=0
        return {'ques_id':ques_id,'title':title,'answers_count':answers_count,'looked':looked}

    def _get_question_max_page(self, ques_id):

        ''' this method is used to get answers count of self.answers
        and return max pages '''

        url = "http://www.zhihu.com/question/{}?sort=created".format(ques_id)
        html = self.request_session(url)

        _sele = scrapy.Selector(text=html)
        answers_count = _sele.xpath('.//*[@id="zh-question-answer-num"]/@data-num').extract_first()
        self.answers_count = answers_count
        logging.debug('the number of all the answers is {}'.format(answers_count))

        # _page_lst = _sele.xpath('.//div[@class="zm-invite-pager"]/span')
        # if _page_lst:
        #     page = 0
        #     for each in _page_lst:
        #         item = each.xpath('string(.)').extract_first()
        #         try:
        #             if int(page) < int(item):
        #                 page = item
        #         except:
        #             pass
        # else:
        #     page = 1
        page=int(answers_count)//20+1

        logging.warning('this question of {} has {} page in total...'.format(ques_id,page))
        return page

    @_retry
    def _extract_one_question_page(self, page, chick=True):

        '''extract one page and get a comment_item list
        then use the func _extract_comment_item and return a list of  extract result'''

        logging.debug('crawling page {}..'.format(page))
        url = "http://www.zhihu.com/question/{}?sort=created&page={}".format(self.ques_id, page)
        html = self.request_session(url)
        answer_wrap = scrapy.Selector(text=html).xpath('.//div[@id="zh-question-answer-wrap"]/div[@tabindex="-1"]')
        comments=self.pool.map(self._extract_comment_item,answer_wrap)
        if chick == True:
            if len(comments) == 20:
                return comments
            else:
                print html
                raise myexception('page {} has not reach 20 | retrying...'.format(page))
        else:

            return comments

    def _extract_comment_item(self, selector):

        '''this func is used to extract infomation of each answer and return'''

        answer_id = selector.xpath('./@data-aid').extract_first()
        _votebar = selector.xpath('.//*[@class="zm-votebar"]')
        if _votebar:
            agree = _votebar.xpath('.//button[@class="up "]/span[@class="count"]/text()').extract_first()
        else:
            agree = 0

        _con = selector.xpath('.//div[@class="zm-editable-content clearfix"]')
        if _con:
            content = _con[0].xpath('string(.)').extract_first()
        else:
            content = ""

        _date=selector.xpath('.//a[@class="answer-date-link meta-item"]/text()').extract_first()
        pre_time=_date.split(" ")[1]
        pubtime=normolize_time(pre_time)

        _comment=selector.xpath('.//a[@name="addcomment"]')[0].xpath('string(.)').extract_first()
        _comment1=remove_space( _comment)
        partten=re.match(u'(\d+)条评论', _comment1)
        if partten:
            comment_count=partten.group(1)
        else:
            comment_count=0
        return {'ques_id':self.ques_id,'answer_id': answer_id, 'agree': agree, 'content': remove_space(content),'pubtime':pubtime,'comment_count':comment_count}

    def start_crwal_question(self, ques_id):

        '''this func starts crawling by single thread'''

        self.ques_id = ques_id
        max_page = self._get_question_max_page(self.ques_id)
        for each in range(1, int(max_page) + 1):
            if each == int(max_page):
                comments = self._extract_one_question_page(each, chick=False)
            else:
                comments = self._extract_one_question_page(each,chick=False)
            for comment in comments:
                yield comment
            # time.sleep(random.randrange(3,5))
        logging.warning('{} answers of the question {} is done'.format(self.answers_count,ques_id))

    def check_question_title(self,title,keyword,name):
        keywords=keyword.split(' ')
        if name in title:
            for each in keywords:
                if each in title:
                    return True
        return False

    def load_next_page(self,topic_id,offset=None):
        url='https://www.zhihu.com/topic/{}/hot'.format(topic_id)
        headers={
            'Host':'www.zhihu.com',
            'Origin':'https://www.zhihu.com',
            'Referer':'https://www.zhihu.com/topic/{}/hot'.format(topic_id),
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'X-Xsrftoken':self.token
        }
        param={
            'start':'0',
            'offset':offset
        }
        html=self.request_session(url,headers=headers,method='post',data=param)
        try:
            _html=json.loads(html)
            load_html=_html['msg']
            return load_html
        except:
            print html

    def _extract_load_page(self,name,html):
        selector=scrapy.Selector(text=html)
        content_area=selector.xpath('.//div[@itemprop="question"]')
        for each in content_area:
            offset= each.xpath('./@data-score').extract_first()


            title=each.xpath('.//a[@class="question_link"]/text()').extract_first()
            print remove_space(title)
            check_result=self.check_question_title(title,'人品 性格 演技',name)
            if check_result:
                href=each.xpath('.//a[@class="question_link"]/@href').extract_first()
                ques_id=re.search('/(\d+)', href).group(1)
                with open('temp/ques_link','a') as f:
                    print ques_id
                    f.write(ques_id+'\n')

        return {'offset':offset}

    def start_crawl_topic(self,name,topic_id):
        def get_token():
            url="https://www.zhihu.com/topic/{}/hot".format(topic_id)
            headers={
            'Host':'www.zhihu.com',
            'Referer':'https://www.zhihu.com/topic/{}/hot'.format(topic_id),
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            }
            html=requests.get(url, verify=False,headers=headers).text
            token=re.search('<input type="hidden" name="_xsrf" value="(.*?)"/>', html).group(1)
            return token
        offset=None
        artical_num=0
        self.token=get_token()


        while(True):
            load_html=self.load_next_page(topic_id,offset)
            num=load_html[0]
            artical_num+=num
            if num!=0:
                html=load_html[1]
                try:
                    result=self._extract_load_page(name,html)
                    offset=result['offset']
                    print offset
                except:
                    print html
                time.sleep(random.randrange(5,7))
            else:
                break

        logging.warn(' the topic of {} is done'.format(name))



if __name__ == '__main__':
    pass


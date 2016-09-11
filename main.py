import spider_zhihu
import re
import logging
from writers.mysql_writer import GetConnect
from multiprocessing.pool import ThreadPool
def space(s):
    sp=re.compile('\s+')
    con=re.sub(sp,"",s)
    return con

def start_crawl(ques_id):
    p = spider_zhihu.Zhihu_spider()
    db=GetConnect()
    ques=p._extract_question_profile(ques_id)
    c= (ques['ques_id'], ques['title'], ques['answers_count'], ques['looked'])
    db.insertInto_zhihu_question(c)
    print ques['ques_id'], ques['title'], ques['answers_count'], ques['looked']
    logging.warning('start crawl the answer of {}'.format(ques_id))

    coms = p.start_crwal_question(ques_id)
    for each in coms:
        s = (each['ques_id'], each['answer_id'], each['pubtime'], each['agree'], each['content'], each['comment_count'])
        db.insertInto_zhihu_answer(s)
        print each['ques_id'], each['answer_id'], each['pubtime'], each['agree'], each['content'], each['comment_count']

def main():
    pool=ThreadPool(10)
    file=open('temp/ques_link')
    lines=file.readlines()
    idlst=[]
    for line in lines:
        if space(line):
            idlst.append( space(line))
    file.close()
    print idlst
    pool.map(start_crawl,idlst)

def debug():
    file=open('temp/ques_link')
    lines=file.readlines()
    file.close()
    quesid_set=set()
    for line in lines:
        if space(line)!='':
            quesid_set.add(space(line))
    quesid_lst=list(quesid_set)
    for each in quesid_lst:

        start_crawl(each)

def get_topic():
    p=spider_zhihu.Zhihu_spider()
    with open('temp/topic') as f:
        for line in f.readlines():
            name=line.split(' ')[0]
            topic_id=line.split(' ')[1]
            print name,topic_id
            p.start_crawl_topic(name,space(topic_id))


if __name__ == '__main__':
    # get_topic()
    debug()

import requests
import json
import os
cook={'Cookie':'d_c0="AGAAz9upQAqPTgb776Usp-71E5oiQOO-gjs=|1468918186"; _za=4a93c142-ec94-4057-951e-e90098bd2b42; _zap=d1cbeac6-11c9-4266-90c5-ec7778fb9ca5; _xsrf=06ef6be6432eeeb5889b4e177126f72f; imhuman_cap_id="N2FkODNkNTA2MmMzNGNjZGI5OWE0YzNmNTQzOWVkODU=|1473218518|db0461f15ba797a106e2948e48fe0721db852a19"; s-q=%E8%83%A1%E6%AD%8C; s-i=3; sid=b1gmdgto; l_n_c=1; q_c1=36503217a24f463ea312a4e9a052f34d|1473220381000|1473220381000; cap_id="YjFkM2RkODg0ZTI1NDE0ODkzYzkyNmFkZGZhM2JiNTY=|1473220381|2ce394af04ef3da65b234a418b376aee712c2917"; l_cap_id="ZGUwYWQ5ZDZkNjI3NGQxY2I3NGU2NzA2ZTcxMzU1OWM=|1473220381|b92d5824ea9d34ff466c02c084c10831fb4c702c"; __utmt=1; login="OTU0Zjk1ZmExNjQ0NDIyZDlkN2I4NDk0MzFkMTU3ZmQ=|1473220895|44c7beb84fb1c6970ae0e00d0217d681921aa31f"; __utma=51854390.1808662302.1469782726.1473157620.1473217225.16; __utmb=51854390.43.9.1473220566275; __utmc=51854390; __utmz=51854390.1473217225.16.14.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.100--|2=registration_date=20160728=1^3=entry_date=20160728=1; a_t="2.0AICA8U4XTAoXAAAALh73VwCAgPFOF0wKAGAAz9upQAoXAAAAYQJVTR8e91cAj3oD0OihWS6rE20JEwu_kFeBpPdVBm6sA0QbUHNOLyZPuNLiv6ojEg=="; z_c0=Mi4wQUlDQThVNFhUQW9BWUFEUDI2bEFDaGNBQUFCaEFsVk5IeDczVndDUGVnUFE2S0ZaTHFzVGJRa1RDNy1RVjRHazl3|1473220910|86aec20e71d92049d52c4ef281dd18b5ad700c7d'}
cook={'Cookie':'d_c0="AGAAz9upQAqPTgb776Usp-71E5oiQOO-gjs=|1468918186"; _za=4a93c142-ec94-4057-951e-e90098bd2b42; _zap=d1cbeac6-11c9-4266-90c5-ec7778fb9ca5; _xsrf=06ef6be6432eeeb5889b4e177126f72f; imhuman_cap_id="N2FkODNkNTA2MmMzNGNjZGI5OWE0YzNmNTQzOWVkODU=|1473218518|db0461f15ba797a106e2948e48fe0721db852a19"; l_n_c=1; q_c1=36503217a24f463ea312a4e9a052f34d|1473220381000|1473220381000; s-q=%E8%83%A1%E6%AD%8C; s-i=1; sid=dlodnlod; __utmt=1; l_cap_id="YWNlOGFiMWRmMzdmNDA3YmFkZWJiNGNhMzRiMmMyYTc=|1473238543|e1c74b9c062eb341e493b3e72b67c4d1fdda4ca3"; cap_id="MjBkNGIyZjY5NjEzNDNhOGJhZjBiMTRhNjFiNjE5ZmI=|1473238543|3850a6784690d6f2ba902271a8e0522e7da3aa3d"; __utma=51854390.1808662302.1469782726.1473237518.1473238427.20; __utmb=51854390.8.10.1473238427; __utmc=51854390; __utmz=51854390.1473238427.20.18.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|2=registration_date=20160728=1^3=entry_date=20160907=1; n_c=1'}
# url1='https://www.zhihu.com/topic/19656332/hot'
# head={
#      'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
# }
# html=requests.get(url1,cookies=cook,headers=head).text
# # print html
#
# url='https://www.zhihu.com/topic/19656332/hot'
# headers={
#     'Host':'www.zhihu.com',
#     # 'Origin':'https://www.zhihu.com',
#     'Referer':'http://www.zhihu.com/explore',
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
#     'X-Requested-With':'XMLHttpRequest',
#     # 'X-Xsrftoken':'06ef6be6432eeeb5889b4e177126f72f'
# }
# data={
#     'start':'0',
#     'offset':None
# }
# html1=requests.post(url,headers=headers,data=data,cookies=cook).text
#
# _html=json.loads(html1)
# load_html=_html['msg']
# number=load_html[0]
# msg=load_html[1]
# print number
# print msg
#
# url="http://www.zhihu.com/explore"
# html=requests.get(url,headers=headers,verify=False)
# print html.request.headers


path= os.path.abspath('./temp/yangmi')
print path
isExists=os.path.exists(path)


if not isExists:

    print path

    os.makedirs(path)

from pyquery import PyQuery as pq

import requests
import time
import json


headers = {
    'User-Agent': 'spider'
}

def get_raw_data(weibo_id):

    def repeat_func():
        res = requests.get('https://weibo.com/u/%s?is_all=1' % weibo_id, headers=headers).content
        doc = pq(res)

        text = doc.text()

        pt = '$CONFIG[\'page_id\']=\''
        start = text.index(pt)
        end = text.index('\';', start+len(pt))
        page_id = text[start+len(pt):end]
        print (page_id)

        n_follow, n_fans, n_posts = [pq(_).text() for _ in doc('.tb_counter strong')]
        print (n_follow, n_fans, n_posts)

        weibo_avatar_url = 'http:' + doc('.photo_wrap>img').attr('src')
        name = doc('.username').text()
        description = doc('.pf_intro').text()
        print (weibo_avatar_url, name, description)

        return n_fans, n_posts, n_follow, weibo_avatar_url, name, description, doc, page_id

    n_fans, n_posts, n_follow, weibo_avatar_url, name, description, doc, page_id = repeat_func()

    profile = {
        'id': 'weibo_%s' % weibo_id,
        'user_id': weibo_id,
        'fans_number': n_fans,
        'weibo_number': n_posts,
        'influence': {
            'n_fans': n_fans,
            'n_posts': n_posts
        }
    }

    posts = {}
    raw_posts = []
    analyzed_posts = []

    def parse_posts(d):
        for feed in d('.WB_feed_detail'):
            f = pq(feed).find('.WB_from>a')[0]
            t = f.attrib['title']
            post_id = f.attrib['name']
            ts = f.attrib['date']

            content = pq(feed).find('.WB_text').text()
            print (content)

            handle = pq(feed).parent().find('.WB_feed_handle')
            zhuan, ping, zan = [pq(_[0][0][1]).text() for _ in handle.find('.pos')[1:]]

            try:
                zhuan = int(zhuan)
            except:
                zhuan = 0

            try:
                ping = int(ping)
            except:
                ping = 0

            try:
                zan = int(zan)
            except:
                zan = 0

            print (zhuan, ping, zan)
            print ('*'*80)

            raw_post = {
                'id': 'post_%s' % post_id,
                'crawler_time': t,
                'crawler_time_stamp': ts,
                'is_retweet': '0',
                'user_id': weibo_id,
                'nick_name': '',
                'tou_xiang': '',
                'user_type': '',
                'weibo_id': post_id,
                'weibo_content': content,
                'zhuan': '%d' % zhuan,
                'ping': '%d' % ping,
                'zhan': '%d' % zan,
                'url': '',
                'device': '',
                'locate': '',
                'time': t,
                'time_stamp': ts,
                'r_user_id': '',
                'r_nick_name': '',
                'r_user_type': '',
                'r_weibo_id': '',
                'r_weibo_content': '',
                'r_zhuan': '%d' % zhuan,
                'r_ping': '%d' % ping,
                'r_zhan': '%d' % zan,
                'r_url': '',
                'r_device': '',
                'r_location': '',
                'r_time': t,
                'r_time_stamp': ts,
                'pic_content': '',
            }
            if post_id in posts:
                return True

            posts[post_id] = raw_post
            raw_posts.append(raw_post)

        return False

    parse_posts(doc)

    pagebar = 0

    while True:
        data = {
            'ajwvr': 6,
            'domain': 100505,
            'is_all': 1,
            'pagebar': pagebar,
            'pl_name': 'Pl_Official_MyProfileFeed__21',
            'id': page_id,
            'script_uri': '/u/%s' % weibo_id,
            'feed_type': 0,
            'page': 1,
            'pre_page': 1,
            'domain_op': 100505,
            '__rnd': int(time.time()),
        }

        def repeat_func():
            page = requests.get('http://weibo.com/p/aj/v6/mblog/mbloglist', params=data, headers=headers).text
            page = json.loads(page)
            return page
        page = repeat_func()

        time.sleep(2)
        if not page['data'].strip():
            break

        d = pq(page['data'])
        dup = parse_posts(d)
        if dup:
            break

        if pagebar > 5:
            break

        pagebar += 1

    profile_data = {
        'profile': profile,
        'raw_posts': raw_posts,
        'weibo_avatar_url': weibo_avatar_url,
        'name': name,
        'description': description
    }
    return profile_data


from pprint import pprint

with open ('weibo.json', 'w') as f:
    result = get_raw_data(2624246740) 
    f.write(json.dumps(result))

print ('done')


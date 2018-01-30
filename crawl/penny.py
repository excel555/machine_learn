
from elasticsearch import Elasticsearch

import requests


es = Elasticsearch('106.15.52.233')

print (es.ping())


keywords = [
    '可口可乐',
    '百岁山',
]


query_dsl = {
    'query': {
        'bool': {
            'should': [{
                'query_string': {
                    'query': keyword,
                    'default_operator': 'AND',
                }
            } for keyword in keywords]
        }
    },
    'size': 100,
}

search_result = es.search('penny_weixin', 'biz', query_dsl, scroll='1m')
scroll_id = search_result['_scroll_id']

page = 0

bids = []

while True:
    body = []
    for _ in search_result['hits']['hits']:
        bid = _['_source']['bid']
        print (bid)

        search_result = es.search('penny_weixin', 'click', {
            'query': {
                'match': {
                    'url': bid
                }
            },
            'size': 10
        })

        posts_number = search_result['hits']['total']

        total_read = 0
        total_like = 0
        for c in search_result['hits']['hits']:
            total_read += c['_source']['read_num']
            total_like += c['_source']['like_num']

        if posts_number:
            avg_read = float(total_read) / len(search_result['hits']['hits'])
            avg_like = float(total_like) / len(search_result['hits']['hits'])

            print (posts_number, avg_read, avg_like, _['_source']['bid'], _['_source']['name'])
            bids.append({
                'bid': bid,
                'name': _['_source']['name'],
                'info': _['_source']['info'],
                'posts_number': posts_number,
                'avg_read': avg_read,
                'avg_like': avg_like,
            })

    search_result = es.scroll(scroll_id, scroll='1m')
    scroll_id = search_result['_scroll_id']

    if not search_result['hits']['hits']:
        break

    page += 1
    print (page)

with open('hearst2.json', 'w') as f:
    f.write(json.dumps(bids))
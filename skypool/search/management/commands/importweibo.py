from django.core.management import BaseCommand

from search.models import Article

from datetime import datetime
from pprint import pprint
import json
import random


class Command(BaseCommand):

    def handle(self, **kwargs):
        
        for _ in range(1, 3):
            with open ('weibo_%s.json' % _) as f:
                result = json.loads(f.read())

            profile = result['profile']

            for row in result['raw_posts']:
                try:
                    article = Article.objects.create(
                        source='weibo', 
                        source_url='https://weibo.com/u/%s' % row['user_id'],
                        create_time=row['time'],
                        title=row['weibo_content'][:20],
                        content=row['weibo_content'][:20000],
                        impression=profile['fans_number'],
                        engagement=int(row['zhuan'])+int(row['ping'])+int(row['zhan']),
                        sentiment=random.random()*0.4+0.5,
                    )
                    print (article.id)
                except:
                    print ('error')
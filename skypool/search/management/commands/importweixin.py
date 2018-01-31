from django.core.management import BaseCommand

from search.models import Article

from datetime import datetime
import json
import random


class Command(BaseCommand):

    def handle(self, **kwargs):
        
        for _ in range(1, 9):
            with open ('weixin_%s.json' % _) as f:
                result = json.loads(f.read())

            for row in result:
                try:
                    article = Article.objects.create(
                        source='wechat', 
                        source_url=row['url'],
                        create_time=datetime.fromtimestamp(row['post_date']),
                        title=row['title'],
                        content=row['content'][:20000],
                        impression=row['engagement_1'],
                        engagement=row['engagement_2'],
                        sentiment=random.random()*0.4+0.5,
                    )
                    print (article.id)
                except:
                    print ('error')
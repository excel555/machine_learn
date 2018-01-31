from django.core.management import BaseCommand

from search.models import Brand, Activity, Article, ActivityArticle, ActivityParam

from datetime import datetime
from pprint import pprint

import json
import random
import requests


API_URL = 'https://eastasia.api.cognitive.microsoft.com/luis/v2.0/apps/32774c6a-037f-4aa4-a7e4-9f34cb7078dd?subscription-key=09b0bab1aa5a45c18ed23ff889a98948&verbose=true&timezoneOffset=0&q=%s'


class Command(BaseCommand):

    def handle(self, **kwargs):
        brands = Brand.objects.all()
        
        for article in Article.objects.all():

            if ActivityArticle.objects.filter(article=article).exists():
                continue

            if article.source == 'weibo':
                text = article.content
            else:
                text = article.title

            for brand in brands:
                if brand.name not in text:
                    continue

                api_result = requests.get(API_URL % text).json()
                pprint (api_result)
                
                intent = api_result['topScoringIntent']['intent']
                popular = figure = market = innovation = capital = 0.0
                for row in api_result['intents']:
                    if row['intent'] == '知名度':
                        popular = row['score']
                    if row['intent'] == '公司形象':
                        figure = row['score']
                    if row['intent'] == '市场潜力':
                        market = row['score']
                    if row['intent'] == '创新':
                        innovation = row['score']
                    if row['intent'] == '资本':
                        capital = row['score']

                entities = []
                for row in api_result['entities']:
                    entity = row['entity']
                    entities.append(entity)

                create_new = False

                activity = Activity.objects.filter(intent=intent, brand=brand).first()
                if activity:
                    for entity in entities:
                        if not ActivityParam.objects.filter(name=entity).exists():
                            create_new = True
                else:
                    create_new = True

                if create_new:
                    activity = Activity.objects.create(
                        create_time=article.create_time,
                        brand=brand,
                        intent=intent,

                        influence=article.impression*0.5+article.engagement*2,
                        sentiment=article.sentiment,

                        popularity_score=popular,
                        figure_score=figure,
                        market_score=market,
                        innovation_score=innovation,
                        capital_score=capital,
                    )

                ActivityArticle.objects.create(activity=activity, article=article)

                for entity in entities:
                    ActivityParam.objects.create(activity=activity, name=entity, external_url='')

                print (brand.name, activity.id, intent)


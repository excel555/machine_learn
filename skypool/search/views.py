from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import Activity, Brand, Article, Tag

import json

json_response = lambda _: HttpResponse(json.dumps(_), 'application/json')


@csrf_exempt
def push_data(request):
    result = {
        'code': 0
    }
    return json_response(result)


def home(request):
    return render(request, 'home.html')


def search(request):
    ctx = {}
    ctx['q'] = q = request.GET.get('q', '')
    ctx['brand_id'] = brand_id = request.GET.get('brand_id', '')
    ctx['intent'] = intent = request.GET.get('intent', '')
    
    activities = Activity.objects.all()
    ctx['activities'] = activities

    return render(request, 'search.html', ctx)


def activity(request, activity_id):
    ctx = {}
    ctx['activity'] = activity = get_object_or_404(Activity, id=activity_id)

    return render(request, 'activity.html', ctx)


def brand(request, brand_id):
    ctx = {}
    ctx['brand'] = brand = get_object_or_404(Brand, id=brand_id)

    return render(request, 'brand.html', ctx)


def article(request, article_id):
    ctx = {}
    ctx['article'] = article = get_object_or_404(Article, id=article_id)

    return render(request, 'article.html', ctx)




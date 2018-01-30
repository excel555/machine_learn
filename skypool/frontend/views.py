from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Activity, Brand, Article, Tag

# Create your views here.
class HomeView(View):
    template_name = "frontend/home.html"

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, self.template_name, ctx)

class NewsIndexView(View):
    template_name = "frontend/news/index.html"

    def get(self, request, *args, **kwargs):
        ctx = {}
        ctx['q'] = q = request.GET.get('q', '')
        ctx['brand_id'] = brand_id = request.GET.get('brand_id', '')
        ctx['intent'] = intent = request.GET.get('intent', '')
        ctx['brands'] = Brand.objects.all()
        ctx['intents'] = Activity.objects.all().values('intent').distinct()

        activities = Activity.objects.all().order_by('create_time')
        paginator = Paginator(activities, 2)
        page = request.GET.get('page', 0)
        if page == 0:
            page = 1
        ctx['current_page'] = int(page)
        activities = paginator.get_page(page)
        ctx['activities'] = activities
        ctx['paginator'] = paginator
        return render(request, self.template_name, ctx)

class NewsShowView(View):
    template_name = "frontend/news/show.html"

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, self.template_name, ctx)

class ArticlesShowView(View):
    template_name = "frontend/articles/show.html"

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, self.template_name, ctx)

class BrandShowView(View):
    template_name = "frontend/brand/show.html"

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, self.template_name, ctx)


def articles_list(request):
    data = {
        'data': [],
    }
    return JsonResponse(data)

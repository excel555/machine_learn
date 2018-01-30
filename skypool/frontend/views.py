from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

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
        return render(request, self.template_name, ctx)

class NewsShowView(View):
    template_name = "frontend/news/show.html"

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

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Article


def blog_index(request):
    return HttpResponse('hello world')

class BasedListView(ListView):
    model = Article
    template_name = "blogapp/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.select_related('author', 'category').prefetch_related('tags').defer('content')
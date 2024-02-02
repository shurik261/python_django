from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Article


class ArticleListView(ListView):
    queryset = (
        Article.objects
            .filter(published_at__isnull=False)
            .order_by('-published_at')
    )


class ArticleDetailView(DetailView):
    model = Article


class LatestArticleFeed(Feed):
    title = 'Blog aerticles (latest)'
    description = 'Обновления об изменениях и дополнениях в статьях блога'
    link = reverse_lazy('blogapp:article')

    def items(self):
        return (
            Article.objects
                .filter(published_at__isnull=False)
                .order_by('-published_at')
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.body[:200]


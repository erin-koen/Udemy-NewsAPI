from django.urls import path
from news.api.views import (ArticleDetailApiView,
                            ArticleListCreateAPIView,
                            JournalistListCreateAPIView)
# from news.api.views import (article_detail_api_view,
#                             article_list_create_api_view)

urlpatterns = [
    # path("articles/", article_list_create_api_view, name="article-list"),
    # path("articles/<int:pk>", article_detail_api_view, name="article-detail")
    path("articles/",
         # need to call as_view() here to avoid typeError
         ArticleListCreateAPIView.as_view(),
         name="article-list"),
    path("articles/<int:pk>",
         ArticleDetailApiView.as_view(),
         name="article-detail"),
    path("journalists/",
         # need to call as_view() here to avoid typeError
         JournalistListCreateAPIView.as_view(),
         name="journalist-list"),
]

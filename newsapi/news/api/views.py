from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from news.models import Article
from news.api.serializers import ArticleSerializer


@api_view(["GET", "POST"])
def article_list_create_api_view(request):
    
    if request.method == "GET":
        articles = Article.objects.filter(active=True)
        # passing query set to the serializer
        # many so that serializer knows it needs to serve entire queryset
        serializer = ArticleSerializer(articles, many=True)
        # Response is a class that allows data to be rendered into arbitrary
        # media types. DRF decides which type of response is most approdpriate
        # based on request itself
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE", "PUT"])
def article_detail_api_view(request, pk):
    # validate primary key
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({"error": {
            "code": 404,
            "message": "Article not found!"
        }}, status= status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serialzer = ArticleSerializer(article)
    elif request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

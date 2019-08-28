from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers
from news.models import Article, Journalist
# define serializers for article model here


class ArticleSerializer(serializers.ModelSerializer):
    # allows us to create fields that aren't on the model as such (this
    # is tied by default to the function  get_samename below)
    time_since_publication = serializers.SerializerMethodField()
    # when you start tying things together with foreign keys - the below allows
    # you to return the __str__ from that field rather than FK
    # author = serializers.StringRelatedField()
    # unless you create a serializer for that table, in which case do the below
    # author = JournalistSerializer()

    class Meta:
        model = Article
        # fields = "__all__" <== all the fields
        # fields = ("title", "description", "body") <== just include these
        exclude = ("id",)  # <== include all but this one

    def get_time_since_publication(self, object):
        publication_date = object.publication_date
        now = datetime.now()
        time_delta = timesince(publication_date, now)
        return time_delta
    # for specific validation you can just add methods the same way you would
    # in the generic serializer class

    def validate(self, data):
            # check that description and title are different:
        if data["title"] == data["description"]:
            raise serializers.ValidationError(
                "Title and description must be different from one another.")
        return data
    # assume that field-level validators need to be in this format.
    # Some magic happens behind the scenes to tie it to title field in model

    def validate_title(self, value):
        if len(value) < 60:
            raise serializers.ValidationError(
                "the title must be at least 60 characters long"
            )
        return value


class JournalistSerializer(serializers.ModelSerializer):
    # to generate a list of links to endpoints for the specific records
    articles = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="article-detail")
    # articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Journalist
        fields = "__all__"


# class ArticleSerializer(serializers.Serializer):
#     # 99% of times we don't want to modify id
#     id = serializers.IntegerField(read_only=True)
#     author = serializers.CharField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     body = serializers.CharField()
#     location = serializers.CharField()
#     publication_date = serializers.DateField()
#     active = serializers.BooleanField()
#     # read only because django modifies these for us
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         print(validated_data)
#         return Article.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get(
#             'description', instance.description)
#         instance.body = validated_data.get('body', instance.body)
#         instance.location = validated_data.get('location', instance.location)
#         instance.publication_date = validated_data.get(
#             'publication_date', instance.publication_date)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate(self, data):
#         # check that description and title are different:
#         if data["title"] == data["description"]:
#             raise serializers.ValidationError(
#                 "Title and description must be different from one another.")
#         return data
#     # assume that field-level validators need to be in this format.
#     # Some magic happens behind the scenes to tie it to title field in model

#     def validate_title(self, value):
#         if len(value) < 60:
#             raise serializers.ValidationError(
#                 "the title must be at least 60 characters long"
#             )
#         return value

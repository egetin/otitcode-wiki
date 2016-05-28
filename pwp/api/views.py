# coding: utf-8

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
from models import Article, Comment
from utils import parseJSON, serialize_json

# Create your views here.
@require_http_methods(["POST"])
def AuthHandler(request):
    body = parseJSON(request.body)
    user = authenticate(username=body["username"], password=body["password"])
    if user is not None:
        token = Token.objects.get(user=user)
        if token is None:
            token = Token.objects.create(user=user)
        jsonresponse = {
            "username": user.username,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "email": user.email
        }
        response = HttpResponse()
        response["Authentication"] = token
        return response
    else:
        return JsonResponse({"error": "Invalid credentials!"}, status_code=401)

def index(request):
    response = HttpResponse("Hello World!")
    return response

@require_http_methods(["GET"])
def ArticlesHandler(request):
    user = request.user
    print user

    articles = Article.objects.all()
    data = []

    for article in articles:
        article_dict = model_to_dict(article)
        data.append(article_dict)

    return JsonResponse(data, safe=False)

@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def ArticleHandler(request, article_id=None):
    if request.method == "POST":
        # Create article
        user = request.user
        if user is None:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        body = parseJSON(request.body)
        try:
            serialized_data = serialize_json(body, 'api.Article')
        except (ValueError, KeyError):
            return JsonResponse({'error': 'JSON is invalid'}, status=409)

        new_article = serializers.deserialize('json', serialized_data).next().object
        new_article.owner = request.user

        new_article.save()

        return JsonResponse(model_to_dict(new_article))

    if request.method == "DELETE" and article_id is not None:
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Article does not exist"}, status=404)

        if article.owner == request.user:
            article.delete()
            return HttpResponse(status=204)
        else:
            return JsonResponse({"error": "Permission denied"}, status=401)


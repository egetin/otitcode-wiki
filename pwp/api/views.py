# coding: utf-8

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
from models import Article, Comment
from utils import parseJSON

# Create your views here.
@require_http_methods(["POST"])
def Auth(request):
    body = parseJSON(request.body)
    user = authenticate(username=body["username"], password=body["password"])
    if user is not None:
        token = Token.objects.create(user=user)
        #jsonresponse = {
        #        "username": user.name
        #        }
        print token.key

def index(request):
    response = HttpResponse("Hello World!")
    return response

def GetArticles(request):
    articles = Article.objects.all()
    data = []

    for article in articles:
        article_dict = model_to_dict(article)
        data.append(article_dict)

    return JsonResponse(data, safe=False)

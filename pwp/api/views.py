from django.http import HttpResponse, JsonResponse
from models import Article, Comment

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def GetArticles(request):
    articles = Article.objects.all()
    article_list = list(articles)

    return JsonResponse(article_list, safe=False)

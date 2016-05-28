# coding: utf-8

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from models import Article, Comment
from utils import parseJSON, serialize_json, to_dict
from django.db import IntegrityError

# Create your views here.
@require_http_methods(["POST", "DELETE"])
def AuthHandler(request):
    if request.method == "POST":
        body = parseJSON(request.body)
        user = authenticate(username=body["username"], password=body["password"])
        if user is not None:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            jsonresponse = {
                "username": user.username,
                "firstname": user.first_name,
                "lastname": user.last_name,
                "email": user.email
            }
            response = JsonResponse(jsonresponse)
            response["Authorization"] = token
            return response
        else:
            return JsonResponse({"error": "Invalid credentials!"}, status=401)

    if request.method == "DELETE":
        if request.user is not None:
            Token.objects.get(user=request.user).delete()
            response = HttpResponse(status=204)
            return response
        else:
            return JsonResponse({"error": "Invalid authentication token"}, status=401)

@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def ArticleHandler(request, article_id=None):
    if request.method == "GET" and article_id is None:
        articles = Article.objects.all()
        data = []

        for article in articles:
            article_dict = to_dict(article)
            data.append(article_dict)

        return JsonResponse(data, safe=False)

    if request.method == "GET" and article_id is not None:
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Article does not exist"}, status=404)

        article_dict = to_dict(article)
        return JsonResponse(article_dict, status=200)

    if request.method == "PUT" and article_id is not None:
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return JsonResponse({"error": "Article does not exist"}, status=404)

        if article.owner != request.user:
            return JsonResponse({"error": "Permission denied"}, status=401)

        data = parseJSON(request.body)
        try:
            article.topic = data["topic"]
        except KeyError:
            pass
        try:
            article.article_text = data["article_text"]
        except KeyError:
            pass

        article.save()
        return JsonResponse(to_dict(article), status=200)

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

        return JsonResponse(to_dict(new_article))

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


@require_http_methods(["PUT"])
def PasswordHandler(request):
    body = parseJSON(request.body)
    try:
        password = body["password"]
    except (ValueError, KeyError):
        return JsonResponse({'error': 'JSON is invalid'}, status=409)

    user = request.user
    user.set_password(password)
    user.save()

    token = Token.objects.create(user=user)
    response = HttpResponse(jsonresponse)
    response["Authorization"] = token


@require_http_methods(["GET", "PUT", "DELETE"])
def CurrentUserHandler(request):
    if request.method == 'GET':
        if request.user is not None:
            user_dict = to_dict(request.user)
            return JsonResponse(user_dict)
        else:
            return JsonResponse({"error": "User not logged in"}, status=404)


@require_http_methods(["GET", "PUT", "POST", "DELETE"])
def UserHandler(request, user_id=None):
    if request.method == 'GET' and user_id is None:
        users = User.objects.all()
        data = []

        for user in users:
            user_dict = to_dict(user)
            user_dict.pop("password", None)
            data.append(user_dict)

        return JsonResponse(data, safe=False)

    if request.method == 'GET' and user_id is not None:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)

        user_dict = to_dict(user)
        return JsonResponse(user_dict, status=200)

    if request.method == "POST":
        body = parseJSON(request.body)
        try:
            username = body["username"]
            password = body["password"]
        except (ValueError, KeyError):
            return JsonResponse({'error': 'JSON is invalid'}, status=409)

        try:
            user = User.objects.create_user(username, None, password)
            user.save()
        except IntegrityError:
            return JsonResponse({'error': 'Username already taken'}, status=409)

        token = Token.objects.get(user=user)
        if token is None:
            token = Token.objects.create(user=user)
        jsonresponse = {
            "username": user.username,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "email": user.email
        }

        response = JsonResponse(jsonresponse)
        response["Authorization"] = token

        return response



@require_http_methods(["GET"])
def CommentHandler(request, comment_id=None):
    if request.method == "GET" and comment_id is None:
        comments = Comment.objects.all()
        data = []

        for comment in comments:
            comment_dict = to_dict(comment)
            data.append(comment_dict)

        return JsonResponse(data, safe=False)

    if request.method == "GET" and comment_id is not None:
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({"error": "Comment does not exist"}, status=404)

        comment_dict = to_dict(comment)
        return JsonResponse(comment_dict, status=200)


@require_http_methods(["GET", "POST"])
def ArticleCommentHandler(request, article_id=None):
    if article_id is None:
        return JsonResponse({"error": "No article was defined."}, status=400)

    if request.method == "GET":
        try:
            comments = Comment.objects.filter(article=article_id)
        except Comment.DoesNotExist:
            return JsonResponse([], status=200)

        data = []
        for comment in comments:
            json_comment = to_dict(comment)
            data.append(json_comment)

        return JsonResponse(data, safe=False)

    if request.method == "POST":
        # Create comment
        user = request.user
        if user is None:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        body = parseJSON(request.body)
        try:
            serialized_data = serialize_json(body, 'api.Comment')
        except (ValueError, KeyError):
            return JsonResponse({'error': 'JSON is invalid'}, status=409)

        new_comment = serializers.deserialize('json', serialized_data).next().object
        new_comment.owner = request.user
        new_comment.article = Article.objects.get(pk=article_id)

        new_comment.save()

        return JsonResponse(to_dict(new_comment))

@require_http_methods(["GET"])
def UserCommentHandler(request, user_id=None):
    if user_id is None:
        return JsonResponse({"error": "No user was defined."}, status=400)

    if request.method == "GET":
        try:
            comments = Comment.objects.filter(owner=user_id)
        except Comment.DoesNotExist:
            return JsonResponse([], status=200)

        data = []
        for comment in comments:
            json_comment = to_dict(comment)
            data.append(json_comment)

        return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def UserArticleHandler(request, user_id=None):
    if user_id is None:
        return JsonResponse({"error": "No user was defined."}, status=400)

    if request.method == "GET":
        try:
            articles = Article.objects.filter(owner=user_id)
        except Article.DoesNotExist:
            return JsonResponse([], status=200)

        data = []
        for article in articles:
            json_article = to_dict(article)
            data.append(json_article)

        return JsonResponse(data, safe=False)

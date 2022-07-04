from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework_jwt.utils import jwt_decode_handler

from comment.models import Comment
from users.models import User
from video.models import Video

@csrf_exempt
@require_http_methods(["POST"])
def submit_comment(request, **kwargs):
    pk = kwargs.get('pk')
    video = Video.objects.all().filter(pk=pk).first()
    content = request.POST.get('content')
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    if content:
        new_comment= Comment(user=user,nickname=user.username,video=video,content=content)
        new_comment.save()
        return JsonResponse({"code":0,'msg':'评论成功!'})
    else:
        return JsonResponse({"code": 1, 'msg': '评论失败!'})

@csrf_exempt
@require_http_methods(["POST"])
def get_comments(request):
    video_id = request.POST.get('video_id')
    video = Video.objects.get(pk=video_id)
    if video:
        comments = video.comments.all().order_by('-timestamp').all().values('content', 'nickname', 'timestamp')
        comment_count = len(comments)

        return JsonResponse({
            'code': 1,
            'comments': list(comments),
            'comment_count': comment_count
        })
    else:
        return JsonResponse({
            'code': 0,
            'comment_count': 0
        })

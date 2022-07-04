from itertools import count

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.viewsets import ModelViewSet, ViewSetMixin
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler

from users.models import User
from .models import Video
from .serializers import VideoModelSerializer
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER # 生payload部分的方法
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER # 生成jwt的方法

class HomeViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    """视图集"""
    queryset = Video.objects.all()
    serializer_class = VideoModelSerializer

    @action(methods=['get'], detail=False)
    def home_list(self, request, cf, *args, **kwargs):
        obj = Video.objects.all().filter(classification=cf).filter(status=0)
        if obj:
            ser = VideoModelSerializer(instance=obj, many=True)
            return JsonResponse({
                'code': '0',
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return JsonResponse({
                'code': '1',
                'msg': '获取失败',
            })
''''
    @action(methods=['post'], detail=False)
    def search_list(self, request, type, *args, **kwargs):
        q = request.POST.get('q')
        if q:
            obj = Video.objects.filter(title__contains=q).filter(status=0)
        else:
            obj = Video.objects.filter(status=0)
        if type:
            obj = obj.annotate('like_count', count("liked")).order_by('-like_count')
        else:
            obj = obj.order_by('-view_count')
        if obj:
            ser = VideoModelSerializer(instance=obj, many=True)
            return JsonResponse({
                'code': '0',
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return JsonResponse({
                'code': '1',
                'msg': '获取失败',
            })

    def detail(self, request,  *args, **kwargs):
        pk = kwargs.get('pk')
        video= Video.objects.all().filter(pk=pk).first()
        if video :
            video.increase_view_count()
            ser = VideoModelSerializer(instance=video)
            return JsonResponse({
                'code': '0',
                'msg': '获取数据成功',
                'data': ser.data,
                'status': video.status
            })
        else:
            return JsonResponse({
                'code': '1',
                'msg': '获取数据失败',
                'status': video.status
            })'''

@csrf_exempt
@require_http_methods(["POST"])
def search_list(request, *args, **kwargs):
    type = kwargs.get('type')
    q = request.POST.get('q')
    if q:
        obj = Video.objects.filter(title__contains=q).filter(status=0)
    else:
        obj = Video.objects.filter(status=0)
    if type:
        obj = obj.annotate(like_count=Count('liked')).order_by('-like_count')
    else:
        obj = obj.order_by('-view_count')
    if obj:
        ser = VideoModelSerializer(instance=obj, many=True)
        return JsonResponse({
            'code': '0',
            'msg': '获取数据成功',
            'data': ser.data
        })
    else:
        return JsonResponse({
            'code': '1',
            'msg': '获取失败',
        })
@require_http_methods(["GET"])
def detail( request, *args, **kwargs):
    pk = kwargs.get('pk')
    video = Video.objects.all().filter(pk=pk).first()
    if video:
        video.increase_view_count()
        ser = VideoModelSerializer(instance=video)
        return JsonResponse({
            'code': '0',
            'msg': '获取数据成功',
            'data': ser.data,
            'status': video.status
        })
    else:
        return JsonResponse({
            'code': '1',
            'msg': '获取数据失败',
            'status': video.status
        })

@csrf_exempt
@require_http_methods(["POST"])
def like(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    if not user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    else:
        video_id = request.POST['video_id']
        video = Video.objects.get(pk=video_id)
        video.switch_like(user)
        return JsonResponse({"code": 0, "likes": video.count_likers()+100, "user_liked": video.user_liked(user)})

@csrf_exempt
@require_http_methods(["POST"])
def attention(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    print(user.pk)
    if not user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    else:
        #video_id = request.POST['video_id']
       # video = Video.objects.get(pk=video_id)
        username=request.POST.get('username')
        print(username)
        creator = User.objects.get(username=username)
        if  creator.pk is user.pk:
            return JsonResponse({"code": 1, "msg": "buenng guanzhuziji"})
        else:
            print(creator.user_attention(user))
            creator.switch_attention(user)
            print( creator.user_attention(user))
            return JsonResponse({"code": 0, "attentions": creator.count_attentions(),
                                 "user_attention": creator.user_attention(user)})


@csrf_exempt
@require_http_methods(["POST"])
def collect(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    if not user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    else:
        video_id = request.POST['video_id']
        video = Video.objects.get(pk=video_id)
        video.switch_collect(user)
        return JsonResponse({"code": 0, "collects": video.count_collecters(), "user_collected": video.user_collected(user)})



@csrf_exempt
@require_http_methods(["POST"])
def publish(request):
    cover = request.POST.get('cover')
    file = request.POST.get('file')
    title = request.POST.get('title')
    desc = request.POST.get('desc')
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    classification = request.POST.get('classification')
    if file:
        new_video = Video(creator=user.username, file=file, cover=cover, title=title, desc=desc, status=1, classification=classification)
        new_video.save()
        return JsonResponse({"code": 0, 'msg': '上传成功!'})
    else:
        return JsonResponse({"code": 1, 'msg': '上传失败!'})
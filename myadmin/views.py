from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
# Create your views here.
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler

import video
from users.forms import UserLoginForm

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from users.models import User
from video.models import Video
from video.serializers import VideoModelSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER # 生payload部分的方法
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER # 生成jwt的方法
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            payload = jwt_payload_handler(user)  # 生成payload, 得到字典
            token = jwt_encode_handler(payload)  # 生成jwt字符串
            return JsonResponse({'code': 0, 'msg': "登陆成功",'token': token })
        else:
            return JsonResponse({'code': 1, 'msg': "登陆失败"})

    else:
        return JsonResponse({'code': 1, 'msg': "请求方式错误"})


@csrf_exempt
def logout(request):
    return JsonResponse({'code': 0, 'msg': "注销成功"})

@csrf_exempt
@require_http_methods(["POST"])
def auditpass(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    if not user.is_staff:
        return JsonResponse({"code": 1, "msg": "没有权限"})
    else:
        video_id = request.POST['video_id']
        video = Video.objects.get(pk=video_id)
        video.status = 0
        video.save()
        return JsonResponse({"code": 0, "msg": "操作成功"})


@csrf_exempt
@require_http_methods(["POST"])
def auditnopass(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    if not (user.is_authenticated and request.user.is_staff):
        return JsonResponse({"code": 1, "msg": "没有权限"})
    else:
        video_id = request.POST['video_id']
        video = Video.objects.get(pk=video_id)
        video.delete()
        return JsonResponse({"code": 0, "msg": "操作成功"})



@require_http_methods(["GET"])
@csrf_exempt
def complaint_list(request, *args, **kwargs):
    obj = video.models.Video.objects.filter(status=2)
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
@csrf_exempt
def audit_list(request, *args, **kwargs):
    obj = video.models.Video.objects.filter(status=1)
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

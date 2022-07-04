from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, response
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler

import video
from video.models import Video
from video.serializers import VideoModelSerializer
from .forms import SignUpForm, UserLoginForm
from .serializers import UserModelSerializer
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER # 生payload部分的方法
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER # 生成jwt的方法
User = get_user_model()

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            payload = jwt_payload_handler(user)  # 生成payload, 得到字典
            token = jwt_encode_handler(payload)  # 生成jwt字符串
            return JsonResponse({'code': 0, 'msg': "登陆成功",'token': token })
        else:
            return JsonResponse({'code': 1, 'msg': "登陆失败"})

    else:
        return JsonResponse({'code': 1, 'msg': "请求方式错误"})

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password1 = form.cleaned_data.get('password1')
            if User.objects.filter(username=username).first() is not None:
                return JsonResponse({'code': 1, 'msg': "用户已存在"})
            else:
                form.save()
            return JsonResponse({'code': 0, 'msg': "注册成功"})
        else:
            return JsonResponse(form.errors, safe=False)
    else:
        return JsonResponse({'code': 1, 'msg': "请求方式错误"})

@csrf_exempt
def logout(request):
    return JsonResponse({'code': 0, 'msg': "注销成功"})

@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        newusername = request.POST.get('newusername')
        newpassword = request.POST.get('newpassword')
        if User.objects.filter(username=newusername).first() is not None:
            return JsonResponse({'errno': 1, 'msg': "用户已存在"})
        else:
            token=request.META.get("HTTP_AUTHORIZATION")
            token_user = jwt_decode_handler(token)
            user_id = token_user['user_id']
            user = User.objects.get(id=user_id)
            user.username = newusername
            user.password = newpassword
            user.save()
            #update_session_auth_hash(request, user)  # 更新session 非常重要！
            return JsonResponse({'code': 0, 'msg': "修改成功"})
    else:
        return JsonResponse({'code': 1, 'msg': "请求方式错误"})

@csrf_exempt
@require_http_methods(["GET"])
def get_like_count(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    if not user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    return JsonResponse({'code': 0, 'username': user.username, 'get_like_count': user.get_like_count(user)})

@require_http_methods(["GET"])
@csrf_exempt
def like_list(request, *args, **kwargs):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    loginuser = user
    #user = get_object_or_404(User, username=request.session.get('username', None))
    obj = Video.objects.filter(liked=loginuser)
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


@csrf_exempt
@require_http_methods(["GET"])
def create_list(request, *args, **kwargs):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    # user = get_object_or_404(User, username=request.session.get('username', None))
    obj = Video.objects.filter(creator=user.username).filter(status=0)
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

@csrf_exempt
@require_http_methods(["GET"])
def collect_list(request, *args, **kwargs):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    obj = Video.objects.filter(collected=user)
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


@csrf_exempt
@require_http_methods(["GET"])
def create_list2(request, *args, **kwargs):
    pk = kwargs.get('pk')
    user = User.objects.all().filter(pk=pk).first()
    obj = Video.objects.filter(creator=user.username).filter(status=0)
    like_count = user.get_like_count(user)
    if obj:
        ser = VideoModelSerializer(instance=obj, many=True)
        return JsonResponse({
            'code': '0',
            'msg': '获取数据成功',
            'get_like_count': like_count,
            'username': user.username,
            'data': ser.data
        })
    else:
        return JsonResponse({
            'code': '1',
            'msg': '没有作品',
            'get_like_count': like_count,
            'username': user.username,
        })


@csrf_exempt
@require_http_methods(["GET"])
def attention_list(request, *args, **kwargs):
    token = request.META.get("HTTP_AUTHORIZATION")
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    obj = User.objects.filter(attentioned=user)
    print(obj)
    if obj:
        ser = UserModelSerializer(instance=obj, many=True)
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

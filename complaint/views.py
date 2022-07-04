from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework_jwt.utils import jwt_decode_handler

from complaint.models import Complaint
from users.models import User
from video.models import Video

@csrf_exempt
@require_http_methods(["POST"])
def submit_complaint(request, **kwargs):
    pk = kwargs.get('pk')
    token = request.META.get("HTTP_AUTHORIZATION")
    print(token)
    token_user = jwt_decode_handler(token)
    user_id = token_user['user_id']
    user = User.objects.get(id=user_id)
    video = Video.objects.all().filter(pk=pk).first()
    video.status = 2
    video.save()
    new_complaint = Complaint(user=user, reason=request.POST.get('reason'), video=video,
                              content=request.POST.get('content'))
    new_complaint.save()
    return JsonResponse({"code":0,'msg':'举报成功!'})

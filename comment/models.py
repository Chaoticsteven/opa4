from django.db import models

# Create your models here.
import datetime

from django.conf import settings
from django.db import models
from video.models import Video


class CommentQuerySet(models.query.QuerySet):

    def get_count(self):
        return self.count()


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE,related_name='comments')
    content = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CommentQuerySet.as_manager()

    class Meta:
        db_table = "v_comment"

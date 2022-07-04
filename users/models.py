from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

import video
from opa4 import settings
from video.models import Video


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    # 关注你的用户
    attentioned = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   blank=True, related_name="attentioned_users")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    class Meta:
        db_table = "v_user"


    def switch_attention(self, user):
        if user in self.attentioned.all():
            self.attentioned.remove(user)
        else:
            self.attentioned.add(user)

    def count_attentions(self):
        return self.attentioned.count()

    def user_attention(self, user):
        if user in self.attentioned.all():
            return 0
        else:
            return 1

    def get_like_count(self, user):
        videos = Video.objects.filter(creator=user.username)
        sum = 0
        if videos:
            for x in videos:
                sum = sum + x.count_likers()
            return sum
        else:
            return 0


from django.db import models

# Create your models here.
import os

from django.conf import settings
from django.db import models
from django.dispatch import receiver


class VideoQuerySet(models.query.QuerySet):

    def get_count(self):
        return self.count()

    def get_published_count(self):
        return self.filter(status=0).count()

    def get_not_published_count(self):
        return self.filter(status=1).count()

    def get_published_list(self):
        return self.filter(clas=0).order_by('-create_time')

    def get_yule_list(self):
        return self.filter(classification=0).order_by('-view_count')

    def get_shenghuo_list(self):
        return self.filter(classification=1).order_by('-view_count')

    def get_keji_list(self):
        return self.filter(classification=2).order_by('-view_count')

    def get_yundong_list(self):
        return self.filter(classification=3).order_by('-view_count')

    def get_search_list(self, q):
        if q:
            return self.filter(title__contains=q).order_by('-create_time')
        else:
            return self.order_by('-create_time')

    def get_recommend_list(self):
        return self.filter(status=0).order_by('-view_count')[:4]


class Video(models.Model):
    STATUS_CHOICES = (
        ('0', '发布中'),
        ('1', '未发布'),
        ('2', '举报中'),
    )
    CF_CHOICES = (
        ('0', '娱乐'),
        ('1', '生活'),
        ('2', '科技'),
        ('3', '运动'),
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    classification = models.CharField(max_length=10, choices=CF_CHOICES, blank=True, null=True)
    #file = models.FileField(max_length=255)   #url
    #cover = models.ImageField(upload_to='cover/', blank=True, null=True)
    file = models.URLField(max_length=6000, blank=True, null=True)
    cover= models.URLField(max_length=6000, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True)
    view_count = models.IntegerField(default=0, blank=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   blank=True, related_name="liked_videos")
    collected = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       blank=True, related_name="collected_videos")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, max_length=20)

    creator = models.CharField(max_length=100, blank=True, null=True)

    objects = VideoQuerySet.as_manager()

    class Meta:
        db_table = "v_video"

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def switch_like(self, user):
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)

    def count_likers(self):
        return self.liked.count()

    def user_liked(self, user):
        if user in self.liked.all():
            return 0
        else:
            return 1

    def switch_collect(self, user):
        if user in self.collected.all():
            self.collected.remove(user)

        else:
            self.collected.add(user)

    def count_collecters(self):
        return self.collected.count()

    def user_collected(self, user):
        if user in self.collected.all():
            return 0
        else:
            return 1


'''@receiver(models.signals.post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    删除FileField文件
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)'''

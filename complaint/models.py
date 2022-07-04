from django.shortcuts import render
from django.db import models
from django.conf import settings
# Create your views here.
from video.models import Video


class ComplaintQuerySet(models.query.QuerySet):

    def get_count(self):
        return self.count()


class Complaint(models.Model):
    RE_CHOICES = (
        ('0', '色情'),
        ('1', '暴力'),
        ('2', '引战'),
        ('3', '违法犯罪'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    content = models.CharField(max_length=100,blank=True,null=True
                               )
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=10, choices=RE_CHOICES, blank=True, null=True)
    objects = ComplaintQuerySet.as_manager()

    class Meta:
        db_table = "v_complaint"

from rest_framework import serializers

from video.models import Video


class VideoModelSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()  # 自定义字段: 选择题选
    collect_count= serializers.SerializerMethodField()
    def get_like_count(self, obj):
        return obj.count_likers()
    def get_collect_count(self, obj):
        return obj.count_collecters()

    class Meta:
        model = Video
        fields = ["id", "status", "title", "desc", "file", "cover", "view_count", "like_count", "collect_count", "creator"]



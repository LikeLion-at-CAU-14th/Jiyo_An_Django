### Model Serializer case

from rest_framework import serializers
from .models import Post
from .models import Comment
from config.custom_api_exceptions import PostConflictException


class PostSerializer(serializers.ModelSerializer):
# 중복된 게시글 제목이 있다면 예외 발생
  def validate(self, data):
    if Post.objects.filter(title=data['title']).exists():
      raise PostConflictException(detail=f"A post with title: '{data['title']}' already exists.")
    
    return data
  
  class Meta:
    model = Post    # serializer가 어떤 모델을 기반으로 만들어지는지 >> post
    fields = "__all__"  # 모델에서 어떤 필드를 가져올지 >> 전체 필드
    read_only_fields = ("writer",)

class CommentSerializer(serializers.ModelSerializer):
    def validate_content(self, value):
        if len(value.strip()) < 15:
            raise serializers.ValidationError(
                "댓글은 최소 15자 이상 작성해야 합니다."
            )
        return value

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("post", "writer")

from .models import Image
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

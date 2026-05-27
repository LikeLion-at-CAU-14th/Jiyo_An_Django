from rest_framework.permissions import BasePermission
from datetime import datetime

class IsAllowedTime(BasePermission):
    def has_permission(self, request, view):
        now = datetime.now().hour

        # 제한 시간: 22시 - 7시
        if now >= 22 or now < 7:
            return False #403 에러
        
        return True
    
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        # GET, HEAD, OPTIONS (읽기 전용) 허용
        if request.method in SAFE_METHODS:
            return True
        
        # 작성자만 수정/삭제 가능
        return obj.writer == request.user
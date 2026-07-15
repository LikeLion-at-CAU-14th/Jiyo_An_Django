from rest_framework.exceptions import APIException


class DailyPostLimitException(APIException):
    status_code = 400
    default_detail = "게시글은 하루에 하나만 작성할 수 있습니다."
    default_code = "daily_post_limit"

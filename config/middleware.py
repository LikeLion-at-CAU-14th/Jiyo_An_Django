import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 요청 URL 로깅
        logger.info(f"Request URL: {request.get_full_path()}")

        response = self.get_response(request)
        return response


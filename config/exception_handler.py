from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    request = context.get("request")
    error = {
        "code": _get_error_code(exc),
        "message": _get_error_message(response.data),
        "status_code": response.status_code,
    }

    if isinstance(exc, ValidationError):
        error.update(
            {
                "code": "validation_error",
                "message": "입력값 검증에 실패했습니다.",
                "field_errors": _convert_error_details(response.data),
            }
        )

    response.data = {
        "success": False,
        "timestamp": timezone.now().isoformat(),
        "path": request.get_full_path() if request else "",
        "error": error,
        "data": None,
    }

    return response


def _get_error_code(exc):
    codes = exc.get_codes() if hasattr(exc, "get_codes") else None

    if isinstance(codes, str):
        return codes

    return getattr(exc, "default_code", "api_error")


def _get_error_message(error_data):
    if isinstance(error_data, dict) and "detail" in error_data:
        return str(error_data["detail"])

    if isinstance(error_data, list) and error_data:
        return str(error_data[0])

    if isinstance(error_data, dict):
        for value in error_data.values():
            if isinstance(value, list) and value:
                return str(value[0])
            return str(value)

    return str(error_data)


def _convert_error_details(value):
    if isinstance(value, dict):
        return {key: _convert_error_details(item) for key, item in value.items()}

    if isinstance(value, list):
        return [_convert_error_details(item) for item in value]

    return str(value)

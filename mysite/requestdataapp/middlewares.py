from django.http import HttpResponseForbidden
from django.core.cache import cache


class IPThrottleMiddleware:
    def __init__(self, get_response, rate_limit=3, period=60):
        self.get_response = get_response
        self.rate_limit = rate_limit
        self.period = period

    def __call__(self, request):
        ip = self.get_client_ip(request)
        if ip:
            cache_key = f'ip_throttle_{ip}'
            count = cache.get(cache_key, 0)

            if count >= self.rate_limit:
                return HttpResponseForbidden(f"Вы отправили больше {count} запросов. Попробуйте позже.")

            cache.set(cache_key, count + 1, self.period)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
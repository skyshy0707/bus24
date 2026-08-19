from django.http import HttpResponse

class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Сначала даем Django обработать запрос и сгенерировать ответ

        # Обработка Preflight-запросов (браузер часто шлет OPTIONS перед POST)
        response = HttpResponse(
            "Success",
            content_type="text/plain", 
            status=200
        ) if request.method == 'OPTIONS' else self.get_response(request)
        

        # 2. Добавляем заголовки CORS прямо в этот ответ
        # "http://localhost:8700" # URL клиента Vue # прокси

        origin = request.META.get('HTTP_ORIGIN', '')
        
        # Устанавливаем Access-Control-Allow-Origin в точности как в запросе
        if origin:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "DELETE, GET, PATCH, POST, PUT, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, X-Sec-CH-Device-Memory, X-User-Agent, X-Client-IP"
            response["Access-Control-Allow-Credentials"] = "true" # Если передаете куки/сессии
        print("exist request",  response.get("Access-Control-Allow-Origin"), " ")


        return response
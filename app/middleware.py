class CORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Configuración CORS muy permisiva
        origin = request.META.get('HTTP_ORIGIN', '*')
        response["Access-Control-Allow-Origin"] = origin if origin else "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "DELETE, GET, OPTIONS, PATCH, POST, PUT, HEAD"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Max-Age"] = "86400"
        response["Access-Control-Expose-Headers"] = "*"
        
        # Para peticiones OPTIONS, devolver respuesta inmediata
        if request.method == "OPTIONS":
            response.status_code = 200
            response.content = b""
        
        return response 
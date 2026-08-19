import re

from django.db import IntegrityError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None and isinstance(exc, IntegrityError):

        error_message = str(exc).lower()
        
        # 🌟 Фильтруем ошибку: реагируем ТОЛЬКО на нарушение уникальности
        if 'unique' in error_message:

            match = re.search(r"failed:\s+(\w+)\.(\w+)", error_message)

            if match: 
                table_name = match.group(1) # например, 'api_user'
                field_name = match.group(2) #

                if field_name == 'username' and table_name == 'api_user':
                    field_name = 'email'

                return Response(
                    {
                        "error": "unique_constraint",
                        "invalid_field": field_name, # 🌟 Передаем конкретное поле во Vue!
                        "message": f"Поле '{field_name}' должно быть уникальным. Такое значение уже занято."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            return Response(
                {
                    "error": "unique_constraint_error",
                    "message": "Такая запись уже существует."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Если это NOT NULL или FOREIGN KEY — пропускаем дальше.
        # Django вернет стандартную 500-ю ошибку, и вы увидите её в логах контейнера.

    return response
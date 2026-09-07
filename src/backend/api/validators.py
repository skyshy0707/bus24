from django.core.exceptions import ValidationError
from rest_framework import status

def route_wiki_url(value: str):
    if "wikiroutes.info/idea" in value:
        return value
    
    raise ValidationError("Invalid route url", code=status.HTTP_400_BAD_REQUEST)

def capacity(value: int):
    if value > 10:
        return value
    raise ValidationError(f"Incorrect capacity for bus: {value}", code=status.HTTP_400_BAD_REQUEST)



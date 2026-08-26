
from rest_framework import request
from rest_framework.permissions import BasePermission, IsAuthenticated

from api import models

def get_profile_id(request: request.Request):

    return models.ATP.objects.get(user_id=request.user.id).id

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return get_profile_id(request) == obj.atp_id
    

class IsLeadWasMessaged(BasePermission):

    def has_object_permission(self, request: request.Request, view, obj):
        lead_id = request.lead_id
        message_id = request.message_id
        message = models.Message.objects.get(id=message_id)
        
        return get_profile_id(request) in message.to.values("id") and lead_id == message.lead_id
    
class IsMessageToMe(BasePermission):

    def has_object_permission(self, request: request.Request, view, obj):

        return get_profile_id(request) in obj.to.values("id")
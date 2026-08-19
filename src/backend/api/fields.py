from api.models import ATP
from api.permissions import get_profile_id

class UserIdDefault:

    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context.get('request')
        user = request.user
        print("setted user_id:", user)

        return user
    
class ATPIdDefault:

    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context.get('request')
        atp = ATP.objects.get(id=get_profile_id(request))

        print("atp retrieved:", atp)

        return atp
    

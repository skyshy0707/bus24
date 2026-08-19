import os

import jwt
import logging
from rest_framework.authentication import (
    BaseAuthentication, 
    exceptions,
    get_authorization_header
)
from rest_framework.request import Request


from api.models import User
from api.utils import to_data_obj

from bearer_auth import settings
from bearer_auth.middleware.bearer_auth import utils
from bearer_auth.models import Token
from bearer_auth.serializers import DeserializeUserDecryptedData

from device.models import Device, UserDevice

logger = logging.getLogger(__name__)


class BearerAuthentication(BaseAuthentication):

    def authenticate(self, request: Request):

        try:
            method, sign = get_authorization_header(request).split()
        except ValueError:
            return None

        if method.lower() != b'bearer':
            return None
        if not sign:
            raise exceptions.AuthenticationFailed("Invalid basic header. No credentials provided.")
        
        secret_key = os.environ.get("SECRET_AUTH_KEY")

        print("sign: ", sign)

        try:
            decrypted = jwt.decode(sign, secret_key, algorithms=[settings.ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token")

        decrypted = DeserializeUserDecryptedData(
            data=decrypted
        )

        if not decrypted.is_valid():
            raise exceptions.AuthenticationFailed("Invalid credentials")
        
        decrypted: DeserializeUserDecryptedData = to_data_obj(decrypted.validated_data)

        
        
        try:
            jwt_token = Token.objects.get(id=decrypted.jti)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("Token not found")
        
        

        if not jwt_token.active:
            raise exceptions.AuthenticationFailed("Token is deactivated")
        
        expired = jwt_token.expired_refresh if decrypted.refresh else jwt_token.expired

        print("decrypted: ", decrypted.refresh, "expired: ", expired)

        if expired:
            raise exceptions.AuthenticationFailed("Token is expired")
        
        fingerprint = utils.calculate_fingerprint(request)

        logger.info(f"FINGER PRINT IN MW BEARER AUTH: {fingerprint}")


        ip = utils.get_client_ip(request)

        try:
            device = Device.objects.get(
                fingerprint=fingerprint, ip=ip
            )
        except Device.DoesNotExist as e:
            print("device not found", e)
            raise exceptions.AuthenticationFailed("Device not found")

        print(
            "jwt_token.userdevice_id", 
            jwt_token.userdevice_id,
            "user devivces ids: ",
            UserDevice.objects.filter(device=device).values_list('id', flat=True)
        )
        if jwt_token.userdevice_id not in UserDevice.objects.filter(device=device).values_list('id', flat=True):
            
            raise exceptions.AuthenticationFailed("Invalid access")

        user = User.objects.get(id=jwt_token.userdevice.user_id)
        
        return (user, None)
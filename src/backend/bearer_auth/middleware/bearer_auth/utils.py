import hashlib
import logging
import os
import re

from django.db.models import Model
import jwt
from rest_framework.request import Request

from bearer_auth.models import Token, settings
from bearer_auth.serializers import TokenData
from device.models import Device, UserDevice

logger = logging.getLogger(__name__)

def generate_salt(key_length: int) -> str:
    return os.urandom(int(key_length)).hex()

def get_client_ip(request: Request) -> str:
    """Возвращает настоящий IP-адрес клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # X-Forwarded-For: client, proxy1, proxy2
        ip = x_forwarded_for.split(',')[0].strip()  # Берём первый — это клиент
        logger.info(f"HTTP_X_FORWARDED_FOR: {ip}")

        return ip

    x_real_ip = request.META.get('HTTP_X_REAL_IP')
    if x_real_ip:
        logger.info(f"HTTP_X_REAL_IP: {x_real_ip}")
        return x_real_ip

    # На случай Cloudflare
    cf_connecting_ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if cf_connecting_ip:
        logger.info(f"HTTP_CF_CONNECTING_IP: {cf_connecting_ip}")
        return cf_connecting_ip

    # Фолбэк — только если нет прокси
    return request.META.get('REMOTE_ADDR')

def calculate_fingerprint(request: Request) -> str:

    user_agent_raw = request.META.get('HTTP_USER_AGENT', '')
    tokens = re.findall(r'([a-zA-Z\-]+)/\d+(?:\.\d+)*', user_agent_raw)

    if tokens:
        if tokens[-1] in ['Safari', 'Mobile'] and len(tokens) > 1:
            # Если на два шага назад стоит 'Version' (это признак оригинального Safari) 
            # или если перед Safari идет 'Version', то это Safari
            if len(tokens) > 2 and tokens[-2] in ['Version', 'Mobile'] and tokens[-3] == 'Version':
                browser_name = 'Safari'
            else:
                browser_name = tokens[-2]
        else:
            browser_name = tokens[-1]
    else:
        browser_name = 'Unknown Browser'

    print("browser: ", browser_name)

    clean_ua_structure = re.sub(r'/\d+(?:\.\d+)*', '', user_agent_raw)
    
    # Склеиваем стабильный паспорт устройства
    ultimate_passport = f"[{browser_name}] | {clean_ua_structure}"
    logger.info(f"HEADERS: {request.META}, {dir(request)}")
    parts = [
        #request.META.get('HTTP_USER_AGENT', ''),
        ultimate_passport,
        request.META.get(
            'HTTP_SEC_CH_DEVICE_MEMORY', 
            request.META.get('HTTP_X_SEC_CH_DEVICE_MEMORY', '')
        ), # Память
    ]
    full_string = '|'.join(parts)

    return hashlib.sha256(full_string.encode()).hexdigest()

def deactivate_tokens(request: Request, userdevice_id: int | None=None, session_model: Model=Token):
    if not userdevice_id:
        fingerprint = calculate_fingerprint(request)
        ip = get_client_ip(request)

        try:
            device = Device.objects.get(fingerprint=fingerprint, ip=ip)
            userdevice = UserDevice.objects.get(device=device, user=request.user)
        except (Device.DoesNotExist, UserDevice.DoesNotExist):
            print("Decice was deleted or not found")
            return
        userdevice_id = userdevice.id
    
    session_model.objects.filter(userdevice__id=userdevice_id, active=True).update(active=False)


def create_bearer_token(request: Request):

    ip = get_client_ip(request)
    fingerprint = calculate_fingerprint(request)
    device, _ = Device.objects.get_or_create(ip=ip, fingerprint=fingerprint)
    user_device, _ = UserDevice.objects.get_or_create(device=device, user=request.user)
    token = Token.objects.create(userdevice=user_device)
    decrypted = {
        "jti": str(token.id),
        "refresh": False
    }

    token_hash = jwt.encode(
        decrypted, 
        key=os.environ.get("SECRET_AUTH_KEY"), 
        algorithm=settings.ALGORITHM
    )
    decrypted["refresh"] = True
    refresh_token = jwt.encode(
        decrypted, 
        key=os.environ.get("SECRET_AUTH_KEY"), 
        algorithm=settings.ALGORITHM
    )

    token_data = TokenData(token)
    response_data = token_data.data
    response_data.update({ "token": token_hash, "refresh_token": refresh_token })

    return response_data



  

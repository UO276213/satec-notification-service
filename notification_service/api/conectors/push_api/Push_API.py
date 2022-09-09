import json
from .serializers import NotificationSerializer
from pywebpush import webpush
from os import path
from django.conf import settings


def notify(data):
    '''
    Envía notificaciones a los navegadores de los suscriptores
    '''
    serializer = NotificationSerializer(data=data)

    if not serializer.is_valid():
        raise BaseException(serializer.errors)

    vapid_pkey_file_path = path.join(
        settings.BASE_DIR, "api", "conectors", "push_api", "secrets", "private_key.pem")

    for subscription in data['subscription_data']:
        webpush(
            subscription_info=subscription,
            data=json.dumps(data['message']),
            vapid_private_key=vapid_pkey_file_path,
            vapid_claims={
                'sub': 'mailto:manuel.anton@satec.es'
            }
        )

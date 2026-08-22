from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer

from api.serializers import MessageSerializer


@receiver(post_save , sender=MessageSerializer.Meta.model)
def broadcast(sender, instance, created, **kwargs):

    if created:
        channel_layer = get_channel_layer()
        serialized = MessageSerializer(instance).data

        for recepient in instance.to.values_list('id', flat=True):
            async_to_sync(channel_layer.group_send)(
                f"user_{recepient.id}",
                {
                    "type": "message:create",
                    "action": "create",
                    "data": serialized
                }
            )
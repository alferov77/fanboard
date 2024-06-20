from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Responses


@receiver(post_save, sender=Responses)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            f'New comment on your post "{instance.post.title}"',
            f'{instance.author.username} commented: "{instance.text}"',
            'noreply@yourdomain.com',
            [instance.post.author.email],
            fail_silently=False,
        )

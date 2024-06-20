import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.mail import send_mail


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=4, blank=True, null=True)

    def generate_confirmation_code(self):
        self.confirmation_code = str(random.randint(1000, 9999))
        self.save()

    def __str__(self):
        return self.username


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.name}"


class Responses(models.Model):
    post = models.ForeignKey('message_board.Post', related_name='post_responses', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_responses', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Response by {self.author.username} on {self.post}'


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            recipients = User.objects.values_list('email', flat=True)
            send_mail(
                self.subject,
                self.message,
                'from@example.com',
                recipients,
                fail_silently=False,
            )
        else:
            super().save(*args, **kwargs)

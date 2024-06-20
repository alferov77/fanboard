from django.db import models
from django.conf import settings

class Responses(models.Model):
    post = models.ForeignKey('message_board.Post', related_name='responses', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Response by {self.author.username} on {self.post}'

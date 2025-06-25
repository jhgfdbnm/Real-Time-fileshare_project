from django.db import models
from datetime import timedelta
from django.utils import timezone

def default_expiry():
    return timezone.now() + timedelta(minutes=5)

class EncryptedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    key = models.BinaryField(default=bytes)
    nonce = models.BinaryField(default=bytes)
    tag = models.BinaryField(default=bytes)
    version = models.IntegerField(default=1)


    # ⏳ Expiry time field (default: 5 mins from now)
    expires_at = models.DateTimeField(default=default_expiry)
    has_been_downloaded = models.BooleanField(default=False)



    def __str__(self):
        return f"File uploaded at {self.uploaded_at}"





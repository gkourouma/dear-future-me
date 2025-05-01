from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Capsule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='capsule_images/', blank=True, null=True)
    open_date = models.DateField()

    def __str__(self):
        return self.title
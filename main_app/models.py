from django.db import models
from django.contrib.auth.models import User
from datetime import date
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.
class Capsule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='capsules')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=True)
    cover_image = models.ImageField(
        upload_to='capsule_images/',
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
    )
    open_date = models.DateField()

    def __str__(self):
        return self.title
    
    def is_unlockable(self):
        return not self.is_locked or self.open_date <= date.today()
    
class Memory(models.Model):
    capsule = models.ForeignKey(Capsule, on_delete=models.CASCADE, related_name='memories')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    title = models.CharField(max_length=255)
    date_taken = models.DateField(null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='memory_images/', blank=True, null=True)
    video = models.FileField(upload_to='memory_videos/', blank=True, null=True)
    audio = models.FileField(upload_to='memory_audios/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_memories', blank=True)

    def __str__(self):
        return f'Memory for {self.capsule.title} - {self.content[:20]}'
    def total_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username
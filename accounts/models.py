from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to='accounts/profiles/avatar')
    phone = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[str(self.pk)])

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else f"{settings.STATIC_URL}images/users/profile.svg"

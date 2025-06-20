from django.db import models
from django.conf import settings
from users.models import User

class Projects(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    director = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_director', blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']
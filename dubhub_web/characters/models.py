from django.db import models
from core.consts import GENDERS, VOICE_TYPES

class Character(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    gender = models.SmallIntegerField(choices=GENDERS, verbose_name='Gender')
    voice_type = models.SmallIntegerField(choices=VOICE_TYPES, verbose_name='Voice type', default=0)
    description = models.TextField(null=False, blank=True)
    photo = models.ImageField(upload_to='characters/fotos', verbose_name='Foto', default=None, null=True, blank=True)

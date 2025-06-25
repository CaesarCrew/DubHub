from django.shortcuts import render
from django.views import View
from django.http import Http404, FileResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User

class FotoUser(View):
    def get(self, request, arquivo):
        try:
            user = User.objects.get(photo='users/fotos/{}'.format(arquivo))
            return FileResponse(user.photo)
        except ObjectDoesNotExist:
            return Http404('<h1>Usuário não encontrado</h1>')